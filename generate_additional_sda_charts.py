import os
import numpy as np
import pandas as pd

os.environ['MPLCONFIGDIR'] = r'C:\Users\HP\.gemini\antigravity\scratch\activity-2\.mplconfig'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig_dir = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\analytics\figures"
os.makedirs(fig_dir, exist_ok=True)

csv_path = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\analytics\dataset\satellite_atmospheric_attenuation.csv"
df = pd.read_csv(csv_path)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12

# -------------------------------------------------------------------------
# FIG 8: SYSTEM ARCHITECTURE BLOCK DIAGRAM
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 4.8), dpi=220)
ax.axis('off')

# Boxes
boxes = [
    ("1. Telemetry Ingestion\n- Weather Station Gauges\n- Satellite Ephemeris\n- Frequency Transceiver", 0.04, 0.55, 0.22, 0.35, "#EBF3FB", "#2B4C7E"),
    ("2. Preprocessing & Hygiene\n- Physical Outlier Filter\n- Range Normalization\n- 80/20 Train/Test Split", 0.29, 0.55, 0.20, 0.35, "#EBF5FB", "#2980B9"),
    ("3. ML Modeling Suite\n- Multiple Linear Regression\n- Ridge Regularization\n- CART Decision Trees\n- Random Forest Ensemble", 0.52, 0.55, 0.22, 0.35, "#E8F8F5", "#16A085"),
    ("4. Evaluation & Export\n- RMSE, MAE, R² Metrics\n- Homoscedasticity\n- JSON Parameter Export", 0.77, 0.55, 0.20, 0.35, "#FEF9E7", "#D4AC0D"),
    ("5. OrbitLink Ground Scheduler & Downlink Engine\nDynamic Bandwidth Scaling (W_eff = W_nominal * η) → 0/1 Knapsack Priority Dispatch", 0.12, 0.10, 0.76, 0.28, "#F5EEF8", "#8E44AD")
]

for title, x, y, w, h, bg, border in boxes:
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", 
                                  facecolor=bg, edgecolor=border, linewidth=2.0)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=9.2, color='#1A252F', fontweight='medium', linespacing=1.3)

# Horizontal Arrows
ax.annotate('', xy=(0.28, 0.725), xytext=(0.26, 0.725), arrowprops=dict(facecolor='#2B4C7E', edgecolor='#2B4C7E', width=2, headwidth=7))
ax.annotate('', xy=(0.51, 0.725), xytext=(0.49, 0.725), arrowprops=dict(facecolor='#2980B9', edgecolor='#2980B9', width=2, headwidth=7))
ax.annotate('', xy=(0.76, 0.725), xytext=(0.74, 0.725), arrowprops=dict(facecolor='#16A085', edgecolor='#16A085', width=2, headwidth=7))

# Downward feedback arrow to scheduler
ax.annotate('', xy=(0.50, 0.38), xytext=(0.87, 0.55), arrowprops=dict(facecolor='#8E44AD', edgecolor='#8E44AD', width=2, headwidth=8))

ax.set_title("Figure 8.1: End-to-End System Architecture and Data Pipeline", fontweight='bold', fontsize=12, pad=15)
plt.tight_layout()
fig8_path = os.path.join(fig_dir, "fig8_system_architecture_diagram.png")
plt.savefig(fig8_path)
plt.close()
print(f"[+] Saved {fig8_path}")

# -------------------------------------------------------------------------
# FIG 9: DECISION TREE RECURSIVE SPLITTING TOPOLOGY
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=220)
ax.axis('off')

# Root Node
ax.text(0.50, 0.88, "Root Node (N=2000)\nRain Rate <= 2.5 mm/hr?\nMSE = 20.8 dB", ha='center', va='center', 
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", edgecolor="#2980B9", lw=2), fontsize=9)

# Level 1 Nodes
ax.text(0.25, 0.60, "Node 1 (Clear/Trace Rain)\nElevation Angle <= 25.0°?\nMSE = 3.4 dB", ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#E8F8F5", edgecolor="#16A085", lw=2), fontsize=8.5)
ax.text(0.75, 0.60, "Node 2 (Active Rain)\nFrequency <= 14.2 GHz?\nMSE = 18.2 dB", ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF9E7", edgecolor="#D4AC0D", lw=2), fontsize=8.5)

# Leaves Level 2
ax.text(0.12, 0.28, "Leaf 1\nHigh Slant Loss\nŷ = 4.2 dB", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", facecolor="#FDEDEC", edgecolor="#E74C3C", lw=1.5), fontsize=8)
ax.text(0.38, 0.28, "Leaf 2\nClear Sky Zenital\nŷ = 0.8 dB", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", facecolor="#EAFAF1", edgecolor="#2ECC71", lw=1.5), fontsize=8)
ax.text(0.62, 0.28, "Leaf 3\nModerate Rain Fade\nŷ = 8.5 dB", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF5E7", edgecolor="#E67E22", lw=1.5), fontsize=8)
ax.text(0.88, 0.28, "Leaf 4\nSevere Ka-Band Fade\nŷ = 22.4 dB", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", facecolor="#FADBD8", edgecolor="#C0392B", lw=1.5), fontsize=8)

# Connectors
ax.plot([0.50, 0.25], [0.80, 0.68], color="#2980B9", lw=1.8)
ax.text(0.35, 0.76, "Yes (<=2.5)", fontsize=8, color="#2980B9", fontweight='bold')
ax.plot([0.50, 0.75], [0.80, 0.68], color="#2980B9", lw=1.8)
ax.text(0.60, 0.76, "No (>2.5)", fontsize=8, color="#C0392B", fontweight='bold')

ax.plot([0.25, 0.12], [0.52, 0.36], color="#16A085", lw=1.5)
ax.plot([0.25, 0.38], [0.52, 0.36], color="#16A085", lw=1.5)
ax.plot([0.75, 0.62], [0.52, 0.36], color="#D4AC0D", lw=1.5)
ax.plot([0.75, 0.88], [0.52, 0.36], color="#D4AC0D", lw=1.5)

ax.set_title("Figure 8.2: Decision Tree (CART) Hierarchical Partitioning Topology", fontweight='bold', pad=15)
plt.tight_layout()
fig9_path = os.path.join(fig_dir, "fig9_decision_tree_topology.png")
plt.savefig(fig9_path)
plt.close()
print(f"[+] Saved {fig9_path}")

# -------------------------------------------------------------------------
# FIG 10: RANDOM FOREST ENSEMBLE BAGGING DIAGRAM
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.8, 4.8), dpi=220)
ax.axis('off')

# Original training data
ax.text(0.12, 0.85, "Telemetry Training Dataset (N=2000)\nFeatures: [El, Freq, Rain, Cloud, Temp, Hum]", ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", edgecolor="#2980B9", lw=2), fontsize=8.5)

# Bootstrap Samples
ax.text(0.12, 0.50, "Bootstrap Resampling\n(With Replacement)\nN = 2000 samples each", ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF9E7", edgecolor="#F39C12", lw=1.8), fontsize=8)

# Arrow from training to bootstrap
ax.annotate('', xy=(0.12, 0.58), xytext=(0.12, 0.76), arrowprops=dict(facecolor='#2980B9', width=1.5, headwidth=6))

# 3 Sample Trees
trees = [
    ("Tree 1 (T_1)\nm = 3 random features\nPrediction: ŷ_1", 0.40, 0.75),
    ("Tree 2 (T_2)\nm = 3 random features\nPrediction: ŷ_2", 0.40, 0.50),
    ("Tree 100 (T_100)\nm = 3 random features\nPrediction: ŷ_100", 0.40, 0.22)
]
for title, tx, ty in trees:
    ax.text(tx, ty, title, ha='center', va='center', bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F8F5", edgecolor="#16A085", lw=1.8), fontsize=8)
    ax.annotate('', xy=(tx - 0.14, ty), xytext=(0.22, 0.50), arrowprops=dict(facecolor='#16A085', width=1.2, headwidth=5))

ax.text(0.40, 0.36, "• • • [B = 100 Bagged Trees] • • •", ha='center', va='center', fontsize=9, fontweight='bold', color='#7F8C8D')

# Aggregation Node
ax.text(0.72, 0.50, "Ensemble Aggregator\nŷ = (1 / 100) * Σ ŷ_b\nVariance Reduced (1/B)", ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F5EEF8", edgecolor="#8E44AD", lw=2), fontsize=8.5)

for _, tx, ty in trees:
    ax.annotate('', xy=(0.60, 0.50), xytext=(tx + 0.12, ty), arrowprops=dict(facecolor='#8E44AD', width=1.2, headwidth=5))

# Final output
ax.text(0.92, 0.50, "Final Output\nPredicted Attenuation\n(R² = 0.9495)", ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#D5F5E3", edgecolor="#27AE60", lw=2), fontsize=8.5)
ax.annotate('', xy=(0.84, 0.50), xytext=(0.80, 0.50), arrowprops=dict(facecolor='#27AE60', width=1.5, headwidth=6))

ax.set_title("Figure 8.3: Random Forest Bootstrap Aggregation (Bagging) Workflow", fontweight='bold', pad=15)
plt.tight_layout()
fig10_path = os.path.join(fig_dir, "fig10_random_forest_ensemble_flow.png")
plt.savefig(fig10_path)
plt.close()
print(f"[+] Saved {fig10_path}")

# -------------------------------------------------------------------------
# FIG 11: 5-FOLD CROSS VALIDATION SPLIT DIAGRAM
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=220)
folds = 5
for i in range(folds):
    for j in range(folds):
        color = '#E05A47' if i == j else '#2B4C7E'
        label_text = 'Validation' if i == j else 'Train'
        rect = patches.Rectangle((j*0.20, (folds - 1 - i)*0.18 + 0.05), 0.18, 0.12, facecolor=color, edgecolor='black', lw=0.8)
        ax.add_patch(rect)
        ax.text(j*0.20 + 0.09, (folds - 1 - i)*0.18 + 0.11, label_text, ha='center', va='center', color='white', fontsize=7.5, fontweight='bold')
    ax.text(-0.02, (folds - 1 - i)*0.18 + 0.11, f"Fold {i+1}:", ha='right', va='center', fontsize=9, fontweight='bold')

ax.set_xlim(-0.15, 1.05)
ax.set_ylim(-0.02, 1.0)
ax.axis('off')
ax.set_title("Figure 13.1: 5-Fold Stratified Cross-Validation Splitting Architecture", fontweight='bold', pad=12)
plt.tight_layout()
fig11_path = os.path.join(fig_dir, "fig11_train_validation_test_split.png")
plt.savefig(fig11_path)
plt.close()
print(f"[+] Saved {fig11_path}")

# -------------------------------------------------------------------------
# FIG 12: CUMULATIVE LOSS EXCEEDANCE DISTRIBUTION (CCDF)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=220)
sorted_att = np.sort(df['signal_attenuation_db'])
ccdf = 1.0 - np.arange(len(sorted_att)) / len(sorted_att)

ax.plot(sorted_att, ccdf * 100, color='#2B4C7E', lw=2.4, label='Empirical Telemetry Observations')
ax.axhline(1.0, color='#E05A47', linestyle='--', lw=1.5, label='99% Availability Threshold (1% Outage)')
ax.axhline(0.1, color='#E67E22', linestyle=':', lw=1.5, label='99.9% Availability Threshold (0.1% Outage)')

ax.set_yscale('log')
ax.set_ylim(0.05, 100)
ax.set_xlabel('Signal Attenuation Threshold (dB)')
ax.set_ylabel('Exceedance Probability P(Loss > A) %')
ax.set_title('Figure 12.8: Complementary Cumulative Distribution Function (CCDF) of Path Loss', fontweight='bold', pad=12)
ax.grid(True, linestyle='--', alpha=0.5, which='both')
ax.legend(frameon=True, loc='upper right')
plt.tight_layout()
fig12_path = os.path.join(fig_dir, "fig12_cumulative_loss_distribution.png")
plt.savefig(fig12_path)
plt.close()
print(f"[+] Saved {fig12_path}")

# -------------------------------------------------------------------------
# FIG 13: BIVARIATE PAIRWISE SCATTER RELATIONSHIPS
# -------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(8.5, 7.0), dpi=220)

axes[0, 0].scatter(df['rain_rate_mm_hr'], df['signal_attenuation_db'], alpha=0.4, color='#2B4C7E', s=18, edgecolors='none')
axes[0, 0].set_xlabel('Rain Rate (mm/hr)')
axes[0, 0].set_ylabel('Signal Attenuation (dB)')
axes[0, 0].set_title('(a) Rain Rate vs. Attenuation', fontweight='bold', fontsize=10)
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].scatter(df['cloud_liquid_water_g_m3'], df['signal_attenuation_db'], alpha=0.4, color='#27AE60', s=18, edgecolors='none')
axes[0, 1].set_xlabel('Cloud Liquid Water (g/m³)')
axes[0, 1].set_ylabel('Signal Attenuation (dB)')
axes[0, 1].set_title('(b) Cloud Liquid Water vs. Attenuation', fontweight='bold', fontsize=10)
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

axes[1, 0].scatter(df['surface_temp_c'], df['signal_attenuation_db'], alpha=0.4, color='#E67E22', s=18, edgecolors='none')
axes[1, 0].set_xlabel('Surface Temperature (°C)')
axes[1, 0].set_ylabel('Signal Attenuation (dB)')
axes[1, 0].set_title('(c) Surface Temperature vs. Attenuation', fontweight='bold', fontsize=10)
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

axes[1, 1].scatter(df['relative_humidity_pct'], df['signal_attenuation_db'], alpha=0.4, color='#8E44AD', s=18, edgecolors='none')
axes[1, 1].set_xlabel('Relative Humidity (%)')
axes[1, 1].set_ylabel('Signal Attenuation (dB)')
axes[1, 1].set_title('(d) Relative Humidity vs. Attenuation', fontweight='bold', fontsize=10)
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.suptitle('Figure 12.9: Pairwise Bivariate Scatter Plots Against Signal Attenuation', fontweight='bold', fontsize=12, y=0.99)
plt.tight_layout()
fig13_path = os.path.join(fig_dir, "fig13_scatter_matrix_bivariate.png")
plt.savefig(fig13_path)
plt.close()
print(f"[+] Saved {fig13_path}")

print("[✓] ALL 6 ADDITIONAL STATISTICAL DIAGRAMS CREATED!")
