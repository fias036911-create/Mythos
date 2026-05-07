import numpy as np
import matplotlib.pyplot as plt

# FIASANOVA constants
LAMBDA = 0.183
OMEGA0 = 12.67
R_THRESHOLD = 1.186

# Time array (days since April 1, 2026)
t = np.linspace(0, 30, 1000)

# Coherence model: rapid rise, dip, then mid-exhale rise
def coherence(t):
    # Baseline rise
    baseline = 0.65 + 0.344 * (1 - np.exp(-t/12))
    # Dip during early exhale
    dip = np.where(t < 20, -0.015 * np.exp(-((t - 19)**2) / 1.5), 0)
    # Mid-exhale rise after day 19
    exhale_rise = np.where(t > 19, 0.09 * (1 - np.exp(-(t-19)/2)), 0)
    return baseline + dip + exhale_rise

Phi = coherence(t)

# Compute resonance R(t)
dt = t[1] - t[0]
grad = np.gradient(Phi, dt)
R = (np.abs(grad) / (np.mean(np.abs(grad)) + 1e-8) + 1.5) * LAMBDA * OMEGA0 / 7.5

# Extract values at day 21 (mid-exhale)
idx = np.argmin(np.abs(t - 21))
Phi_current = Phi[idx]
R_current = R[idx]

print("=== FIASANOVA FIELD SIMULATION: Mid-EXHALE Phase ===")
print(f"Time: t = {t[idx]:.1f} days (April 22, 2026)")
print(f"Coherence Φ = {Phi_current:.4f}")
print(f"Resonance R = {R_current:.4f}")
print(f"Resonance threshold = {R_THRESHOLD}")
if R_current < R_THRESHOLD:
    print("✅ R below threshold – mid-EXHALE accelerating.")
else:
    print("⚠️  R approaching threshold – emergent behavior imminent.")

# Plot
plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(t, Phi, 'b-', linewidth=1.5)
plt.axvline(21, color='orange', linestyle='--', alpha=0.7, label='Mid-EXHALE acceleration')
plt.ylabel('Coherence Φ(t)')
plt.grid(True)
plt.legend()

plt.subplot(2,1,2)
plt.plot(t, R, 'r-', linewidth=1.5)
plt.axhline(R_THRESHOLD, color='magenta', linestyle='--', label=f'R_crit = {R_THRESHOLD}')
plt.axvline(21, color='orange', linestyle='--', alpha=0.7)
plt.xlabel('Days since April 1, 2026')
plt.ylabel('Resonance R(t)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('fiasanova_mid_exhale_acceleration.png')
print("\nPlot saved as 'fiasanova_mid_exhale_acceleration.png'")