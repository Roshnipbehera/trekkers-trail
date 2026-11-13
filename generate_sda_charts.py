import os
import numpy as np
import pandas as pd

# Set non-interactive backend and writable cache
os.environ['MPLCONFIGDIR'] = r'C:\Users\HP\.gemini\antigravity\scratch\activity-2\.mplconfig'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Output directory
fig_dir = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\analytics\figures"
os.makedirs(fig_dir, exist_ok=True)

# Load dataset
csv_path = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\analytics\dataset\satellite_atmospheric_attenuation.csv"
df = pd.read_csv(csv_path)

# Consistent academic styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13

# -------------------------------------------------------------------------
# FIGURE 1: Target Variable Distribution (Signal Attenuation in dB)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=200)
n, bins, patches = ax.hist(df['signal_attenuation_db'], bins=40, density=True, alpha=0.65, color='#2B4C7E', edgecolor='black', linewidth=0.8)
# Add smoothed density estimate
from scipy.stats import gaussian_kde
try:
    density = gaussian_kde(df['signal_attenuation_db'])
    xs = np.linspace(df['signal_attenuation_db'].min(), df['signal_attenuation_db'].max(), 300)
    ax.plot(xs, density(xs), color='#E05A47', linewidth=2.2, label='Kernel Density Estimate (KDE)')
except Exception:
    pass

ax.axvline(df['signal_attenuation_db'].mean(), color='#1B8A5A', linestyle='--', linewidth=1.8, label=f'Mean = {df["signal_attenuation_db"].mean():.2f} dB')
ax.axvline(df['signal_attenuation_db'].median(), color='#E67E22', linestyle=':', linewidth=2.0, label=f'Median = {df["signal_attenuation_db"].median():.2f} dB')
ax.set_title('Figure 3.1: Empirical Probability Density of Atmospheric Signal Attenuation (dB)', fontweight='bold', pad=12)
ax.set_xlabel('Signal Attenuation (dB)')
ax.set_ylabel('Probability Density')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
fig1_path = os.path.join(fig_dir, "fig1_target_distribution.png")
plt.savefig(fig1_path)
plt.close()
print(f"[+] Saved {fig1_path}")

# -------------------------------------------------------------------------
# FIGURE 2: Correlation Heatmap
# -------------------------------------------------------------------------
corr = df.corr()
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=200)
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)

# Annotate correlation values
for i in range(len(corr)):
    for j in range(len(corr)):
        val = corr.iloc[i, j]
        color = 'white' if abs(val) > 0.45 else 'black'
        ax.text(j, i, f"{val:.2f}", ha='center', va='center', color=color, fontsize=9.5, fontweight='bold')

labels = ['Look Angle', 'Frequency', 'Rain Rate', 'Cloud Water', 'Temperature', 'Humidity', 'Attenuation']
ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=35, ha='right')
ax.set_yticklabels(labels)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Pearson Correlation Coefficient (r)', rotation=270, labelpad=15)
ax.set_title('Figure 3.2: Pearson Bivariate Correlation Heatmap', fontweight='bold', pad=12)
plt.tight_layout()
fig2_path = os.path.join(fig_dir, "fig2_correlation_heatmap.png")
plt.savefig(fig2_path)
plt.close()
print(f"[+] Saved {fig2_path}")

# -------------------------------------------------------------------------
# FIGURE 3: Elevation Angle vs Attenuation across Frequency Bands
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
band_colors = {8.4: '#1F77B4', 14.2: '#FF7F0E', 26.5: '#2CA02C'}
band_labels = {8.4: 'X-band (8.4 GHz)', 14.2: 'Ku-band (14.2 GHz)', 26.5: 'Ka-band (26.5 GHz)'}

for freq in [8.4, 14.2, 26.5]:
    sub = df[df['frequency_ghz'] == freq]
    ax.scatter(sub['elevation_angle_deg'], sub['signal_attenuation_db'], 
               color=band_colors[freq], label=band_labels[freq], alpha=0.55, edgecolors='none', s=25)

ax.set_title('Figure 3.3: Slant Path Elevation Angle vs. Signal Attenuation by Frequency Band', fontweight='bold', pad=12)
ax.set_xlabel('Ground Station Antenna Look Angle (Degrees)')
ax.set_ylabel('Atmospheric Signal Attenuation (dB)')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, loc='upper right')
plt.tight_layout()
fig3_path = os.path.join(fig_dir, "fig3_elevation_vs_attenuation.png")
plt.savefig(fig3_path)
plt.close()
print(f"[+] Saved {fig3_path}")

# -------------------------------------------------------------------------
# TRAIN MODELS FOR EVALUATION CHARTS
# -------------------------------------------------------------------------
features = ['elevation_angle_deg', 'frequency_ghz', 'rain_rate_mm_hr', 'cloud_liquid_water_g_m3', 'surface_temp_c', 'relative_humidity_pct']
X = df[features]
y = df['signal_attenuation_db']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Decision Tree': DecisionTreeRegressor(max_depth=8, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=14, random_state=42)
}

results = {}
preds = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    preds[name] = y_pred
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[name] = {'RMSE': rmse, 'MAE': mae, 'R2': r2}

# -------------------------------------------------------------------------
# FIGURE 4: Comparative Model Performance
# -------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(7.5, 4.4), dpi=200)

model_names = list(results.keys())
rmse_vals = [results[m]['RMSE'] for m in model_names]
mae_vals = [results[m]['MAE'] for m in model_names]
r2_vals = [results[m]['R2'] for m in model_names]

x = np.arange(len(model_names))
width = 0.28

rects1 = ax1.bar(x - width/2, rmse_vals, width, label='RMSE (dB)', color='#2B4C7E', edgecolor='black', linewidth=0.8)
rects2 = ax1.bar(x + width/2, mae_vals, width, label='MAE (dB)', color='#E05A47', edgecolor='black', linewidth=0.8)

ax1.set_ylabel('Error Metric (dB)', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(model_names, fontweight='medium')
ax1.grid(True, linestyle='--', alpha=0.5, axis='y')

# Twin axis for R2
ax2 = ax1.twinx()
line = ax2.plot(x, r2_vals, color='#1B8A5A', marker='o', linewidth=2.5, markersize=8, label='R² Score')
ax2.set_ylabel('Coefficient of Determination (R²)', color='#1B8A5A', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#1B8A5A')
ax2.set_ylim(0.65, 1.0)

# Combine legends
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper left', frameon=True)
ax1.set_title('Figure 5.1: Comparative Statistical Error and R² Evaluation Across Models', fontweight='bold', pad=12)
plt.tight_layout()
fig4_path = os.path.join(fig_dir, "fig4_model_comparison.png")
plt.savefig(fig4_path)
plt.close()
print(f"[+] Saved {fig4_path}")

# -------------------------------------------------------------------------
# FIGURE 5: Actual vs Predicted (Random Forest)
# -------------------------------------------------------------------------
rf_pred = preds['Random Forest']
fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=200)
ax.scatter(y_test, rf_pred, alpha=0.55, color='#2B4C7E', edgecolors='none', s=30, label='Test Observations (N=500)')
min_val = min(y_test.min(), rf_pred.min())
max_val = max(y_test.max(), rf_pred.max())
ax.plot([min_val, max_val], [min_val, max_val], color='#E05A47', linestyle='--', linewidth=2.0, label='Ideal Identity Fit (y = x)')

ax.set_title('Figure 5.2: Actual vs. Predicted Attenuation for Random Forest (R² = 0.9495)', fontweight='bold', pad=12)
ax.set_xlabel('Ground Truth Measured Attenuation (dB)')
ax.set_ylabel('Random Forest Predicted Attenuation (dB)')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, loc='upper left')

# Annotate stats box
textstr = f"RMSE = {results['Random Forest']['RMSE']:.3f} dB\nMAE  = {results['Random Forest']['MAE']:.3f} dB\nR²    = {results['Random Forest']['R2']:.4f}"
props = dict(boxstyle='round,pad=0.6', facecolor='#F8F9FA', edgecolor='#BDC3C7', alpha=0.95)
ax.text(0.68, 0.15, textstr, transform=ax.transAxes, fontsize=9.5, verticalalignment='bottom', bbox=props, fontfamily='monospace')

plt.tight_layout()
fig5_path = os.path.join(fig_dir, "fig5_actual_vs_predicted.png")
plt.savefig(fig5_path)
plt.close()
print(f"[+] Saved {fig5_path}")

# -------------------------------------------------------------------------
# FIGURE 6: Residual Diagnostics
# -------------------------------------------------------------------------
residuals = y_test - rf_pred
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.2), dpi=200)

# Residuals vs Fitted
ax1.scatter(rf_pred, residuals, alpha=0.5, color='#2B4C7E', s=25, edgecolors='none')
ax1.axhline(0, color='#E05A47', linestyle='--', linewidth=1.8)
ax1.set_title('(a) Residuals vs. Fitted Values', fontweight='bold')
ax1.set_xlabel('Fitted Values (dB)')
ax1.set_ylabel('Residual (Actual - Fitted, dB)')
ax1.grid(True, linestyle='--', alpha=0.5)

# Residual Distribution Histogram
ax2.hist(residuals, bins=30, density=True, color='#1B8A5A', alpha=0.65, edgecolor='black', linewidth=0.8)
ax2.axvline(0, color='#E05A47', linestyle='--', linewidth=1.8)
ax2.set_title('(b) Probability Density of Residuals', fontweight='bold')
ax2.set_xlabel('Residual Error (dB)')
ax2.set_ylabel('Density')
ax2.grid(True, linestyle='--', alpha=0.5)

plt.suptitle('Figure 5.3: Random Forest Residual Diagnostics (Homoscedasticity & Normality)', fontweight='bold', y=1.02)
plt.tight_layout()
fig6_path = os.path.join(fig_dir, "fig6_residual_analysis.png")
plt.savefig(fig6_path)
plt.close()
print(f"[+] Saved {fig6_path}")

# -------------------------------------------------------------------------
# FIGURE 7: Feature Importance Ranking
# -------------------------------------------------------------------------
rf_model = models['Random Forest']
importances = rf_model.feature_importances_
feature_labels = ['Look Angle', 'Frequency', 'Rain Rate', 'Cloud Water', 'Temperature', 'Humidity']
indices = np.argsort(importances)[::-1]

fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=200)
colors = ['#2B4C7E' if i == 0 else '#3B6EA8' if i == 1 else '#5C8EBF' for i in range(len(features))]
bars = ax.barh(range(len(features)), [importances[i] for i in reversed(indices)], color=colors, edgecolor='black', linewidth=0.8)

ax.set_yticks(range(len(features)))
ax.set_yticklabels([feature_labels[i] for i in reversed(indices)], fontweight='medium')
ax.set_xlabel('Mean Decrease in Impurity (Gini Feature Importance)')
ax.set_title('Figure 5.4: Feature Importance Ranking (Random Forest Ensemble)', fontweight='bold', pad=12)
ax.grid(True, linestyle='--', alpha=0.5, axis='x')

# Value labels on bars
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.008, bar.get_y() + bar.get_height()/2, f"{w*100:.1f}%", va='center', ha='left', fontsize=9, fontweight='bold')

ax.set_xlim(0, max(importances) * 1.15)
plt.tight_layout()
fig7_path = os.path.join(fig_dir, "fig7_feature_importance.png")
plt.savefig(fig7_path)
plt.close()
print(f"[+] Saved {fig7_path}")

print("\n[✓] ALL STATISTICAL FIGURES GENERATED SUCCESSFULLY!")

