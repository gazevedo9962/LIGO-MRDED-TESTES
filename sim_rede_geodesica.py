import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. GRID
# =========================

N = 100
phi = np.zeros((N, N))

# =========================
# 2. MASSA CENTRAL (campo φ)
# =========================

cx, cy = N//2, N//2

for i in range(N):
    for j in range(N):
        r = np.sqrt((i-cx)**2 + (j-cy)**2) + 1e-5
        phi[i,j] = -1.0 / r   # campo gravitacional simples

# =========================
# 3. PARTÍCULA
# =========================

x, y = 10, N//2   # posição inicial

traj_x = []
traj_y = []

# =========================
# 4. MOVIMENTO (regra MRDED)
# =========================

for step in range(300):

    traj_x.append(x)
    traj_y.append(y)

    # vizinhos (cima, baixo, esquerda, direita)
    neighbors = [
        (x+1,y),(x-1,y),(x,y+1),(x,y-1)
    ]

    best = None
    best_cost = 1e9

    for nx, ny in neighbors:

        if 0 <= nx < N and 0 <= ny < N:

            # custo = diferença de φ (≈ ω)
            cost = phi[nx, ny]

            if cost < best_cost:
                best_cost = cost
                best = (nx, ny)

    if best is None:
        break

    x, y = best

# =========================
# 5. PLOT
# =========================

plt.figure(figsize=(6,6))

plt.imshow(phi, cmap='inferno')
plt.colorbar(label="φ (campo)")

plt.plot(traj_y, traj_x, 'cyan', linewidth=2, label="trajetória")

plt.scatter([cy],[cx], color='white', label="massa")

plt.legend()
plt.title("Geodésica emergente (MRDED)")
plt.show()