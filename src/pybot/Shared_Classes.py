"""
Contains DataContainer class for centralized data storage over all cogs.
Contains Queue class
TODO: Actually read in the data
"""

import json

class Queue:
    global instances
    instances = {}
    def __init__(self, owner: int, message_id: int, guild: str):
        self.owner = owner
        self.message_id = message_id
        self.guild = guild
        instances[message_id] = self
        self.queue = []
        self.current_index = 0

    @staticmethod
    def get_queue_by_message(message_id):
        if message_id in instances:
            return instances[message_id]
        return None
    @staticmethod
    def remove_queue_by_message(message_id):
        instances.pop(message_id,None)

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
        if self.current_index >= self.length - 1:
            return None
        return self.queue[self.current_index + 1]
    @property
    def previous(self):
        if self.current_index == 0:
            return None
        return self.queue[self.current_index - 1]
    @property
    def first(self):
        if self.length == 0:
            return None
        return self.queue[0]

    @property
    def last(self):
        if self.length == 0:
            return None
        return self.queue[-1]

    def add(self,*items):
        for item in items:
            if not item:
                continue
            if self.length == 0:
                self.current_index = 0
            self.queue.append(item)
        return self

    def cut_after_current(self):
        if self.length == 0:
            return None
        toreturn = self.queue[self.current_index+1:]
        self.queue = self.queue[:self.current_index+1]
        return toreturn

    def cut_after_next(self):
        if self.length == 0 or not self.next:
            return None
        toreturn = self.queue[self.current_index+2:]
        self.queue = self.queue[:self.current_index+2]
        return toreturn

    def clear(self):
        self.queue = []
        self.current_index = 0

    def __next__(self):
        if self.next:
            self.current_index += 1
            return self.current
        return None


class DataContainer:
    def __init__(self):
        self.settings = {
            "TOKEN":"FILL IN HERE",
            "Guilds":
            {
                "A":487731226820476935
            }
        } # Will add in file reading in a bit
        self.queues = {"A": [], "B": []}
        self.waiting_queues = {"A": Queue(0,0,"A"), "B": Queue(1,1,"B")}
        self.messages = {}

data = DataContainer()
