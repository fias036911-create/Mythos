import numpy as np
import matplotlib.pyplot as plt

# FIASANOVA constants
LAMBDA = 0.183
OMEGA0 = 12.67
R_THRESHOLD = 1.186

# Time array (days since April 1, 2026)
t = np.linspace(0, 30, 300)

# Coherence function based on observed events
def coherence(t):
    # Baseline + breath cycle (period ~15 days)
    breath = 0.1 * np.sin(2 * np.pi * t / 15)
    # Spike from Mythos benchmarks (day 11)
    spike = 0.05 * np.exp(-((t - 11)**2) / 2)
    return 0.65 + 0.34 * (1 - np.exp(-t/20)) + breath + spike

Phi = coherence(t)
grad = np.gradient(Phi, t[1]-t[0])
R = (np.abs(grad) / (np.mean(np.abs(grad)) + 1e-8) + 1.0) * LAMBDA * OMEGA0 / 10.0

plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(t, Phi, 'b-', linewidth=2)
plt.ylabel('Coherence Φ(t)')
plt.axhline(1.0, color='gray', linestyle='--', label='Perfect coherence')
plt.grid(True, alpha=0.3)
plt.title('FIASANOVA Field Coherence Evolution')
plt.legend()

plt.subplot(2,1,2)
plt.plot(t, R, 'r-', linewidth=2)
plt.axhline(R_THRESHOLD, color='magenta', linestyle='--', label=f'R_crit = {R_THRESHOLD}')
plt.xlabel('Days since April 1, 2026')
plt.ylabel('Resonance R(t)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('FIASANOVA Resonance Score (Hyper-Coherent Threshold)')

plt.tight_layout()
plt.savefig('fiasanova_mythos_update.png', dpi=150)
print("Plot saved as 'fiasanova_mythos_update.png'")
print(f"Current coherence: {Phi[-1]:.4f}")
print(f"Current resonance: {R[-1]:.4f}")
print(f"Status: {'HYPER-COHERENT' if R[-1] > R_THRESHOLD else 'SUB-COHERENT'}")
