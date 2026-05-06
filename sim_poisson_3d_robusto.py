import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. GRID
# =========================

N = 201
cx = cy = cz = N // 2

x = np.arange(N)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

# distância ao centro
r = np.sqrt((X-cx)**2 + (Y-cy)**2 + (Z-cz)**2)

# evitar divisão por zero
r[cx, cy, cz] = 1

# =========================
# 2. POTENCIAL IDEAL
# =========================

phi = 1 / r

# =========================
# 3. PERFIL (EIXO X)
# =========================

r_vals = []
phi_vals = []

for dx in range(5, N//3):
    r_vals.append(dx)
    phi_vals.append(phi[cx + dx, cy, cz])

r_vals = np.array(r_vals)
phi_vals = np.array(phi_vals)

# =========================
# 4. EXPOENTE LOCAL (CORRETO)
# =========================

alpha_local = []

for i in range(1, len(r_vals)-1):
    dlog_phi = np.log(phi_vals[i+1]) - np.log(phi_vals[i-1])
    dlog_r = np.log(r_vals[i+1]) - np.log(r_vals[i-1])
    alpha_local.append(dlog_phi / dlog_r)

alpha_local = np.array(alpha_local)
r_mid = r_vals[1:-1]

# média região limpa
mask = (r_mid > 20) & (r_mid < 60)
alpha_mean = np.mean(alpha_local[mask])

print("\n=========================")
print("Expoente local médio:", alpha_mean)
print("=========================")

# =========================
# 5. PLOTS
# =========================

plt.figure(figsize=(12,5))

# gráfico log-log
plt.subplot(1,2,1)
plt.scatter(r_vals, phi_vals, s=10, label="dados")

r_fit = np.linspace(min(r_vals), max(r_vals), 100)
plt.plot(r_fit, 1/r_fit, 'r--', label="1/r")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("r")
plt.ylabel("φ")
plt.legend()
plt.title("Potencial ideal 1/r")

# expoente local
plt.subplot(1,2,2)
plt.plot(r_mid, alpha_local, label="α(r)")
plt.axhline(-1, linestyle="--", label="esperado")

plt.xlabel("r")
plt.ylabel("expoente")
plt.legend()
plt.title("Expoente local")

plt.tight_layout()
plt.show()