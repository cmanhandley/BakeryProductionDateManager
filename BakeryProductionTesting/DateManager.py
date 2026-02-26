import json
from collections import deque

class InventoryQueue:
    def __init__(self, name, shelf_life, queue_list):
        self.name = name
        self.shelf_life = shelf_life
        self.queue = deque(queue_list, maxlen=shelf_life)
        self.pulled_today = 0

    def add_today(self, amount):
        if len(self.queue) == self.shelf_life:
            self.pulled_today = self.queue.popleft()
        else:
            self.pulled_today = 0

        self.queue.append(amount)

    def to_json(self):
        return json.dumps(list(self.queue))
