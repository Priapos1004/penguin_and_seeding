import os
import pandas as pd
import matplotlib.pyplot as plt

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

# Daten sammeln
all_dfs = []

for csv_file, label in csv_info.items():
    path = os.path.join(base_dir, csv_file)
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {path}")
        continue
    except Exception as e:
        print(f"Fehler beim Lesen von {path}: {e}")
        continue
    
    df['strategy'] = df['strategy'].fillna("None").astype(str)
    df['summary_percent_covered'] = pd.to_numeric(df['summary_percent_covered'], errors='coerce')
    
    # Nur relevante Seeds und Strategien
    df = df[df['seed'].isin([42, 43, 44, 45, 46])]
    df = df[df['strategy'].isin(['None', 'tree_traverse'])]

    df['category'] = label
    all_dfs.append(df)

# Kombinieren
combined_box_df = pd.concat(all_dfs)

# Umbenennen für Lesbarkeit
strategy_names = {
    'None': 'No Seeding',
    'tree_traverse': 'Tree Traverse'
}
combined_box_df['strategy'] = combined_box_df['strategy'].map(strategy_names)

# Boxplot erzeugen (nur dieser Plot!)
fig, ax = plt.subplots(figsize=(10, 6))  # Größere Box, schmaler

# Boxplot horizontal
box = ax.boxplot(
    [
        combined_box_df[combined_box_df['strategy'] == 'No Seeding']['summary_percent_covered'],
        combined_box_df[combined_box_df['strategy'] == 'Tree Traverse']['summary_percent_covered']
    ],
    tick_labels=['No Seeding', 'Tree Traverse'],
    patch_artist=True,
    vert=False
)

# Farben
colors = ['lightcoral', 'steelblue']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

for median in box['medians']:
    median.set_color('black')
    median.set_linewidth(2)

for flier in box['fliers']:
    flier.set(marker='o', markersize=5, alpha=0.5)

# Achsentitel etc.
ax.set_title('Distribution of Test Coverage by Strategy', fontsize=14, pad=15)
ax.set_xlabel('Mean Coverage [%]', fontsize=12)
ax.set_xlim(0, 100)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()

# Speichern
output_path = os.path.join(base_dir, "coverage_boxplot.png")
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Boxplot gespeichert unter: {output_path}")
