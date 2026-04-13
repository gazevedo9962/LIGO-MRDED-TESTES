import numpy as np
import matplotlib.pyplot as plt
from real_data_test import get_data

# =========================
# 1. CARREGAR DADOS
# =========================

t, strain = get_data()

# alinhar pico do sinal
t = t - t[np.argmax(np.abs(strain))]

# tempo positivo (para evitar problemas na exponencial)
t0 = t - t.min()

# =========================
# 2. PARÂMETROS FÍSICOS
# =========================

A0 = np.max(np.abs(strain))     # amplitude real
gamma = 150                     # amortecimento

# chirp (frequência variável)
f0 = 40
f1 = 250

f_t = f0 + (f1 - f0) * (t0 / t0.max())
omega_t = 2 * np.pi * f_t

# =========================
# 3. SINAL GR (MELHORADO)
# =========================

h_gr = A0 * np.exp(-gamma * t0) * np.cos(omega_t * t)

# =========================
# 4. PARÂMETROS MRDED
# =========================

Delta_t = 0.03
R = 0.3
N_ecos = 5

np.random.seed(42)
epsilon = np.random.normal(0, 1e-3, N_ecos)

# =========================
# 5. SINAL MRDED
# =========================

h_mrded = np.copy(h_gr)

for n in range(1, N_ecos + 1):
    t_n = n * Delta_t + epsilon[n-1]

    echo = A0 * (R**n) * np.exp(-gamma * (t0 - t_n)) * np.cos(omega_t * (t - t_n))
    echo[t0 < t_n] = 0

    h_mrded += echo

# =========================
# 6. DADOS REAIS
# =========================

data = strain
sigma = np.std(strain)

# =========================
# 7. CHI-QUADRADO
# =========================

chi2_gr = np.sum((data - h_gr)**2 / sigma**2)
chi2_mrded = np.sum((data - h_mrded)**2 / sigma**2)

# normalização
chi2_gr /= len(t)
chi2_mrded /= len(t)

delta_chi2 = chi2_gr - chi2_mrded

print("Chi² GR:", chi2_gr)
print("Chi² MRDED:", chi2_mrded)
print("ΔChi²:", delta_chi2)

# =========================
# 8. PLOTS
# =========================N

plt.figure(figsize=(10,5))
plt.plot(t, data, label="Dados reais", alpha=0.6)
plt.plot(t, h_gr, label="GR")
plt.plot(t, h_mrded, label="MRDED", linestyle="--")
plt.legend()
plt.title("GW150914 - Comparação GR vs MRDED")
plt.xlabel("Tempo (s)")
plt.ylabel("Strain")
plt.show()

# =========================
# 9. RESIDUAL
# =========================

residual_gr = data - h_gr
residual_mrded = data - h_mrded

plt.figure(figsize=(10,4))
plt.plot(t, residual_gr, label="Residual GR")
plt.plot(t, residual_mrded, label="Residual MRDED", linestyle="--")
plt.legend()
plt.title("Residuals")
plt.show()