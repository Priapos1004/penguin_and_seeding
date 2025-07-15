import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# CSV-Dateien und ihre Kurzbezeichnungen
csv_info = {
    "in_func_coverage_reports.csv": "in_func",
    "len_func_coverage_reports.csv": "len_func",
    "str_comp_func_coverage_reports.csv": "str_comp",
    "str_with_func_coverage_reports.csv": "str_with",
    "mixed_func_coverage_reports.csv": "mixed"
}

# Basisverzeichnis
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evaluations")

# Ergebnisse sammeln
data = []

for csv_file, label in csv_info.items():
    path = os.path.join(base_dir, csv_file)
    df = pd.read_csv(path)
    df['strategy'] = df['strategy'].fillna("None").astype(str)
    df['summary_percent_covered'] = pd.to_numeric(df['summary_percent_covered'], errors='coerce')
    
    # Mittelwert je Seed und Strategie
    grouped = df.groupby(['seed', 'strategy'])['summary_percent_covered'].mean().reset_index()
    
    # Mittelwert je Strategie
    means = grouped.groupby('strategy')['summary_percent_covered'].mean()
    
    data.append({
        'label': label,
        'no_seeding': means.get('None', 0),
        'tree_traverse': means.get('tree_traverse', 0)
    })

# In DataFrame umwandeln
summary_df = pd.DataFrame(data)

# Balkendiagramm erzeugen
x = np.arange(len(summary_df['label']))  # Positionen
width = 0.35

fig, ax = plt.subplots(figsize=(10, 5))

bars1 = ax.bar(x - width/2, summary_df['no_seeding'], width, label='no_seeding', color='lightcoral')
bars2 = ax.bar(x + width/2, summary_df['tree_traverse'], width, label='tree_traverse', color='steelblue')

# Beschriftung je Balken
for bar in bars1 + bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height:.1f}%', 
            ha='center', va='bottom', fontsize=9)

# Achsentitel und Labels

# Titel mit mehr Abstand zum Plot
ax.set_title('Mean Coverage by Strategy over Categories', pad=20)

# Legende weiter rechts außerhalb des Plots platzieren
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax.set_ylabel('Mean Coverage [%]')
ax.set_xlabel('Category')
ax.set_title('Mean Coverage by Strategy over Categories')
ax.set_xticks(x)
ax.set_xticklabels(summary_df['label'])
ax.set_ylim(0, 100)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()

# Speichern
output_path = os.path.join(base_dir, "coverage_by_category.png")
plt.savefig(output_path)
plt.show()

print(f"Plot gespeichert unter: {output_path}")
