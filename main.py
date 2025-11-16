from plots.plots import PlotBuilder
from report.report import ReportGenerator
from utils.database import Database
from utils.file_system import FileSystem

class Program:
    def __init__(self, file_system: FileSystem, database: Database):
        self.file_system = file_system
        self.database = database
    
    def print_menu_with_options(self):
        print("\n")
        print("1 - Clean install")
        print("2 - Összes panel átlaghőmérsékletéhez szükséges plot diagram generálása.")
        print("3 - Napi átlaghőmérséklet - hőtérkép plot diagram generálása")
        print("4 - Adott panel napi min-max-átlag plot diagram generálása")
        print("5 - Panel - mintavétel + outlierek (TOP 100) plot diagram generálása")
        print("6 = Panel 1 napi átlaghőmérséklet")
        print("0 - Kilépés")
        print("\n")
    
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
            user_input = int(input("Kérem adja meg számmal a választott lehetőséget: "))
            print("\n")
            
            if user_input == 0:
                print("A program kilép.")
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