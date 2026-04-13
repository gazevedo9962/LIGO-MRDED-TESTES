from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
import h5py
import numpy as np

# baixar dados do detector LIGO (Hanford)
'''
data = TimeSeries.fetch_open_data('H1', 1126259446, 1126259462)

# normalizar
data = data.whiten()
'''

with h5py.File("H-H1_GWOSC_4KHZ_R1-1126259447-32.hdf5", "r") as f:
    strain = f["strain"]["Strain"][:]
    dt = f["strain"]["Strain"].attrs["Xspacing"]

# reconstruir manualmente
data = TimeSeries(strain, sample_rate=1/dt)

data = data.bandpass(20, 300)
data = data.whiten()

# tempo e sinal
t = data.times.value
strain = data.value


# =========================
# 2. RECORTAR EVENTO
# =========================

mask = (t > t.mean() - 0.1) & (t < t.mean() + 0.1)

t = t[mask]
strain = strain[mask]

# normalizar tempo
t = t - t[0]

# =========================
# 3. VISUALIZAR
# =========================

plt.figure(figsize=(10,4))
plt.plot(t, strain)
plt.title("GW150914 - Dados Reais")
plt.show()

# =========================
# EXPORTAR VARIÁVEIS
# =========================

def get_data():
    return t, strain