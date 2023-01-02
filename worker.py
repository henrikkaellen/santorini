
class Worker:
    def __init__(self, name, row, col):
        self._name = name
        self._row = row
        self._col = col
        self._height = 0
    
    def __str__(self):
        return self._name
    
    def get_worker_pos(self):
        return [self._row, self._col]
    
    def get_worker_row(self):
        return self._row
    
    def get_worker_col(self):
        return self._col
    
    def update(self, row, col, height):
        self._row = row
        self._col = col
        self._height = height
    
    def get_worker_height(self):
        return self._height

    def check_height(self):
        return self._height == 3
    
    def check_center(self):
        if [self._row, self._col] == [2, 2]:
            return 2
        elif [self._row, self._col] in [[1,1], [1,2], [1,3], [2,1], [2,3], [3,1], [3,2], [3,3]]:
            return 1
        else:
            return 0