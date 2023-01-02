from space import Space
from worker import Worker

class ValidDirectionError(Exception):
    pass

class ValidMoveError(Exception):
    pass

class Board:

    OFFSET_MAP = {'n':[-1, 0], 'ne':[-1, +1], 'e':[0, 1], 'se':[1, 1], 's':[1, 0], 'sw':[1, -1], 'w':[0, -1], 'nw':[-1, -1]}

    def __init__(self, worker_A, worker_B, worker_Y, worker_Z):
        self._board_layout = [[Space(0,0), Space(0,1), Space(0,2), Space(0,3), Space(0,4)],
        [Space(1,0), Space(1,1,worker_Y), Space(1,2), Space(1,3,worker_B), Space(1,4)],
        [Space(2,0), Space(2,1), Space(2,2), Space(2,3), Space(2,4)],
        [Space(3,0), Space(3,1,worker_A), Space(3,2), Space(3,3,worker_Z), Space(3,4)], 
        [Space(4,0), Space(4,1), Space(4,2), Space(4,3), Space(4,4)]]
    
    def __str__(self):
        ret_str = ""
        for row in self._board_layout:
            ret_str += "+--+--+--+--+--+\n"
            for col in row:
                ret_str += str(col)
            ret_str += "|\n"
        ret_str += "+--+--+--+--+--+"
        
        return ret_str
    
    def _check_input_exceptions(self, move, possible_moves_lst):
        """Check if a move or build is valid"""
        if move not in Board.OFFSET_MAP:
            raise(ValidDirectionError)
        if move not in possible_moves_lst:
            raise(ValidMoveError)

    def find_all_possible_moves(self, pos):
        """Find all possible moves for a given position"""
        possible_moves = []

        height = self._board_layout[pos[0]][pos[1]].get_height()

        for key, val in Board.OFFSET_MAP.items():
            row, col = (pos[0] + val[0]), (pos[1] + val[1])
            if row >= 0 and row <= 4 and col >= 0 and col <= 4 and self._board_layout[row][col].check_move(height) and self.find_all_possible_builds([row, col]) != None:
                possible_moves.append(key)
        
        return possible_moves
    
    def find_all_possible_builds(self, pos):
        """Find all possible builds for a given position"""
        possible_builds = []

        for key, val in Board.OFFSET_MAP.items():
            row, col = (pos[0] + val[0]), (pos[1] + val[1])
            if row >= 0 and row <= 4 and col >= 0 and col <= 4 and self._board_layout[row][col].check_build():
                possible_builds.append(key)
        
        return possible_builds
    
    def move(self, move, worker):
        """Move a worker"""
        pos = worker.get_worker_pos()
        possible_moves_lst = self.find_all_possible_moves(pos)

        self._check_input_exceptions(move, possible_moves_lst)

        self._board_layout[pos[0]][pos[1]].update_space_after_move(None)

        row, col = (pos[0] + Board.OFFSET_MAP[move][0]), (pos[1] + Board.OFFSET_MAP[move][1])

        self._board_layout[row][col].update_space_after_move(worker)
    
    def build(self, build, worker):
        """Build after a move"""
        pos = worker.get_worker_pos()
        possible_moves_lst = self.find_all_possible_builds(pos)

        self._check_input_exceptions(build, possible_moves_lst)

        row, col = (pos[0] + Board.OFFSET_MAP[build][0]), (pos[1] + Board.OFFSET_MAP[build][1])

        self._board_layout[row][col].update_space_after_build()
    
    def find_height_score(self, pos1, pos2):
        height1 = self._board_layout[pos1[0]][pos1[1]].get_height()
        height2 = self._board_layout[pos2[0]][pos2[1]].get_height()

        return (height1 + height2)
    
    def find_center_score(self, pos1, pos2):
        score1 = self._check_center(pos1)
        score2 = self._check_center(pos2)

        return (score1 + score2)
    
    def find_distance_score(self, current_pos_lst, other_pos_lst):
        min_distance1 = self._find_distance(other_pos_lst[0], current_pos_lst)
        min_distance2 = self._find_distance(other_pos_lst[1], current_pos_lst)
        
        return (8 - (min_distance1 + min_distance2))
    
    def _find_distance(self, other_pos, current_pos_lst):
        min_distance = -1
        for current_pos in current_pos_lst:
            distance = max(abs(current_pos[0] - other_pos[0]), abs(current_pos[1] - other_pos[1]))
            if min_distance == -1 or min_distance > distance:
                min_distance = distance
        
        return min_distance
    
    def _check_center(self, pos):
        """Check if a worker is in the center"""
        if [pos[0], pos[1]] == [2, 2]:
            return 2
        elif [pos[0], pos[1]] in [[1,1], [1,2], [1,3], [2,1], [2,3], [3,1], [3,2], [3,3]]:
            return 1
        else:
            return 0
    
    def find_other_workers_pos(self, current_workers):
        """Find the positions of the other player's workers"""
        pos = []
        for row in self._board_layout:
            for space in row:
                if space.get_worker() != None and space.get_worker() not in current_workers:
                    pos.append(space.get_position())
        
        return pos

    def get_worker(self, name):
        for row in self._board_layout:
            for space in row:
                if str(space._worker_on_space) == name:
                    return space._worker_on_space