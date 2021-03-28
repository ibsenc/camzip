class Queue:
    """a queue class using a Python
    list as its implementation"""
    def __init__(self):
        self.items = []

    def __str__(self):
        return self.items.__str__()

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        if len(self.items) == 0:
            return True
        else:
            return False
