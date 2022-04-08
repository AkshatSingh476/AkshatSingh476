class Point():
    def __init__(self, px, py, prevPoint=None):
        self.px = px
        self.py = py
        self.prevPoint = prevPoint

    def toString(self):
        return (self.px, self.py)

    def print(self):
        print(self.toString())