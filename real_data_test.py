from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt

# baixar dados do detector LIGO (Hanford)
'''
data = TimeSeries.fetch_open_data('H1', 1126259446, 1126259462)

# normalizar
data = data.whiten()
'''

url = "https://www.gwosc.org/eventapi/json/GWTC-1-confident/GW150914/v3/H-H1_LOSC_4_V2-1126259446-32.hdf5"
data = TimeSeries.read(url)

# filtro passa-banda (remove ruído fora da banda relevante)
data = data.bandpass(20, 300)

# tempo e sinal
t = data.times.value
strain = data.value

plt.figure(figsize=(10,4))
plt.plot(t, strain)
plt.title("Sinal real LIGO (GW150914)")
plt.xlabel("Tempo")
plt.ylabel("Strain")
plt.show()