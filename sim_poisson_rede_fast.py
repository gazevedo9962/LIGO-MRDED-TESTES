import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS
# =========================

N = 101  # menor = muito mais rápido
phi = np.zeros((N, N))
rho = np.zeros((N, N))

cx, cy = N // 2, N // 2
rho[cx, cy] = 1.0

# =========================
# 2. SOLVER (JACOBI VETORIZADO)
# =========================

n_iter = 2000
tolerance = 1e-5

for it in range(n_iter):
    phi_new = np.copy(phi)

    # atualização vetorizada (sem loops!)
    phi_new[1:-1, 1:-1] = 0.25 * (
        phi[2:, 1:-1] +
        phi[:-2, 1:-1] +
        phi[1:-1, 2:] +
        phi[1:-1, :-2] +
        rho[1:-1, 1:-1]
    )

    # erro para convergência
    error = np.max(np.abs(phi_new - phi))

    phi = phi_new

    if it % 200 == 0:
        print(f"Iter {it} | erro = {error:.6e}")

    if error < tolerance:
        print(f"Convergiu em {it} iterações")
        break

# =========================
# 3. PERFIL RADIAL
# =========================

y, x = np.indices((N, N))
r = np.sqrt((x - cx)**2 + (y - cy)**2)

mask = (r > 2) & (r < N//2)

r_vals = r[mask]
phi_vals = np.abs(phi[mask])

# =========================
# 4. FIT (log-log)
# =========================

log_r = np.log(r_vals)
log_phi = np.log(phi_vals + 1e-12)  # evita log(0)

coef = np.polyfit(log_r, log_phi, 1)
alpha = coef[0]

print(f"\nExpoente encontrado: {alpha:.3f}")

# =========================
# 5. PLOTS
# =========================

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.imshow(phi, cmap='inferno')
plt.colorbar(label="φ")
plt.title("Campo potencial")

plt.subplot(1,2,2)
plt.scatter(r_vals, phi_vals, s=5, label="Rede")

r_fit = np.linspace(min(r_vals), max(r_vals), 100)
phi_fit = np.exp(coef[1]) * r_fit**alpha

plt.plot(r_fit, phi_fit, 'r--', label=f"fit ~ r^{alpha:.2f}")
plt.xscale("log")
plt.yscale("log")
plt.legend()

plt.tight_layout()
plt.show()