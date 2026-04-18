from models.player import Player

class PlayerRegistry:
    """A registry for looking up and managing Participant objects by name.

    Attributes:
        players: A dictionary of player name: Player objects
    """
    def __init__(self):
        self.players: dict[str, Player] = {}

    def find(self, name: str) -> Player | None:
        """Returns named Player obj if they exist 
        
        Args:
            name: Player name string    
        """
        return self.player.get(name)

    def get_or_create(self, name: str) -> Player:
        """Returns named Player obj. Creates new player if they don't yet exist.
        """
        if name not in self._players:
            self._players[name] = Player(name)
        
        return self.players[name]
    
    def record_session_played(self, name: str) -> None:
        """Updates"""


