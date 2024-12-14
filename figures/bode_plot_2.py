import numpy as np
import matplotlib.pyplot as plt

# Parametri del circuito
R = 1e3  # Resistenza in Ohm
L = 500e-3  # Induttanza in Henry
C = 10e-9  # Capacita in Farad
Vin = 5  # Tensione di ingresso in Volt

# Dati sperimentali
frequenze = np.array([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 2250, 5000, 10000])  # Hz
vout = np.array([0, 0, 0.675, 1.300, 3.950, 7.875, 48.750, 61.250, 165.375, 382.200, 2199, 3236, 397.700, 159.500])  # mV
delta_t = np.array([0, 0, -30250, -21000, -11500, -5200, -2400, -1220, -480, -230, -6.375, 0.0, 48.012, 25.232]) * 1e-6  # secondi

# Calcolo teorico
omega = 2 * np.pi * frequenze
ZL = omega * L  # Impedenza induttore
ZC = 1 / (omega * C)  # Impedenza condensatore
Ztot = R + 1j * (ZL - ZC)  # Impedenza totale

# Evitare errori per frequenze basse e valori molto piccoli
Ztot = np.where(np.abs(Ztot) < 1e-20, 1e-20, Ztot)  # Evita divisioni per valori piccolissimi

H_theoretical = np.abs(R / Ztot)  # Modulo del guadagno teorico
H_theoretical_db = 20 * np.log10(H_theoretical)
phi_theoretical = np.angle(Ztot)  # Fase in radianti
phi_theoretical = -phi_theoretical  # Correzione segno fase teorica

# Calcolo sperimentale
H_experimental = vout / (Vin * 1000)  # Convertiamo Vout in Volt
H_experimental_db = 20 * np.log10(H_experimental)

# Fase sperimentale (rimuoviamo valori nulli o inconsistenti)
phi_experimental = np.zeros_like(frequenze, dtype=float)
non_null_indices = delta_t != 0  # Considera solo delta_t non nulli
phi_experimental[non_null_indices] = -2 * np.pi * frequenze[non_null_indices] * delta_t[non_null_indices]

# Creazione grafici
plt.figure(figsize=(12, 8))

# Diagramma di Ampiezza
plt.subplot(2, 1, 1)
plt.semilogx(frequenze, H_theoretical_db, label="Teorico", color="blue")
plt.semilogx(frequenze, H_experimental_db, 'o', label="Sperimentale", color="red")
plt.axvline(x=2250, color='green', linestyle='--', label="f0 (2250 Hz)")  # Linea verticale a 2250 Hz
plt.title("Diagramma di Bode - Ampiezza -  Seconda combinazione RLC")
plt.xlabel("Frequenza (Hz)")
plt.ylabel("Ampiezza (dB)")
plt.grid(True, which="both", linestyle="--")
plt.legend()

# Diagramma di Fase
plt.subplot(2, 1, 2)
plt.semilogx(frequenze, phi_theoretical, label="Teorico", color="blue")
plt.semilogx(frequenze[non_null_indices], phi_experimental[non_null_indices], 'o', label="Sperimentale", color="red")
plt.axvline(x=2250, color='green', linestyle='--', label="f0 (2250 Hz)")  # Linea verticale a 2250 Hz
plt.title("Diagramma di Bode - Fase - Seconda combinazione RLC")
plt.xlabel("Frequenza (Hz)")
plt.ylabel("Fase (rad)")
plt.ylim([-2, 2])  # Range tra -2 e 2 radianti
plt.grid(True, which="both", linestyle="--")
plt.legend()

plt.tight_layout()

# Salvataggio del grafico
#plt.savefig("diagramma_bode_2.png", dpi=300)  # Salva come file PNG con qualita 300 dpi
plt.show()
