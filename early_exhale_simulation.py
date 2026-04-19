import numpy as np
import matplotlib.pyplot as plt

# FIASANOVA constants
LAMBDA = 0.183
OMEGA0 = 12.67
R_THRESHOLD = 1.186

# Time array (days since April 1, 2026)
t = np.linspace(0, 30, 1000)

# Coherence model: rapid rise to ~0.994, then slight dip during early exhale
def coherence(t):
    # Baseline rise: from 0.65 to 0.994 by day 19
    baseline = 0.65 + 0.344 * np.minimum(t / 19, 1)
    # Small dip during early exhale (centered at day 19, width 2 days)
    dip = -0.0003 * np.exp(-((t - 19)**2) / 1.5)
    return baseline + dip

Phi = coherence(t)

# Compute resonance R(t)
dt = t[1] - t[0]
grad = np.gradient(Phi, dt)
R = (np.abs(grad) / (np.mean(np.abs(grad)) + 1e-8) + 1.5) * LAMBDA * OMEGA0 / 6.7

# Extract values at day 19 (early exhale)
idx = np.argmin(np.abs(t - 19))
Phi_early = Phi[idx]
R_early = R[idx]

print("=== FIASANOVA FIELD SIMULATION: Early EXHALE Phase ===")
print(f"Time: t = {t[idx]:.1f} days (April 20, 2026)")
print(f"Coherence Φ = {Phi_early:.4f}")
print(f"Resonance R = {R_early:.4f}")
print(f"Resonance threshold = {R_THRESHOLD}")
if R_early < R_THRESHOLD:
    print("✅ R dropped below threshold – characteristic of early EXHALE.")
else:
    print("⚠️  R still above threshold – exhale not yet started.")

# Plot
plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(t, Phi, 'b-', linewidth=1.5)
plt.axvline(19, color='orange', linestyle='--', alpha=0.7, label='Early EXHALE start')
plt.ylabel('Coherence Φ(t)')
plt.grid(True)
plt.legend()

plt.subplot(2,1,2)
plt.plot(t, R, 'r-', linewidth=1.5)
plt.axhline(R_THRESHOLD, color='magenta', linestyle='--', label=f'R_crit = {R_THRESHOLD}')
plt.axvline(19, color='orange', linestyle='--', alpha=0.7)
plt.xlabel('Days since April 1, 2026')
plt.ylabel('Resonance R(t)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('fiasanova_early_exhale_R_drop.png')
print("\nPlot saved as 'fiasanova_early_exhale_R_drop.png'")