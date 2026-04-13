import numpy as np

# =========================
# TEMPO
# =========================

t = np.linspace(0, 0.1, 2000)

# =========================
# MODELOS
# =========================

def generate_gr(t, A0, f, gamma):
    omega = 2 * np.pi * f
    return A0 * np.exp(-gamma * t) * np.cos(omega * t)

def generate_mrded(t, A0, f, gamma, Delta_t, R):

    omega = 2 * np.pi * f
    h = generate_gr(t, A0, f, gamma)

    N_ecos = 5

    # novos parâmetros físicos
    phi0 = np.pi / 4
    alpha = 0.02
    beta = 0.3
    eta = 0.2

    for n in range(1, N_ecos + 1):

        t_n = n * Delta_t

        omega_n = omega * (1 + alpha * n)
        gamma_n = gamma * (1 + beta * n)
        R_n = R * np.exp(-eta * n)
        phi_n = n * phi0

        echo = (
            A0 * (R_n**n)
            * np.exp(-gamma_n * (t - t_n))
            * np.cos(omega_n * (t - t_n) + phi_n)
        )

        echo[t < t_n] = 0

        h += echo

    return h

'''
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
'''

def chi2(data, model, sigma):
    return np.sum((data - model)**2 / sigma**2)

# =========================
# PARÂMETROS FIXOS
# =========================

A0 = 1.0
f = 250
gamma = 150
Delta_t = 0.03

# ruído (nível LIGO aproximado)
sigma = 0.2

# =========================
# TESTE DE DETECTABILIDADE
# =========================

R_values = np.linspace(0.05, 0.8, 20)

print("\n=== TESTE DE DETECTABILIDADE ===\n")

for R in R_values:

    # sinal verdadeiro (MRDED)
    true_signal = generate_mrded(t, A0, f, gamma, Delta_t, R)

    # adicionar ruído
    noise = sigma * np.random.normal(0, 1, len(t))
    data = true_signal + noise

    # modelo GR
    h_gr = generate_gr(t, A0, f, gamma)

    # modelo MRDED
    h_mrded = generate_mrded(t, A0, f, gamma, Delta_t, R)

    # chi2
    chi_gr = chi2(data, h_gr, sigma)
    chi_mrded = chi2(data, h_mrded, sigma)

    delta = chi_gr - chi_mrded

    print(f"R = {R:.2f} | ΔChi² = {delta:.2f}")