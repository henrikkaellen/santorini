from player import HumanPlayer, RandomPlayer, HeuristicPlayer

class PlayerFactory:
    """Abstract Factory for creating blue and white player"""
    def create_human_player():
        pass

    def create_random_player():
        pass

    def create_heuristic_player():
        pass

class WhitePlayerFactory(PlayerFactory):
    def create_human_player(worker1, worker2, board):
        return HumanPlayer([worker1, worker2], "white", board)
    
    def create_random_player(worker1, worker2, board):
        return RandomPlayer([worker1, worker2], "white", board)
    
    def create_heuristic_player(worker1, worker2, board):
        return HeuristicPlayer([worker1, worker2], "white", board)

class BluePlayerFactory(PlayerFactory):
    def create_human_player(worker1, worker2, board):
        return HumanPlayer([worker1, worker2], "blue", board)
    
    def create_random_player(worker1, worker2, board):
        return RandomPlayer([worker1, worker2], "blue", board)
    
    def create_heuristic_player(worker1, worker2, board):
        return HeuristicPlayer([worker1, worker2], "blue", board)