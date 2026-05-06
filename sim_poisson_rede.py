import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS DA REDE
# =========================

N = 201              # tamanho da grade (ímpar para ter centro)
phi = np.zeros((N, N))
rho = np.zeros((N, N))

# posição da fonte (centro)
cx, cy = N // 2, N // 2

# fonte pontual (delta discreta)
rho[cx, cy] = 1.0

# =========================
# 2. RESOLVER POISSON
# =========================

n_iter = 8000

for it in range(n_iter):
    for i in range(1, N-1):
        for j in range(1, N-1):
            phi[i, j] = 0.25 * (
                phi[i+1, j] +
                phi[i-1, j] +
                phi[i, j+1] +
                phi[i, j-1] +
                rho[i, j]
            )

    # condição de contorno (bordas = 0)
    phi[0, :] = 0
    phi[-1, :] = 0
    phi[:, 0] = 0
    phi[:, -1] = 0

    # debug leve
    if it % 1000 == 0:
        print(f"Iteração {it}")

print("Convergiu!")

# =========================
# 3. EXTRAIR PERFIL RADIAL
# =========================

r_vals = []
phi_vals = []

for i in range(N):
    for j in range(N):
        r = np.sqrt((i - cx)**2 + (j - cy)**2)
        if r > 2 and r < N//2:
            r_vals.append(r)
            phi_vals.append(abs(phi[i, j]))

r_vals = np.array(r_vals)
phi_vals = np.array(phi_vals)

# =========================
# 4. AJUSTE DE LEI DE POTÊNCIA
# =========================

log_r = np.log(r_vals)
log_phi = np.log(phi_vals)

coef = np.polyfit(log_r, log_phi, 1)
alpha = coef[0]

print(f"\nExpoente encontrado: {alpha:.3f}")

# =========================
# 5. PLOTS
# =========================

plt.figure(figsize=(12,5))

# campo 2D
plt.subplot(1,2,1)
plt.imshow(phi, cmap='inferno')
plt.colorbar(label="Potencial φ")
plt.title("Campo potencial (Poisson)")

# lei de potência
plt.subplot(1,2,2)
plt.scatter(r_vals, phi_vals, s=5, label="Rede")

r_fit = np.linspace(min(r_vals), max(r_vals), 100)
phi_fit = np.exp(coef[1]) * r_fit**alpha

plt.plot(r_fit, phi_fit, 'r--', label=f"fit ~ r^{alpha:.2f}")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("r")
plt.ylabel("|φ|")
plt.legend()
plt.title("Teste de lei de potência")

plt.tight_layout()
plt.show()