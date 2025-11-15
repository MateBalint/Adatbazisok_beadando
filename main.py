from plots.plots import PlotBuilder
from report.report import ReportGenerator
from utils.database import Database
from utils.file_system import FileSystem

class Program:
    def __init__(self, file_system: FileSystem, database: Database):
        self.file_system = file_system
        self.database = database
    
    def print_menu_with_options(self):
        print("1 - Clean install")
        print("2 - Osszes panel atlag homersekletehez szukseges plot diagram generalasa.")
        print("3 - Napi atlaghomerseklet - hoterkep plot diagram generalasa")
        print("4 - Adott panel napi min-max-atlag plot diagram generalasa")
        print("5 - Panel - mintavetel + outlierek (TOP 100) plot diagram generalasa")
        print("6 = Panel 1 napi atlaghomerseklet")
        print("0 - Kilepes")
    
    def clean_install(self):
        self.file_system.remove_existing_documents()
        self.database.run_sql_schema_script()
        self.run_reports()
        
    def run_reports(self):
        report_generator = ReportGenerator()
        report_generator.generate_reports()
    
    def main(self):
        plot_builder = PlotBuilder()
        self.file_system.setup_folders()
        
        while True:
            self.print_menu_with_options()
            user_input = int(input("Kerem adja meg szammal a valasztott lehetoseget: "))
            
            if user_input == 0:
                print("A program kilep.")
                break
                
            elif user_input == 1:
                self.clean_install()
            
            elif user_input == 2:
                plot_builder.build_all_daily_average_panel()

            elif user_input == 3:
                plot_builder.build_heatmap_daily_average_panel()

            elif user_input == 4:
                plot_builder.build_panel_1_minmax_band()

            elif user_input == 5:
                plot_builder.build_panel1_outliers()

            elif user_input == 6:
                plot_builder.build_panel_1()

        print("\n" * 2)


if __name__ == "__main__":
    file_system_obj = FileSystem()
    database_obj = Database()
    program = Program(file_system_obj, database_obj)
    program.main()