from models.session import Session
from player_registry import PlayerRegistry

class SessionManager:
    """Manages a collection of sessions and player statistics
    
    Attributes:
        registry: A player registry used to look up or create players by name.
        sessions: A list of all sessions manaaged by this instance.
    """
    def __init__(self, registry: PlayerRegistry):
        self.registry = registry
        self.sessions: list[Session] = []

    @property
    def chronological(self):
        return sorted(self.session, key=lambda s: s.date_datetime)
    
    @property
    def is_most_recent_session_booked(self):
        return bool(self.sessions_reverse_chronological[0].who_booked)
    
    def new_session(self, date: str, players: list, bookers: list = None) -> Session:
        """Generates a new session object from raw session data.

        Takes player names and session booker names as lists of strings and 
        converts to lists of Player objects. New players automatically generated.
        Bookers may be optional. 
        Player stats not updated here. 

        Args:
            date: String representation of session date.
            players: List of player names.
            bookers: List of player names who booked the session (optional). 
        """
        if not bookers:
            bookers = []

        p = [self.registry.get_or_create(name) for name in players]
        b = [self.registry.get_or_create(name) for name in bookers]

        session = Session(date, p, b)


    def update_player_stats(self, registry: PlayerRegistry, session: Session):
        """Updates player stats with session data.

        Args:
            registry: registry containing Player objects
            session: session data (date of session, who played, who booked (optional)) 
        """
        for p in registry.players:
            registry.players[p]