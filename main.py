import sys
from board import Board
from player import HumanPlayer, RandomPlayer, HeuristicPlayer, ValidWorkerError, OtherWorkerError
from worker import Worker
from factory import WhitePlayerFactory, BluePlayerFactory
from memento import Memento, ConcreteMemento, Caretaker
from copy import deepcopy

class MainCLI:
    """Display a menu for the game and respond to choices when run."""
    def __init__(self, player1, player2, undo_redo, score):
        self._worker_A = Worker('A', 3, 1)
        self._worker_B = Worker('B', 1, 3)
        self._worker_Y = Worker('Y', 1, 1)
        self._worker_Z = Worker('Z', 3, 3)

        self._board = Board(self._worker_A, self._worker_B, self._worker_Y, self._worker_Z)

        if player1 == "human":
            self._white_player = WhitePlayerFactory.create_human_player(self._worker_A, self._worker_B, self._board)
        elif player1 == "random":
            self._white_player = WhitePlayerFactory.create_random_player(self._worker_A, self._worker_B, self._board)
        else:
            self._white_player = WhitePlayerFactory.create_heuristic_player(self._worker_A, self._worker_B, self._board)
        
        if player2 == "human":
            self._blue_player = BluePlayerFactory.create_human_player(self._worker_Y, self._worker_Z, self._board)
        elif player2 == "random":
            self._blue_player = BluePlayerFactory.create_random_player(self._worker_Y, self._worker_Z, self._board)
        else:
            self._blue_player = BluePlayerFactory.create_heuristic_player(self._worker_Y, self._worker_Z, self._board)

        self._current_player = self._white_player
        self._other_player = self._blue_player

        self._turn = 1
        self._undo_redo = undo_redo
        self._score = score

        self._state = self._board
        self._caretaker = Caretaker(self)


    def _display_MainCLI(self):
        """Display the game in terminal"""
        while True:
            print(self._board)
            if self._score:
                self._current_player.calculate_move_score()
                print(f"Turn: {self._turn}, {self._current_player}, ({self._current_player.height_score}, {self._current_player.center_score}, {self._current_player.distance_score})")
            else:
                print(f"Turn: {self._turn}, {self._current_player}")
            
            if self._check_end_of_game():
                break

            if self._undo_redo:
                undo_redo = self._current_player.select_undo_redo()
                if undo_redo == "undo":
                    if self._caretaker.undo():
                        self._update_game(-1)
                    continue
                elif undo_redo == "redo":
                    if self._caretaker.redo():
                        self._update_game(1)
                    continue
                else:
                    self._caretaker.next()

            self._current_player.take_turn()

            self._update_current_player()
            self._turn += 1

    def run(self):
        """Display the main menu and respond to choices."""
        self._display_MainCLI()
    
    def _update_game(self, num):
        """Update the game after an undo or redo"""
        self._board = self._state
        self._board._board_layout = self._state._board_layout
        self._update_board_and_workers()
        self._turn += num
        self._update_current_player()

    def _update_current_player(self):
        """Update the current player after a turn"""
        temp = self._current_player
        self._current_player = self._other_player
        self._other_player = temp
    
    def _check_end_of_game(self):
        """Check if the a player has won"""
        if self._other_player.check_worker_height():
            return True

        if self._current_player.check_possible_moves():
            return True
        
        return False
    
    def _update_board_and_workers(self):
        """Update the board and workers in the Player classes"""
        worker_A = self._board.get_worker("A")
        worker_B = self._board.get_worker("B")

        self._worker_A = worker_A
        self._worker_B = worker_B

        self._white_player.set_workers(worker_A, worker_B)

        worker_Y = self._board.get_worker("Y")
        worker_Z = self._board.get_worker("Z")

        self._worker_Y = worker_Y
        self._worker_Z = worker_Z

        self._blue_player.set_workers(worker_Y, worker_Z)

        self._white_player.set_board(self._board)
        self._blue_player.set_board(self._board)
    
    def save(self) -> Memento:
        """
        Saves the current state inside a memento.
        """

        return ConcreteMemento(deepcopy(self._state))

    def restore(self, memento: Memento):
        """
        Restores the Originator's state from a memento object.
        """

        self._state = memento.get_state()
            

if __name__ == "__main__":
    player1 = "human"
    if len(sys.argv) >= 2:
        player1 = sys.argv[1]
    player2 = "human"
    if len(sys.argv) >= 3:
        player2 = sys.argv[2]
    undo_redo = False
    if len(sys.argv) >= 4:
        if sys.argv[3] == "on":
            undo_redo = True
    score = False
    if len(sys.argv) >= 5:
        if sys.argv[4] == "on":
            score = True
    
    MainCLI(player1, player2, undo_redo, score).run()