import os
import shutil

from constants.file_paths import DB_PATH, OUTPUT_DIR_CSV, OUTPUT_DIR_IMAGES

class FileSystem:
    def setup_folders(self):
        os.makedirs("output", exist_ok=True)
        os.makedirs("output/csv_files", exist_ok=True)
        os.makedirs("output/images", exist_ok=True)
        os.makedirs("backup", exist_ok=True)

    def remove_existing_documents(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

        self.remove_generated_files_from_folder(OUTPUT_DIR_CSV)
        self.remove_generated_files_from_folder(OUTPUT_DIR_IMAGES)

    def remove_generated_files_from_folder(self, path: str):
        for item in os.listdir(path):
            full = os.path.join(path, item)

            if os.path.isfile(full):
                os.remove(full)
            else:
                shutil.rmtree(full)