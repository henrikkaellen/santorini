from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits
from board import Board
from copy import deepcopy
import pdb


class Memento(ABC):
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """

    @abstractmethod
    def get_name(self) -> str:
        pass


class ConcreteMemento(Memento):
    def __init__(self, state):
        self._state = state

    def get_state(self):
        """
        The Originator uses this method when restoring its state.
        """
        return self._state

    def get_name(self):
        """
        The rest of the methods are used by the Caretaker to display metadata.
        """

        return f"{self._state}"



class Caretaker():
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """

    def __init__(self, originator) -> None:
        self._mementos = []
        self._redos = []
        self._originator = originator

    def backup(self):
        self._mementos.append(self._originator.save())

    def undo(self):
        if not len(self._mementos):
            return False
        
        self._redos.append(self._originator.save())
        memento = self._mementos.pop()
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()
        
        return True
    
    def redo(self):
        if not len(self._redos):
            return False
        
        self._mementos.append(self._originator.save())
        redo = self._redos.pop()
        try:
            self._originator.restore(redo)
        except Exception:
            self.redo()
        
        return True
    
    def next(self):
        self.backup()
        self._redos = []
