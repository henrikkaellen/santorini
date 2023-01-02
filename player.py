
from worker import Worker
import random
from board import Board, ValidDirectionError, ValidMoveError

class ValidWorkerError(Exception):
    pass

class OtherWorkerError(Exception):
    pass

class Player:
    OFFSET_MAP = {'n':[-1, 0], 'ne':[-1, +1], 'e':[0, 1], 'se':[1, 1], 's':[1, 0], 'sw':[1, -1], 'w':[0, -1], 'nw':[-1, -1]}

    def __init__(self, workers, color, board: Board):
        self._workers = workers
        self.color = color

        self._board = board

        self._current_worker = None
        self._move_direction = None
        self._build_direction = None

        self.height_score = 0
        self.center_score = 2
        self.distance_score = 4
    
    def __str__(self):
        return f"{self.color} ({str(self._workers[0])}{str(self._workers[1])})"

    def get_workers(self):
        return self._workers
    
    def check_worker_height(self):
        """Check the height of a worker"""
        for worker in self._workers:
            if worker.check_height():
                print(f"{self.color} has won")
                return True
        
        return False
    
    def set_workers(self, worker1, worker2):
        self._workers = [worker1, worker2]
    
    def set_board(self, board):
        self._board = board

    def check_possible_moves(self):
        """Check if a player still has possible moves for their workers"""
        pos1 = self._workers[0].get_worker_pos()
        pos2 = self._workers[1].get_worker_pos()

        if self._board.find_all_possible_moves(pos1) == [] and self._board.find_all_possible_moves(pos2) == []:
            if self.color == "blue":
                print("white has won")
            else:
                print("blue has won")
            return True
        else:
            return False

    def calculate_move_score(self, pos1 = None, pos2 = None):
        """Caclulate the move score"""
        if pos1 == None and pos2 == None:
            current_pos1 = self._workers[0].get_worker_pos()
            current_pos2 = self._workers[1].get_worker_pos()
        else:
            current_pos1 = pos1
            current_pos2 = pos2

        other_pos = self._board.find_other_workers_pos(self._workers)

        self.height_score = self._board.find_height_score(current_pos1, current_pos2)
        self.center_score = self._board.find_center_score(current_pos1, current_pos2)
        self.distance_score = self._board.find_distance_score([current_pos1, current_pos2], [other_pos[0], other_pos[1]]) 

        return (3*self.height_score + 2*self.center_score + 1*self.distance_score)
    
    def _pick_build(self):
        pos = self._current_worker.get_worker_pos()
        possible_builds_lst = self._board.find_all_possible_builds(pos)

        self._build_direction = random.choice(possible_builds_lst)
        self._board.build(self._build_direction, self._current_worker)

        print(f"{self._current_worker},{self._move_direction},{self._build_direction}")
    
    def select_undo_redo(self):
        undo_redo = input("undo, redo, or next\n")

        return undo_redo

class HumanPlayer(Player):
    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self._type = "human"
    
    def take_turn(self):
        self._select_worker_to_move()
        self._select_move_direction()
        self._select_build_direction()

    def _select_worker_to_move(self):
        while True:
            worker = input("Select a worker to move\n")
            try:
                self._current_worker = self._check_input_worker(worker)
            except ValidWorkerError:
                print("Not a valid worker")
                continue
            except OtherWorkerError:
                print("That is not your worker")
                continue
            break
    
    def _select_move_direction(self):
        while True:
            move_direction = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            try:
                self._board.move(move_direction, self._current_worker)
            except ValidDirectionError:
                print("Not a valid direction")
                continue
            except ValidMoveError:
                print(f"Cannot move {move_direction}")
                continue
            break
    
    def _select_build_direction(self):
        while True:
            build_direction = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            try:
                self._board.build(build_direction, self._current_worker)
            except ValidDirectionError:
                print("Not a valid direction")
                continue
            except ValidMoveError:
                print(f"Cannot build {build_direction}")
                continue
            break

    def _check_input_worker(self, worker_name):
        if worker_name not in ["A", "B", "Y", "Z"]:
            raise(ValidWorkerError)
        
        for worker in self._workers:
            if str(worker) == worker_name:
                return worker
        raise(OtherWorkerError)

class RandomPlayer(Player):
    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self._type = "random"
    
    def take_turn(self):
        self._current_worker = self._pick_player()
        self._pick_move()
        self._pick_build()

    def _pick_player(self):
        pos1 = self._workers[0].get_worker_pos()
        if self._board.find_all_possible_moves(pos1) == []:
            return self._workers[1]
        
        pos2 = self._workers[1].get_worker_pos()
        if self._board.find_all_possible_moves(pos2) == []:
            return self._workers[0]

        return random.choice(self._workers)
    
    def _pick_move(self):
        pos = self._current_worker.get_worker_pos()
        possible_moves_lst = self._board.find_all_possible_moves(pos)

        self._move_direction = random.choice(possible_moves_lst)
        self._board.move(self._move_direction, self._current_worker)


class HeuristicPlayer(Player):
    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self._type = "heuristic"
    
    def take_turn(self):
        pos1 = self._workers[0].get_worker_pos()
        pos2 = self._workers[1].get_worker_pos()

        distance1 = -1

        possible_moves_lst = self._board.find_all_possible_moves(pos1)
        for item in possible_moves_lst:
            val = Player.OFFSET_MAP[item]
            pos = [(pos1[0] + val[0]), (pos1[1] + val[1])]
            distance = self.calculate_move_score(pos, pos2)
            if distance1 == -1 or distance1 < distance:
                distance1 = distance
                direction1 = item
        
        distance2 = -1

        possible_moves_lst = self._board.find_all_possible_moves(pos2)
        for item in possible_moves_lst:
            val = Player.OFFSET_MAP[item]
            pos = [(pos2[0] + val[0]), (pos2[1] + val[1])]
            distance = self.calculate_move_score(pos1, pos)
            if distance2 == -1 or distance2 < distance:
                distance2 = distance
                direction2 = item
        
        if distance1 > distance2:
            self._move_direction = direction1
            self._current_worker = self._workers[0]
        else:
            self._move_direction = direction2
            self._current_worker = self._workers[1]
        
        self._board.move(self._move_direction, self._current_worker)
        self._pick_build()