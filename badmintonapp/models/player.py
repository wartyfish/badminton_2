from dataclasses import dataclass, field

@dataclass
class Player:
    """Represents a player and their participation statistics.

    Attributes:
        name: The player's name.
        times_played: The total number of sessions the player has participated in.
        times_booked: The total number of sessions the player has booked.
        sessions_booked: A list of datetimes for each session the player booked.
        sessions_played: A list of datetimes for each session the player played in.
        booking_score: A score reflecting the player's booking activity.
    """
    name: str
    times_played: int = 0
    times_booked: int = 0
    sessions_booked: list = field(default_factory=list)
    sessions_played: list = field(default_factory=list)
    
    @property
    def booking_score()

    def reset(self):
        """Resets all statistics to their default values.

        Clears play and booking counts, session history, and booking score.
        The player's name is preserved.
        """
        self.times_played = 0
        self.times_booked = 0
        self.sessions_booked.clear()
        self.sessions_played.clear()
        self.booking_score = 0

