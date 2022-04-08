from point import Point

class Hamiltonian():
    # ------------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------------
    def __init__(self, px, py, width, height, snake):
        self.COLS = width
        self.ROWS = height
        self.snake = snake
        self.POINT_COUNT = self.COLS * self.ROWS - len(snake)

        self.path = [None] * self.POINT_COUNT   # array of POINT_COUNT size, will store Point(s)
        self.path[0] = Point(px, py)

        # Each element will store a list of connected points
        # j represents column (i.e.x) and i represents row (i.e. y)
        # indexing will be as => connected[row][col]
        self.connected = [[None for j in range(self.COLS)] for i in range(self.ROWS)]

        # now build connections
        self.buildConnections()

    # ------------------------------------------------------------------------
    # print path
    # ------------------------------------------------------------------------
    def printPath(self):
        for i in range(len(self.path)):
            if self.path[i] is not None:
                print(self.path[i].toString(), ' ', end='')
            else:
                print('(None) ', end='')

        print('')

    # ------------------------------------------------------------------------
    # build connections
    # ------------------------------------------------------------------------
    def buildConnections(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if (i, j) not in self.snake:
                    self.connected[i][j] = self.getConnectedPoints(j, i)

    # ------------------------------------------------------------------------
    # print connections
    # ------------------------------------------------------------------------
    def printConnections(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.connected[i][j]:
                    self.connected[i][j] = self.getConnectedPoints(j, i)

    # ------------------------------------------------------------------------
    # buildPath recursive method
    # ------------------------------------------------------------------------
    def buildPath(self, pos):
        print('buildPath => pos: ', pos)
        self.printPath()

        if pos == self.POINT_COUNT:
            # are these two points connected, if yes then we got the solution
            p = self.path[pos-1]
            if p is not None and self.isConnected(p.px, p.py, self.path[0].px, self.path[0].py):
                return True

            return False

        # Process all the points except the one added in the path
        for row in range(self.ROWS):
            for col in range(self.COLS):
                # either it is not a nod or it is the self node, then ignore it
                if self.connected[row][col] is None or self.path[0].py == row and self.path[0].px == col:
                    continue

                p = Point(row, col)
                if self.isConnectedPending(col, row, pos):
                    self.path[pos] = p

                    if self.buildPath(pos + 1):
                        return True

                    self.path[pos] = None

        return False

    # ------------------------------------------------------------------------
    # isConnectedPending()
    # Check if new point is adjacent to the previous point, and it is not processed already
    # ------------------------------------------------------------------------
    def isConnectedPending(self, px, py, pos):
        # if not connected then return
        if (self.path[pos-1] is not None and self.isConnected(px, py, self.path[pos-1].px, self.path[pos-1].py) == False):
            return False

        # Is it already processed
        for i in range(pos):
            if self.path[i] is not None and self.path[i].px == px and self.path[i].py == py:
                return False

        return True

    # are these two points adjacent to each other?
    def isConnected(self, x1, y1, x2, y2):
        print('isConnected =>', (x1, y1), (x2, y2))
        points = self.connected[y1][x1]
        if points is not None:
            print('Connected points of: ', ())
            for i in range(len(points)):
                print(points[i].toString(), ' ', end='')
                if points[i].px == x2 and points[i].py == y2:
                    print('')
                    return True
            print('')

        return False

    # Get connected points in horizontal and vertical directions
    # don't consider points occupied by the snake
    def getConnectedPoints(self, px, py):
        points = []
        rowMoves = []
        colMoves = []

        #Check for columns
        if px == 0:
            # Only Right move
            colMoves.append(1)
        elif px == self.COLS - 1:
            # Only Left move
            colMoves.append(-1)
        else:
            # Left and Right both
            colMoves.append(1)
            colMoves.append(-1)

        # Check for rows
        if py == 0:
            # Down move
            rowMoves.append(1)
        elif py == self.ROWS - 1:
            # Up move
            rowMoves.append(-1)
        else:
            # Up and Down both
            rowMoves.append(1)
            rowMoves.append(-1)

        for i in range(len(rowMoves)):
            rowDir = rowMoves[i]
            if (px, py+rowDir) not in self.snake:
                points.append(Point(px, py+rowDir))

        for i in range(len(colMoves)):
            colDir = colMoves[i]
            if (px+colDir, py) not in self.snake:
                points.append(Point(px+colDir, py))

        return points
