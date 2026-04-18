import os
import sheets
import time
from pathlib import Path


#from session_manager import SessionManager

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    path_to_credentials = Path(r"badminton_credentials.json")
    clear()
    print("Fetching data from Google Sheets... ")
    print("Success")
    time.sleep(1)
    clear()

if __name__ == "__main__":
    main()
