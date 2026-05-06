import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS
# =========================

N = 201
phi = np.zeros((N, N))
rho = np.zeros((N, N))

cx, cy = N // 2, N // 2
rho[cx, cy] = 1.0

# =========================
# 2. SOLVER (GAUSS-SEIDEL VETORIZADO)
# =========================

n_iter = 4000

for it in range(n_iter):

    phi[1:-1, 1:-1] = 0.25 * (
        phi[2:, 1:-1] +
        phi[:-2, 1:-1] +
        phi[1:-1, 2:] +
        phi[1:-1, :-2] +
        rho[1:-1, 1:-1]
    )

    # bordas
    phi[0, :] = 0
    phi[-1, :] = 0
    phi[:, 0] = 0
    phi[:, -1] = 0

    if it % 500 == 0:
        print(f"Iter {it}")

print("Convergiu!")

# =========================
# 3. PERFIL RADIAL (MÉDIA EM ANEL)
# =========================

r_bins = np.arange(1, N//2)
phi_r = []

for r in r_bins:
    mask = (np.sqrt((np.arange(N)[:,None]-cx)**2 + (np.arange(N)[None,:]-cy)**2) >= r) & \
           (np.sqrt((np.arange(N)[:,None]-cx)**2 + (np.arange(N)[None,:]-cy)**2) < r+1)

    values = np.abs(phi[mask])
    if len(values) > 0:
        phi_r.append(np.mean(values))
    else:
        phi_r.append(np.nan)

phi_r = np.array(phi_r)

# =========================
# 4. REGIÃO BOA (ASSINTÓTICA)
# =========================

mask_fit = (r_bins > 10) & (r_bins < 60)

log_r = np.log(r_bins[mask_fit])
log_phi = np.log(phi_r[mask_fit])

coef = np.polyfit(log_r, log_phi, 1)
alpha = coef[0]

print(f"\nExpoente corrigido: {alpha:.3f}")

# =========================
# 5. PLOT
# =========================

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.imshow(phi, cmap='inferno')
plt.colorbar(label="φ")
plt.title("Campo potencial")

plt.subplot(1,2,2)
plt.scatter(r_bins, phi_r, s=10, label="média radial")

r_fit = np.linspace(10, 60, 100)
phi_fit = np.exp(coef[1]) * r_fit**alpha

plt.plot(r_fit, phi_fit, 'r--', label=f"fit ~ r^{alpha:.2f}")
plt.xscale("log")
plt.yscale("log")
plt.legend()

plt.tight_layout()
plt.show()