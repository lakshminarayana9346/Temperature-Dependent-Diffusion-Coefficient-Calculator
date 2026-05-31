import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

# Gas Constant
R = 8.314

print("====================================")
print(" Diffusion Coefficient Calculator ")
print("====================================")

# User Inputs
Q = float(input("Enter Activation Energy Q (kJ/mol): "))
D0 = float(input("Enter Pre-exponential Factor D0 (m^2/s): "))
T_min = float(input("Enter Minimum Temperature (K): "))
T_max = float(input("Enter Maximum Temperature (K): "))

# Convert Q to J/mol
Q = Q * 1000

# Create folders if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# Temperature Array
T = np.linspace(T_min, T_max, 100)

# Arrhenius Equation
D = D0 * np.exp(-Q / (R * T))
inverse_temperature = 1 / T
ln_D = np.log(D)

slope, intercept, r_value, p_value, std_err = linregress(
    inverse_temperature,
    ln_D
)

fitted_ln_D = slope * inverse_temperature + intercept
# DataFrame
df = pd.DataFrame({
    "Temperature (K)": T,
    "Diffusion Coefficient (m^2/s)": D,
    "1/T (1/K)": inverse_temperature,
"ln(D)": ln_D
})

# Save CSV
df.to_csv("data/diffusion_results.csv", index=False)

# Plot 1
plt.figure(figsize=(8,5))
plt.plot(T, D, linewidth=2, marker="o", markersize=3)
plt.xlabel("Temperature (K)")
plt.ylabel("Diffusion Coefficient (m²/s)")
plt.title("Diffusion Coefficient vs Temperature")
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/diffusion_vs_temperature.png", dpi=300)

# Plot 2
plt.figure(figsize=(8,5))

plt.scatter(
    inverse_temperature,
    ln_D,
    label="Calculated Data"
)

plt.plot(
    inverse_temperature,
    fitted_ln_D,
    linewidth=2,
    label="Linear Fit"
)

plt.xlabel("1/T (1/K)")
plt.ylabel("ln(D)")
plt.title("Arrhenius Plot with Linear Regression")
plt.grid(True)
plt.legend()

plt.savefig(
    "figures/arrhenius_plot.png",
    dpi=300
)
print("\n===== Regression Results =====")

print(f"Slope = {slope:.4f}")
print(f"Intercept = {intercept:.4f}")
print(f"R² = {r_value**2:.6f}")
print("\nResults saved successfully!")
print("CSV file saved in data folder")
print("Graphs saved in figures folder")
plt.show()