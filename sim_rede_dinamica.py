import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. PARÂMETROS
# =========================

N = 120
dx = 1.0
dt = 0.1

c = 1.0
gamma = 0.05

steps = 600

# =========================
# 2. CAMPOS
# =========================

phi = np.zeros((N, N))
phi_old = np.zeros_like(phi)
phi_new = np.zeros_like(phi)

# =========================
# 3. PARTÍCULA
# =========================

px, py = 20.0, N//2
vx, vy = 0.0, 0.0

traj_x = []
traj_y = []

# =========================
# 4. FUNÇÕES AUXILIARES
# =========================

def laplacian(Z):
    return (
        np.roll(Z,1,0) + np.roll(Z,-1,0) +
        np.roll(Z,1,1) + np.roll(Z,-1,1) -
        4*Z
    ) / dx**2

def source(px, py):
    S = np.zeros((N,N))
    ix, iy = int(px), int(py)
    if 0 <= ix < N and 0 <= iy < N:
        S[ix, iy] = 10.0
    return S

# potencial (opcional)
def dV(phi):
    return 0.0
    # exemplo não-linear:
    # return 0.1 * (phi**3)

# =========================
# 5. LOOP TEMPORAL
# =========================

for t in range(steps):

    # fonte da partícula
    S = source(px, py)

    # equação de onda (leapfrog)
    phi_new = (
        2*phi - phi_old
        + (c*dt)**2 * laplacian(phi)
        - gamma*dt*(phi - phi_old)
        - dt**2 * dV(phi)
        + dt**2 * S
    )

    # =========================
    # MOVIMENTO DA PARTÍCULA
    # =========================

    ix, iy = int(px), int(py)

    if 1 <= ix < N-1 and 1 <= iy < N-1:

        # gradiente
        dphix = (phi[ix+1,iy] - phi[ix-1,iy]) / 2
        dphiy = (phi[ix,iy+1] - phi[ix,iy-1]) / 2

        # força
        fx = -dphix
        fy = -dphiy

        # atualização simples
        vx += fx * dt
        vy += fy * dt

        px += vx * dt
        py += vy * dt

    traj_x.append(px)
    traj_y.append(py)

    # atualizar campos
    phi_old = phi.copy()
    phi = phi_new.copy()

# pega linha central
perfil = phi[N//2, :]

# cria eixo radial
r = np.arange(len(perfil))

# =========================
# 6. PLOT
# =========================

plt.figure(figsize=(6,6))
plt.imshow(phi, cmap='inferno')
plt.colorbar(label="φ")

plt.plot(traj_y, traj_x, 'cyan', linewidth=2)
plt.title("Rede dinâmica + trajetória emergente")
plt.plot(r, perfil)
plt.title("Perfil do campo φ(r)")
plt.show()