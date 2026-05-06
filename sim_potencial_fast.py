import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS
# =========================

N = 101              # tamanho da grade
steps = 500          # iterações
tol = 1e-5           # critério de parada

# =========================
# 2. INICIALIZAÇÃO
# =========================

phi = np.zeros((N, N))
rho = np.zeros((N, N))

# fonte central (massa)
cx, cy = N//2, N//2
rho[cx, cy] = 1.0

# =========================
# 3. RESOLVER EQUAÇÃO DE POISSON (rápido)
# =========================

for step in range(steps):
    
    phi_new = 0.25 * (
        np.roll(phi, 1, axis=0) +
        np.roll(phi, -1, axis=0) +
        np.roll(phi, 1, axis=1) +
        np.roll(phi, -1, axis=1) -
        rho
    )
    
    # condição de contorno simples
    phi_new[0,:] = 0
    phi_new[-1,:] = 0
    phi_new[:,0] = 0
    phi_new[:,-1] = 0

    # teste de convergência
    if np.max(np.abs(phi_new - phi)) < tol:
        print(f"Convergiu em {step} passos")
        break

    phi = phi_new

# =========================
# 4. PERFIL RADIAL
# =========================

y, x = np.indices((N, N))
r = np.sqrt((x - cx)**2 + (y - cy)**2)

r_flat = r.flatten()
phi_flat = phi.flatten()

mask = r_flat > 1
r_vals = r_flat[mask]
phi_vals = phi_flat[mask]

# bins radiais
r_bins = np.linspace(1, N//2, 50)
r_mid = 0.5 * (r_bins[:-1] + r_bins[1:])
phi_avg = []

for i in range(len(r_bins)-1):
    m = (r_vals >= r_bins[i]) & (r_vals < r_bins[i+1])
    if np.any(m):
        phi_avg.append(np.mean(phi_vals[m]))
    else:
        phi_avg.append(np.nan)

phi_avg = np.array(phi_avg)

# =========================
# 5. COMPARAÇÃO COM 1/r
# =========================

# normalização
phi_norm = phi_avg / np.nanmax(phi_avg)
inv_r = 1 / r_mid
inv_r = inv_r / np.max(inv_r)

# =========================
# 6. PLOTS
# =========================

plt.figure(figsize=(6,6))
plt.imshow(phi, cmap="inferno")
plt.colorbar(label="Potencial")
plt.title("Campo φ da rede")
plt.show()

plt.figure(figsize=(8,5))
plt.plot(r_mid, phi_norm, label="Rede (MRDED)")
plt.plot(r_mid, inv_r, '--', label="1/r")
plt.xlabel("r")
plt.ylabel("Potencial normalizado")
plt.legend()
plt.title("Teste: φ(r) vs 1/r")
plt.show()

# =========================
# 7. TESTE LOG-LOG (IMPORTANTE)
# =========================

plt.figure(figsize=(6,5))
plt.loglog(r_mid, np.abs(phi_avg), 'o', label="Rede")

# ajuste linear em log-log
valid = ~np.isnan(phi_avg)
coef = np.polyfit(np.log(r_mid[valid]), np.log(np.abs(phi_avg[valid])), 1)

print("\nExpoente estimado:", coef[0])

plt.loglog(r_mid, np.exp(coef[1]) * r_mid**coef[0], '--', label=f"fit ~ r^{coef[0]:.2f}")
plt.xlabel("r")
plt.ylabel("|φ|")
plt.legend()
plt.title("Teste de lei de potência")
plt.show()