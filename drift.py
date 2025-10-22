import pandas as pd

from evidently import Dataset
from evidently import DataDefinition
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset
from evidently.renderers.html_renderers import HTMLRenderer

df_2024 = pd.read_csv("data/ValeursFoncieres-2024.txt.csv")
df_2025 = pd.read_csv("data/ValeursFoncieres-2025-S1.txt.csv")

# Créer un rapport
report = Report([
    DataDriftPreset()
])

# Exécuter le rapport
report.run(reference_data=df_2024, current_data=df_2025)

# Après avoir exécuté report.run(...)
renderer = HTMLRenderer()
renderer.render(report)
renderer.save_html("rapport_drift.html")
quit()

# Sauvegarder le rapport en HTML
html = report.get_html()
with open("data/rapport_drift.html", "w") as f:
    f.write(html)
#report.save_html("data/rapport_drift.html")
