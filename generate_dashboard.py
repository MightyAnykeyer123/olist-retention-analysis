import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# Load pre-aggregated data
df_csat = pd.read_csv('delivery_csat_summary.csv')
df_cat = pd.read_csv('top_churn_categories.csv')

# Handle missing category names safely
df_cat['category_name'] = df_cat['category_name'].fillna('Uncategorized').astype(str)

# Create 16:9 canvas
fig = plt.figure(figsize=(16, 9), facecolor='#F8F9FA')
gs = fig.add_gridspec(3, 2, height_ratios=[0.22, 0.78, 0.02], hspace=0.35, wspace=0.25)

# --- HEADER: KPI CARDS ---
ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.axis('off')

kpis = [
    ("TOTAL CUSTOMERS", "93,358", "#1E293B", "Baseline Delivered Cohort"),
    ("REPEAT PURCHASE RATE", "3.00%", "#0F766E", "97% Single-Order Churn"),
    ("ON-TIME CSAT", "4.29 / 5.0", "#15803D", "6.6% 1-Star Review Rate"),
    ("LATE DELIVERY CSAT", "2.27 / 5.0", "#B91C1C", "53.7% 1-Star Review Rate (8.1x Surge)")
]

for idx, (title, val, col, sub) in enumerate(kpis):
    x_pos = 0.02 + idx * 0.25
    rect = FancyBboxPatch((x_pos, 0.05), 0.22, 0.90, transform=ax_kpi.transAxes,
                          facecolor='white', edgecolor='#E2E8F0',
                          boxstyle="round,pad=0.02,rounding_size=0.03", lw=1.2)
    ax_kpi.add_patch(rect)
    ax_kpi.text(x_pos + 0.11, 0.72, title, transform=ax_kpi.transAxes,
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#64748B')
    ax_kpi.text(x_pos + 0.11, 0.42, val, transform=ax_kpi.transAxes,
                ha='center', va='center', fontsize=18, fontweight='heavy', color=col)
    ax_kpi.text(x_pos + 0.11, 0.18, sub, transform=ax_kpi.transAxes,
                ha='center', va='center', fontsize=8, color='#94A3B8')

# --- VISUAL 1: CSAT BY DELIVERY PERFORMANCE ---
ax1 = fig.add_subplot(gs[1, 0])
palette = {'On-Time / Early': '#0284C7', 'Late': '#EF4444'}
sns.barplot(data=df_csat, x='review_score', y='order_count', hue='delivery_performance',
            palette=palette, ax=ax1, edgecolor="none", alpha=0.9)

ax1.set_title("Customer Review Score Distribution by Timeliness", fontsize=13, fontweight='bold', pad=12, color='#1E293B')
ax1.set_xlabel("Review Score (1 = Worst, 5 = Best)", fontsize=10.5, color='#475569')
ax1.set_ylabel("Delivered Orders", fontsize=10.5, color='#475569')
ax1.legend(title="Fulfillment SLA", frameon=True, facecolor='white', framealpha=0.9)

# --- VISUAL 2: TOP 10 CHURN CATEGORIES ---
ax2 = fig.add_subplot(gs[1, 1])
df_cat_sorted = df_cat.sort_values('pct_1_star_reviews', ascending=True)

clean_names = df_cat_sorted['category_name'].apply(lambda x: str(x).replace('_', ' ').title())
bars = ax2.barh(clean_names, df_cat_sorted['pct_1_star_reviews'], color='#F97316', edgecolor='none', height=0.65)

# Highlight top risk in red
bars[-1].set_color('#DC2626')

for bar in bars:
    w = bar.get_width()
    ax2.text(w + 0.3, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", 
             va='center', ha='left', fontsize=8.5, fontweight='bold', color='#334155')

ax2.set_title("Top 10 High-Risk Categories (1-Star Review %)", fontsize=13, fontweight='bold', pad=12, color='#1E293B')
ax2.set_xlabel("% of Orders Receiving 1-Star Review (Min. 500 Orders)", fontsize=10.5, color='#475569')
ax2.set_xlim(0, 25)

plt.tight_layout()
plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight')
print("Dashboard generated successfully: executive_dashboard.png")
