import os

import matplotlib.pyplot as plt
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

# Gesamtdaten sammeln
all_data = []

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
    
    # Daten vorbereiten
    df['strategy'] = df['strategy'].fillna("None").astype(str)
    df['summary_percent_covered'] = pd.to_numeric(df['summary_percent_covered'], errors='coerce')
    
    # Nur relevante Seeds und Strategien
    df = df[df['seed'].isin([42, 43, 44, 45, 46])]
    df = df[df['strategy'].isin(['None', 'tree_traverse'])]
    
    # Daten für Gesamtmittelwert sammeln
    all_data.append(df)

# Alle Daten kombinieren
combined_df = pd.concat(all_data)

# Gesamtmittelwert je Strategie berechnen
total_means = combined_df.groupby('strategy')['summary_percent_covered'].mean().reset_index()

# Umbenennen für bessere Lesbarkeit
strategy_names = {
    'None': 'No Seeding',
    'tree_traverse': 'Tree Traverse'
}
total_means['strategy'] = total_means['strategy'].map(strategy_names)

# Sortierung für horizontale Balken (Tree Traverse oben)
total_means = total_means.sort_values('strategy', ascending=True)

# Diagramm erstellen (horizontal)
plt.figure(figsize=(10, 5))
bars = plt.barh(
    total_means['strategy'],
    total_means['summary_percent_covered'],
    color=['lightcoral', 'steelblue'],
    height=0.6
)

# Werte anzeigen
for bar in bars:
    width = bar.get_width()
    plt.text(
        width - 3, 
        bar.get_y() + bar.get_height()/2, 
        f'{width:.2f}%',
        ha='right', 
        va='center',
        color='white',
        fontweight='bold',
        fontsize=12
    )

# Diagramm anpassen
plt.title('Mean Coverage of total Test Suite', fontsize=14)
plt.xlabel('Mean Coverage [%]', fontsize=12)
plt.xlim(0, 100)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()

# Diagramm speichern
output_path = os.path.join(base_dir, "coverage_total_testsuite.png")
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Plot gespeichert unter: {output_path}")