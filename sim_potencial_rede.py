import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS
# =========================

N = 101              # tamanho da grade (ímpar para ter centro)
steps = 500          # número de iterações
c = 0.2              # "velocidade" da rede
damping = 0.01       # amortecimento

# =========================
# 2. INICIALIZAÇÃO
# =========================

omega = np.zeros((N, N))
omega_new = np.zeros_like(omega)

# fonte central (massa)
cx, cy = N//2, N//2
omega[cx, cy] = 10.0

# =========================
# 3. EVOLUÇÃO (equação tipo Laplace / onda amortecida)
# =========================

for step in range(steps):
    for i in range(1, N-1):
        for j in range(1, N-1):
            
            laplacian = (
                omega[i+1,j] + omega[i-1,j] +
                omega[i,j+1] + omega[i,j-1] -
                4*omega[i,j]
            )
            
            omega_new[i,j] = omega[i,j] + c * laplacian - damping * omega[i,j]
    
    # manter fonte fixa
    omega_new[cx, cy] = 10.0
    
    omega = omega_new.copy()

# =========================
# 4. EXTRAIR PERFIL RADIAL
# =========================

r_values = []
phi_values = []

for i in range(N):
    for j in range(N):
        r = np.sqrt((i - cx)**2 + (j - cy)**2)
        
        if r > 0:
            r_values.append(r)
            phi_values.append(omega[i,j])

r_values = np.array(r_values)
phi_values = np.array(phi_values)

# ordenar por r
idx = np.argsort(r_values)
r_values = r_values[idx]
phi_values = phi_values[idx]

# =========================
# 5. MÉDIA RADIAL
# =========================

r_bins = np.linspace(1, N//2, 50)
phi_avg = []

for k in range(len(r_bins)-1):
    mask = (r_values >= r_bins[k]) & (r_values < r_bins[k+1])
    
    if np.sum(mask) > 0:
        phi_avg.append(np.mean(phi_values[mask]))
    else:
        phi_avg.append(np.nan)

r_mid = 0.5 * (r_bins[:-1] + r_bins[1:])
phi_avg = np.array(phi_avg)

# =========================
# 6. COMPARAÇÃO COM 1/r
# =========================

# normalizar para comparação
phi_norm = phi_avg / np.nanmax(phi_avg)
inv_r = 1 / r_mid
inv_r = inv_r / np.max(inv_r)

# =========================
# 7. PLOTS
# =========================

plt.figure(figsize=(6,6))
plt.imshow(omega, cmap="inferno")
plt.colorbar(label="Energia da rede")
plt.title("Campo ω (potencial emergente)")
plt.show()

plt.figure(figsize=(8,5))
plt.plot(r_mid, phi_norm, label="Rede (MRDED)")
plt.plot(r_mid, inv_r, '--', label="1/r")
plt.xlabel("r")
plt.ylabel("Potencial normalizado")
plt.legend()
plt.title("Teste: emergência de 1/r")
plt.show()