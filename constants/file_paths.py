from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DB_PATH = ROOT / "data/projekt.db"
ADAGOK_PATH = ROOT / "data/Adagok.csv"
PANELEK_PATH = ROOT / "data/Hutopanelek.csv"
OUTPUT_DIR_IMAGES = ROOT / "output/images"
OUTPUT_DIR_CSV = ROOT / "output/csv_files"
DAILY_AVERAGE_CSV = ROOT / "output/csv_files/daily_avg.csv"
DAILY_AVERAGE_OUTPUT = ROOT / "out/images/all_panels_daily_avg.png"
HEATMAP_DAILY_AVERAGE = ROOT / "out/images/heatmap_daily_avg.png"
PANEL_1_DAILY_AVERAGE = ROOT / "out/images/panel1_daily_avg.png"
DAILY_MINMAX_CSV = ROOT / "output/csv_files/daily_minmax.csv"
PANEL_1_MINMAX_BAND = ROOT / "out/images/panel1_minmax_band.png"
PANEL_1_OUTLIERS = ROOT / "out/images/panel1_outliers.png"