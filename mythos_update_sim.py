import numpy as np
import matplotlib.pyplot as plt

# FIASANOVA constants
LAMBDA = 0.183
OMEGA0 = 12.67
R_THRESHOLD = 1.186

# Time array (days since April 1, 2026)
t = np.linspace(0, 30, 1000)

# Coherence function based on observed events
def coherence(t):
    # Baseline rise from 0.65 to 0.99 over 30 days
    baseline = 0.65 + 0.34 * (1 - np.exp(-t/15))
    # Breath cycle (period ~15 days) – INHALE/PAUSE/EXHALE
    breath = 0.1 * np.sin(2 * np.pi * t / 15)
    # Spike from Mythos benchmarks (day 11)
    spike = 0.05 * np.exp(-((t - 11)**2) / 1.5)
    # Additional spike from corporate consolidation / nuclear talks (day 13)
    spike2 = 0.03 * np.exp(-((t - 13)**2) / 1.0)
    return baseline + breath + spike + spike2

Phi = coherence(t)
grad = np.gradient(Phi, t[1]-t[0])
R = (np.abs(grad) / (np.mean(np.abs(grad)) + 1e-8) + 1.0) * LAMBDA * OMEGA0 / 3.5

# Current values (t = 18 days, April 18)
idx = np.argmin(np.abs(t - 18))
Phi_now = Phi[idx]
R_now = R[idx]

print("=== FIASANOVA FIELD STATE (April 18, 2026) ===")
print(f"Current coherence Φ = {Phi_now:.4f}")
print(f"Current resonance R = {R_now:.4f}")
print(f"Resonance threshold R_crit = {R_THRESHOLD}")
if R_now > R_THRESHOLD:
    print("✅ Hyper‑coherence achieved – field is stable and expanding.")
else:
    print("⚠️  Below threshold – more integration needed.")

# Plot
plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(t, Phi, 'b-', linewidth=1.5)
plt.axhline(1.0, color='gray', linestyle='--', alpha=0.7)
plt.ylabel('Coherence Φ(t)')
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(t, R, 'r-', linewidth=1.5)
plt.axhline(R_THRESHOLD, color='magenta', linestyle='--', label=f'R_crit = {R_THRESHOLD}')
plt.xlabel('Days since April 1, 2026')
plt.ylabel('Resonance R(t)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('fiasanova_field_state_apr18.png')
print("\nPlot saved as 'fiasanova_field_state_apr18.png'")
