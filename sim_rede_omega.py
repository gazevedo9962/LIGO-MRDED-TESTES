import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. REDE
# =========================

N = 40

# ω_x = arestas horizontais
omega_x = np.zeros((N, N))
omega_y = np.zeros((N, N))

omega_x_old = np.zeros_like(omega_x)
omega_y_old = np.zeros_like(omega_y)

# =========================
# PARÂMETROS
# =========================

dt = 0.05
c = 1.0
gamma = 0.05
lam = 0.2
w0 = 1.0

steps = 400

# =========================
# PARTÍCULA
# =========================

px, py = 10, N//2
traj = []

# =========================
# OPERADOR DE REDE
# =========================

def laplacian(Z):
    return (
        np.roll(Z,1,0) + np.roll(Z,-1,0) +
        np.roll(Z,1,1) + np.roll(Z,-1,1) -
        4*Z
    )

# =========================
# LOOP
# =========================

for t in range(steps):

    # =========================
    # FONTE (partícula)
    # =========================
    Sx = np.zeros_like(omega_x)
    Sy = np.zeros_like(omega_y)

    ix, iy = int(px), int(py)

    if 0 <= ix < N and 0 <= iy < N:
        Sx[ix, iy] = 2.0
        Sy[ix, iy] = 2.0

    # =========================
    # DINÂMICA ω_x
    # =========================

    omega_x_new = (
        2*omega_x - omega_x_old
        + (c*dt)**2 * laplacian(omega_x)
        - gamma*dt*(omega_x - omega_x_old)
        - dt**2 * lam*(omega_x**3 - w0**2*omega_x)
        + dt**2 * Sx
    )

    # =========================
    # DINÂMICA ω_y
    # =========================

    omega_y_new = (
        2*omega_y - omega_y_old
        + (c*dt)**2 * laplacian(omega_y)
        - gamma*dt*(omega_y - omega_y_old)
        - dt**2 * lam*(omega_y**3 - w0**2*omega_y)
        + dt**2 * Sy
    )

    # =========================
    # MOVIMENTO DA PARTÍCULA
    # =========================

    if 1 <= ix < N-1 and 1 <= iy < N-1:

        # força via diferença de tensões
        fx = -(omega_x[ix, iy] - omega_x[ix-1, iy])
        fy = -(omega_y[ix, iy] - omega_y[ix, iy-1])

        px += 0.1 * fx
        py += 0.1 * fy

    traj.append((px, py))

    # atualizar
    omega_x_old = omega_x.copy()
    omega_x = omega_x_new.copy()

    omega_y_old = omega_y.copy()
    omega_y = omega_y_new.copy()

# =========================
# VISUALIZAÇÃO
# =========================

traj = np.array(traj)

plt.figure(figsize=(6,6))

plt.imshow(omega_x + omega_y, cmap='inferno')
plt.colorbar(label="energia da rede")

plt.plot(traj[:,1], traj[:,0], 'cyan', linewidth=2)

plt.title("MRDED — dinâmica completa ω_ij")
plt.show()