import os
import subprocess
import csv
import io

def get_miseq_metrics_via_cli(run_folder_path, interop_bin_dir):
    """
    run_folder_path: Pfad zum MiSeq Laufordner
    interop_bin_dir: Pfad zum entpackten 'bin' Ordner der Illumina CLI Tools
    """
    exe_path = "C:\\Users\\dule\\Downloads\\interop-1.9.0-Windows-MSVC\\interop-1.9.0-Windows-MSVC\\bin\\index-summary.exe"
    
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"index-summary.exe nicht gefunden unter: {exe_path}")

    # Führt das Illumina Tool im Hintergrund aus und holt die Daten als CSV-String
    result = subprocess.run(
        [exe_path, run_folder_path, "--csv"], 
        capture_output=True, 
        text=True, 
        check=True
    )
    
    # Parser für die CSV-Ausgabe des Tools
    csv_data = io.StringIO(result.stdout)
    reader = csv.DictReader(csv_data)
    
    # Wir holen uns die Werte der ersten Lane/Kachel (Standard-Zusammenfassung)
    for row in reader:
        # Hinweis: Die genauen Spaltennamen siehst du in der result.stdout
        # Meistens: 'Yield (Gb)', 'Cluster Density (K/mm2)', '% >= Q30'
        return {
            "Yield_GB": float(row.get("Yield (Gb)", 0)),
            "Cluster_Density_Kmm2": float(row.get("Cluster Density (K/mm2)", 0)),
            "Percent_Q30": float(row.get("% >= Q30", 0))
        }

# Morgen im Labor zum Testen:
# cli_tools = r"C:\Pfad\zu\deinem\entpackten\InterOp\bin"
# run_path = r"C:\Pfad\zu\einem\MiSeq_Laufordner"
# print(get_miseq_metrics_via_cli(run_path, cli_tools))