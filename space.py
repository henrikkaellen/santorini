import sys
from worker import Worker

class Space:
    OFFSET_MAP = {'n':[-1, 0], 'ne':[-1, +1], 'e':[0, 1], 'se':[1, 1], 's':[1, 0], 'sw':[1, -1], 'w':[0, -1], 'nw':[-1, -1]}

    def __init__(self, row, col, worker: Worker = None):
        self._height = 0
        self._worker_on_space = worker
        self._row = row
        self._col = col
    
    def __str__(self):
        if self._worker_on_space:
            return f"|{self._height}{self._worker_on_space}"
        else:
            return f"|{self._height} "
    
    def get_worker(self):
        return self._worker_on_space
    
    def get_position(self):
        return [self._row, self._col]
    
    def get_height(self):
        return self._height

    def check_move(self, height):
        if self._height < (height + 2) and self._height < 4 and self._worker_on_space == None:
            return True
        else:
            return False
    
    def check_build(self):
        if self._height < 4 and self._worker_on_space == None:
            return True
        else:
            return False
    
    def update_space_after_move(self, worker):
        """Update the space after a move"""
        self._worker_on_space = worker
        if self._worker_on_space:
            self._worker_on_space.update(self._row, self._col, self._height)
    
    def update_space_after_build(self):
        self._height += 1
