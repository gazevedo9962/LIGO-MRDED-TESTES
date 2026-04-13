import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS DO EVENTO
# =========================

A0 = 1.0                 # amplitude inicial
f = 250                  # frequência (Hz)
omega = 2 * np.pi * f    # rad/s
gamma = 200              # amortecimento (1/s)

# Tempo
t = np.linspace(0, 0.2, 5000)  # 0.2 segundos

# =========================
# 2. SINAL GR
# =========================

h_gr = A0 * np.exp(-gamma * t) * np.cos(omega * t)

# =========================
# 3. PARÂMETROS MRDED
# =========================

Delta_t = 0.03          # tempo entre ecos (s)
R = 0.3                 # coeficiente de reflexão
N_ecos = 5              # número de ecos

# Pequenas irregularidades (estrutura da rede)
np.random.seed(42)
epsilon = np.random.normal(0, 1e-3, N_ecos)

# =========================
# 4. SINAL MRDED
# =========================

h_mrded = np.copy(h_gr)

for n in range(1, N_ecos + 1):
    t_n = n * Delta_t + epsilon[n-1]
    
    echo = A0 * (R**n) * np.exp(-gamma * (t - t_n)) * np.cos(omega * (t - t_n))
    
    # evitar contribuição antes do tempo do eco
    echo[t < t_n] = 0
    
    h_mrded += echo

# =========================
# 5. RESIDUAL
# =========================

residual = h_mrded - h_gr


# =========================
# 5. GERAR DADOS REALISTAS (COM RUÍDO)
# =========================

sigma = 0.2
noise = sigma * np.random.normal(0, 1, len(t))

#data = h_mrded + noise
data = h_gr + noise

# =========================
# 6. CHI-QUADRADO
# =========================

chi2_gr = np.sum((data - h_gr)**2 / sigma**2)
chi2_mrded = np.sum((data - h_mrded)**2 / sigma**2)

print("Chi² GR:", chi2_gr)
print("Chi² MRDED:", chi2_mrded)

delta_chi2 = chi2_gr - chi2_mrded
print("ΔChi²:", delta_chi2)


# =========================
# 6. PLOTS
# =========================

plt.figure(figsize=(12, 8))

# GR vs MRDED

plt.figure(figsize=(10,5))
plt.plot(t, data, label="Dados (com ruído)", alpha=0.6)
plt.plot(t, h_gr, label="GR")
plt.plot(t, h_mrded, label="MRDED", linestyle="--")
plt.legend()
plt.title("Comparação com ruído")
plt.show()

'''
plt.subplot(3,1,1)
plt.plot(t, h_gr, label="GR")
plt.plot(t, h_mrded, label="MRDED", linestyle="--")
plt.title("Sinal GR vs MRDED")
plt.legend()

# Zoom no final (onde aparecem ecos)
plt.subplot(3,1,2)
plt.plot(t, h_mrded)
plt.xlim(0.05, 0.2)
plt.title("Zoom (Ecos MRDED)")

# Residual
plt.subplot(3,1,3)
plt.plot(t, residual)
plt.title("Residual (MRDED - GR)")

plt.tight_layout()
plt.show()
'''

