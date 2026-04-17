import gspread
from dataclasses import dataclass
from google.oauth2.service_account import Credentials

@dataclass
class Sheets:
    current_log: gspread.Worksheet
    initialising_data: gspread.Worksheet
    output_table: gspread.Worksheet
    
def load_sheets(credentials_path) -> Sheets:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    try:
        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    except Exception as e:
        raise ValueError("Credentials could not be validated", e)
    client = gspread.authorize(creds)

    book = client.open("Badminton Session Log")

    return Sheets(
        current_log=book.worksheet("2026 Log"),
        initialising_data=book.worksheet("2025 Log"),
        output_table=book.worksheet("Booking Stats")
    )
       

# reads data from gspread.Worksheet objects
# each row contains info from a different session
# data from each session is passed individually to session_manager
def read_sessions_from_sheets(log, session_manager) -> None:
    data = log.get_all_values()[1:] # skip header
    rows = [value[0:3] for value in data]
    rows = [row for row in rows if any(cell.strip() for cell in row)]

    for date, booked_str, played_str in rows:
        played = played_str.split(", ") if played_str else []
        booked = booked_str.split(", ") if booked_str else []
    
        session_manager.new_session(date, played, booked)

def update_log_sheet(sheet, session_manager) -> None:
    sheet.batch_clear(["A2:C1000"])

    rows = []
    for s in session_manager.sessions_chronological:
        if s.date_datetime.year == 2026:
            rows.append([
                s.date,
                ", ".join(sorted([p.name for p in s.who_booked])),
                ", ".join(sorted([p.name for p in s.who_played]))
            ])
        
    sheet.update("A2", rows)
    
    print("Log updated successfully")

def update_processed_sheet(sheet, player_registry) -> None:
    rows = []

    for player in sorted(
        player_registry.all(), 
        key=lambda p: (-1* p.sessions_since_last_booking, p.bookings_per_session, p.most_recent_booking)
    ):
        rows.append([
            player.name,
            player.times_played,
            player.times_booked,
            player.sessions_since_last_booking,
            round(player.bookings_per_session, 2),
            player.due_to_book
        ])
    
    print("Processed updated successfully")
    
    sheet.batch_clear(["A2:F"])   
    sheet.update(values=rows, range_name="A2")
    
