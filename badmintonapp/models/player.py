import datetime
from dataclasses import dataclass

@dataclass
class Participant:
    name: str
    times_played = 0
    times_booked = 0
    sessions_book = []
    sessions_played = []
    booking_score = []