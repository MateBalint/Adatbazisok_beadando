from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DB_PATH = ROOT / "data/projekt.db"
OUTPUT_FOLDER_PATH = ROOT / "output"
ADAGOK_PATH = ROOT / "data/Adagok.csv"
PANELEK_PATH = ROOT / "data/Hutopanelek.csv"
OUTPUT_DIR_IMAGES = ROOT / "output/images"
OUTPUT_DIR_CSV = ROOT / "output/csv_files"
DAILY_AVERAGE_CSV = ROOT / "output/csv_files/daily_avg.csv"
DAILY_AVERAGE_OUTPUT = ROOT / "output/images/all_panels_daily_avg.png"
HEATMAP_DAILY_AVERAGE = ROOT / "output/images/heatmap_daily_avg.png"
PANEL_1_DAILY_AVERAGE = ROOT / "output/images/panel1_daily_avg.png"
DAILY_MINMAX_CSV = ROOT / "output/csv_files/daily_minmax.csv"
PANEL_1_MINMAX_BAND = ROOT / "output/images/panel1_minmax_band.png"
PANEL_1_OUTLIERS = ROOT / "output/images/panel1_outliers.png"
SQL_SCHEMA = ROOT / "sql/schema.sql"