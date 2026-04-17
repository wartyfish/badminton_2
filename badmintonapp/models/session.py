import datetime
from dataclasses import dataclass, field

@dataclass
class Session:
    date: str
    players: list
    bookers: list = field(default_factory=list)
    date_datetime: datetime.datetime = field(init=False)

    def __post_init__(self):
        try:
            self.date_datetime = datetime.datetime.strptime(self.date, "%d/%m/%y")
        except ValueError:
            print("ValueError: failed to assign datetime for session {date}")
            self.date_datetime = datetime.datetime.min

    def __str__(self):
        booked = ", ".join(p.name for p in self.bookers) if self.bookers else "N/A"
        played = ", ".join(p.name for p in self.players)
        
        return (
            f"Date: {self.date}\n"
            f"Booked by: {booked}\n"
            f"Players: {played}"
        )
    

        