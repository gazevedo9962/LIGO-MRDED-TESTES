import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS
# =========================

N = 61
phi = np.zeros((N, N, N))
cx = cy = cz = N // 2

# =========================
# 2. FONTE SUAVIZADA
# =========================

x = np.arange(N)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

sigma = 1.5
r2 = (X-cx)**2 + (Y-cy)**2 + (Z-cz)**2

rho = np.exp(-r2 / (2*sigma**2))
rho /= np.sum(rho)  # massa total = 1

# =========================
# 3. SOLVER (SOR) — SINAL CORRETO
# =========================

omega = 1.8
tol = 1e-6

for it in range(5000):
    max_diff = 0.0

    for i in range(1, N-1):
        for j in range(1, N-1):
            for k in range(1, N-1):

                old = phi[i, j, k]

                new = (1/6) * (
                    phi[i+1,j,k] + phi[i-1,j,k] +
                    phi[i,j+1,k] + phi[i,j-1,k] +
                    phi[i,j,k+1] + phi[i,j,k-1] +
                    rho[i,j,k]            # <<< AQUI É +rho
                )

                phi[i,j,k] = (1-omega)*old + omega*new

                diff = abs(phi[i,j,k] - old)
                if diff > max_diff:
                    max_diff = diff

    if it % 200 == 0:
        print(f"Iter {it} | erro = {max_diff:.2e}")

    if max_diff < tol:
        print(f"Convergiu em {it} iterações")
        break

# remover offset
phi -= np.mean(phi)

# =========================
# 4. PERFIL 1D (EIXO X)
# =========================

r_vals = []
phi_vals = []

for dx in range(6, N//3):
    r_vals.append(dx)
    phi_vals.append(phi[cx + dx, cy, cz])  # agora φ já é positivo

r_vals = np.array(r_vals)
phi_vals = np.array(phi_vals)

# =========================
# 5. FIT
# =========================

coef = np.polyfit(np.log(r_vals), np.log(phi_vals), 1)
alpha = coef[0]

print("\n=========================")
print("Expoente final:", alpha)
print("=========================")

# =========================
# 6. PLOT
# =========================

plt.scatter(r_vals, phi_vals, s=15, label="dados")

r_fit = np.linspace(min(r_vals), max(r_vals), 100)
phi_fit = np.exp(coef[1]) * r_fit**alpha

plt.plot(r_fit, phi_fit, 'r--', label=f"fit ~ r^{alpha:.2f}")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("r")
plt.ylabel("φ(r)")
plt.legend()
plt.title("Potencial 3D (∇²φ = ρ)")

plt.show()