# Program leírása

- virtuális környezetet használunk a programhoz
  - aktiválás `.venv\Scripts\Activate`
  - `python main.py` parancs futtatása
  - `deactivate` paranccsal lehet deaktiválni a virtuális környezetet
- a requirements.txt tartalmazza az összes package-et a verziókkal amit használunk
- az első futtatás előtt érdemes a `pip install requirements.txt` parancsot futtatni hogy minden package-et telepítsünk
- python 3.14.0 verzióval készült a projekt
- az `output/csv_files` mappába generáódnak ki a lekérdezésekből generált .csv fájlok
- az `output/images` mappába pedig a generált grafikonok kerülnek