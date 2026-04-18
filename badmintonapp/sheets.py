import gspread
from dataclasses import dataclass
from google.oauth2.service_account import Credentials

@dataclass
class Sheets:
    """Container for the Google Sheets worksheets used by the application.
    
    Attributes:
        current_log: The workspace containing the current year's session log.
        initialising_data: The worksheet containing historical session data used 
            to initialise player statistics.
        output_table: The worksheet where computed booking statistics are written.
    """
    current_log: gspread.Worksheet
    initialising_data: gspread.Worksheet
    output_table: gspread.Worksheet
    
def load_sheets(credentials_path) -> Sheets:
    """Authenticates with the Google Sheets API and loads the required worksheets.
    Args:
        credentials_path: Path to a Google service account credentials JSON file.

    Returns:
        A Sheets instance containing the three worksheets needed by the application.

    Raises:
        ValueError: If the credentials file cannot be found or is invalid.
    """
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
       

def read_sessions_from_sheets(log, session_manager) -> None:
    """Reads session data from a worksheet and registers each session.

    Expects the worksheet to have a header row followed by rows where each row
    represents a single session. Columns are read as: date, who booked
    (comma-separated), who played (comma-separated). Blank rows are skipped.

    Args:
        log: A gspread.Worksheet containing session records.
        session_manager: A SessionManager instance that receives each session
            via its new_session method.
    """
    data = log.get_all_values()[1:] # skip header
    rows = [value[0:3] for value in data]
    rows = [row for row in rows if any(cell.strip() for cell in row)]

    for date, booked_str, played_str in rows:
        played = played_str.split(", ") if played_str else []
        booked = booked_str.split(", ") if booked_str else []
    
        session_manager.new_session(date, played, booked)

def update_log_sheet(sheet, session_manager) -> None:
    """Writes the current year's sessions back to the log worksheet.

    Clears the existing data in rows 2 to 1000 of columns A-C, then writes
    one row per 2026 session in chronological order. Each row contains the
    session date, a sorted comma-separated list of who booked, and a sorted
    comma-separated list of who played.

    Args:
        sheet: A gspread.Worksheet to write the session log to.
        session_manager: A SessionManager instance whose sessions provide
            the data to write.
    """
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
    """Writes computed player statistics to the output worksheet.

    Clears columns A-F from row 2 downward, then writes one row per player
    sorted by: most sessions since last booking (descending), then lowest
    bookings-per-session ratio, then most recent booking date. Each row
    contains name, times played, times booked, sessions since last booking,
    bookings per session (rounded to 2 decimal places), and due-to-book status.

    Args:
        sheet: A gspread.Worksheet to write the statistics to.
        player_registry: A player registry whose all() method returns all
            tracked players.
    """
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
    
