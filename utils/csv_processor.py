import pandas as pd

class CsvProcessor:
    """
    Class that contains all the functionalities needed to process the .csv files.
    """
    @staticmethod
    def read_chunks(file_path: str, chunk_size: int):
        """
        Reads the given .csv file.
        """
        try:
            for chunk in pd.read_csv(file_path, chunksize=chunk_size, sep=';', skip_blank_lines=True):
                yield chunk

        except Exception as e:
            print(f"Error happened during processing of CSV file. Cause of error: {e}")