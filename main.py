from menu.menu import Menu
import os

def main():
    menu = Menu()
    
    
    
    while True:
        menu.print_menu_with_options()
        user_input = int(input("Kerem adja meg szammal a valasztott lehetoseget: "))
        
        if user_input == 0:
            print("A program kilep.")
            break
        
        
        
    

if __name__ == "__main__":
    main()