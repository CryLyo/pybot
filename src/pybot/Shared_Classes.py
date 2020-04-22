"""
Contains DataContainer class for centralized data storage over all cogs.
Contains Queue class
TODO: Actually read in the data
"""

import json

class Queue:
    def __init__(self, id: str or int):
        self.id = id

        self.queue = []
        self.first = None
        self.last = None
        self.current_index = 0

    @property
    def length(self):
        return len(self.queue)
    def __len__(self):
        return len(self.queue)

    @property
    def current(self):
        if self.length == 0:
            return None
        return self.queue[self.current_index]
    @property
    def next(self):
        if self.current_index == self.length - 1:
            return None
        return self.queue[self.current_index + 1]
    @property
    def previous(self):
        if self.current_index == 0:
            return None
        return self.queue[self.current_index - 1]

    def add(self,*items):
        for item in items:
            if self.length == 0:
                self.first = item
                self.current_index = 0

            self.queue.append(item)
            self.last = item
        return self

    def __next__(self):
        if self.next:
            self.current_index += 1
            return self.current


class DataContainer:
    def __init__(self):
        self.settings = {"TOKEN": "BEST_NOT_ON_GITHUB"} # Will add in file reading in a bit
        self.queues = []

data = DataContainer()
