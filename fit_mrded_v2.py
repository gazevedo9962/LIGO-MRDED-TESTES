import numpy as np
from real_data_test import get_data

# =========================
# 1. CARREGAR DADOS
# =========================

t, strain = get_data()

# encontrar pico (merger)
peak = np.argmax(np.abs(strain))

# usar só ringdown (após pico)
t = t[peak:]
strain = strain[peak:]

# reset tempo
t = t - t[0]

# cortar janela (evitar ruído tardio)
mask = t < 0.1
t = t[mask]
strain = strain[mask]

# normalizar
strain = strain / np.max(np.abs(strain))

data = strain
sigma = np.std(strain)

A0 = 1.0

# =========================
# 2. MODELOS
# =========================

def generate_gr(t, A0, f, gamma):
    omega = 2 * np.pi * f
    return A0 * np.exp(-gamma * t) * np.cos(omega * t)

def generate_mrded(t, A0, f, gamma, Delta_t, R):
    omega = 2 * np.pi * f
    h = generate_gr(t, A0, f, gamma)

    N_ecos = 5

    for n in range(1, N_ecos + 1):
        t_n = n * Delta_t

        echo = A0 * (R**n) * np.exp(-gamma * (t - t_n)) * np.cos(omega * (t - t_n))
        echo[t < t_n] = 0

        h += echo

    return h

def chi2(data, model, sigma):
    return np.sum((data - model)**2 / sigma**2)

# =========================
# 3. GRID INTELIGENTE
# =========================

f_values = np.linspace(150, 300, 8)
gamma_values = np.linspace(50, 200, 8)

Delta_t_values = np.linspace(0.01, 0.05, 8)
R_values = np.linspace(0.1, 0.6, 8)

# =========================
# 4. FIT GR
# =========================

best_gr = None
best_chi2_gr = np.inf

for f in f_values:
    for gamma in gamma_values:
        h = generate_gr(t, A0, f, gamma)
        c2 = chi2(data, h, sigma)

        if c2 < best_chi2_gr:
            best_chi2_gr = c2
            best_gr = (f, gamma)

print("\n=== MELHOR GR ===")
print("f:", best_gr[0])
print("gamma:", best_gr[1])
print("chi2:", best_chi2_gr)

# =========================
# 5. FIT MRDED
# =========================

best_mrded = None
best_chi2_mrded = np.inf

for f in f_values:
    for gamma in gamma_values:
        for Delta_t in Delta_t_values:
            for R in R_values:

                h = generate_mrded(t, A0, f, gamma, Delta_t, R)
                c2 = chi2(data, h, sigma)

                if c2 < best_chi2_mrded:
                    best_chi2_mrded = c2
                    best_mrded = (f, gamma, Delta_t, R)

print("\n=== MELHOR MRDED ===")
print("f:", best_mrded[0])
print("gamma:", best_mrded[1])
print("Delta_t:", best_mrded[2])
print("R:", best_mrded[3])
print("chi2:", best_chi2_mrded)

# =========================
# 6. RESULTADO FINAL
# =========================

delta = best_chi2_gr - best_chi2_mrded

print("\n=== RESULTADO ===")
print("ΔChi² =", delta)