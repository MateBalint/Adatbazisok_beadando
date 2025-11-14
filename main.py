from menu.menu import Menu
import os

class Program:
    def setup_folders(self):
        os.makedirs("output", exist_ok=True)
        os.makedirs("output/csv_files", exist_ok=True)
        os.makedirs("output/images", exist_ok=True)
        os.makedirs("backup", exist_ok=True)
    
    def main(self):
        self.setup_folders()
        
        
        
        menu = Menu()
        
        
        
        while True:
            menu.print_menu_with_options()
            user_input = int(input("Kerem adja meg szammal a valasztott lehetoseget: "))
            
            if user_input == 0:
                print("A program kilep.")
                break
        
        
        
    

if __name__ == "__main__":
    program = Program()
    program.main()