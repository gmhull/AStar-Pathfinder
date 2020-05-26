import numpy as np
import cv2
import math

class Square(object):
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.isWall = False
        # Sets a percentage of the squares to be walls at random
        if np.random.rand(1) < 0.5:
            self.isWall = True
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self,other):
        # We evaluate whether squares are equivalent based on their positioning
        return self.position == other.position

def createBoard(length,squares,start,end):
    # Create the start and end squares, make sure they arent walls
    start = Square(None, start)
    start.isWall = False
    start.g=start.h=start.f=0
    end = Square(None, end)
    end.isWall = False
    end.g=end.f=end.h=0

    # create the board with a white background
    board = np.zeros((length,length,3),np.uint8)
    squareLength = length / squares
    board = cv2.rectangle(board,(0,0),(length,length),(255,255,255),-1)
    count = 0
    walls = []
    for row in range(squares):
        for col in range(squares):
            # create a square for each grid location on the board
            r = Square(None,(row,col))
            # Color the start blue
            if r == start:
                board = cv2.rectangle(board,(int(row*squareLength),int(col*squareLength)),
                                    (int(row*squareLength + squareLength),int(col*squareLength + squareLength)),(255,100,100),-1)
                count += 1
            # Color the end red
            elif r == end:
                board = cv2.rectangle(board,(int(row*squareLength),int(col*squareLength)),
                                    (int(row*squareLength + squareLength),int(col*squareLength + squareLength)),(100,100,255),-1)
                count += 1
            # Draw a thin black border around the open squares
            elif r.isWall == False:
                board = cv2.rectangle(board,(int(row*squareLength),int(col*squareLength)),
                                    (int(row*squareLength + squareLength),int(col*squareLength + squareLength)),(0,0,0),1)
                count += 1
            # Draw the walls in black
            elif r.isWall == True:
                board = cv2.rectangle(board,(int(row*squareLength),int(col*squareLength)),
                                    (int(row*squareLength + squareLength),int(col*squareLength + squareLength)),(0,0,0),-1)
                count += 1
                # Keep track of the walls
                walls.append(r)
    if count == squares**2:
        print("Made the board")
        return board, walls, start, end

def findPath(board, walls, squares, start, end):
    openSet = []
    closedSet = []
    openSet.append(start)
    print("starting to find path")
    while openSet:
        currentNode = openSet[0]
        currentIndex = 0
        # Look through openSet to find the square with the greatest f value
        for index, node in enumerate(openSet):
            if node.f < currentNode.f:
                currentNode = node
                currentIndex = index
        openSet.pop(currentIndex)
        closedSet.append(currentNode)

        children = []
        if currentNode == end:
            print("Found the end")
            path = []
            current = currentNode
            # If we are at the end, look at the squares parents to find the optimal path
            while current is not None:
                path.append(current.position)
                current = current.parent
            # This returns the ideal path through the maze, excluding the start and end points
            return path[-2:0:-1]

        # look through all of the squares around the current square
        for newPosition in [(1,1),(1,0),(0,1),(1,-1),(-1,1),(0,-1),(-1,0),(-1,-1)]:
            nodePosition = (currentNode.position[0]+newPosition[0],currentNode.position[1]+newPosition[1])

            # Check to see if the new position is in the board
            if nodePosition[0] > (squares-1) or nodePosition[0] < 0 or nodePosition[1] > (squares-1) or nodePosition[1] < 0:
                continue

            # If an adjacent square passes the two tests, make it a child of the currentNode
            newNode = Square(currentNode, nodePosition)

            # If the currentNode is a wall, ignore it and move on
            if newNode in walls:
                continue

            children.append(newNode)

        for child in children:
            # If the child is in closedSet, we skip it
            if child in closedSet:
                continue

            # Heuristic takes the euclidian distance to select the square closest to the end
            child.g = currentNode.g + 1
            child.h = math.dist((child.position[0],child.position[1]),(end.position[0],end.position[1]))
            child.f = child.g + child.h

            # Dont think that this is the cleanest way to do this but I think it works
            # If the child is in openSet and its g value is greater than openNode, add it to closed set
            # Then check again to see if the child is in closedSet, and pass if it is
            for openNode in openSet:
                if child == openNode and child.g > openNode.g:
                    closedSet.append(child)
            if child in closedSet:
                continue
                
            # If the child passes the above tests, add it to open set
            openSet.append(child)

def drawSearch(board,squareLength,path):
    # This function takes the path that was calculated and draws it out on the board
    for square in path:
        board = cv2.rectangle(board,(int(square[0]*squareLength+ squareLength/4),int(square[1]*squareLength+squareLength/4)),
                            (int(square[0]*squareLength + 3*squareLength/4),int(square[1]*squareLength + 3*squareLength/4)),(255,255,0),-1)
    return board

def run(length,squares):
    squareLength = length/squares
    start = (0,0)
    end = (squares-1,squares-1)
    board, walls, start, end = createBoard(length,squares,start,end)
    try:
        path = findPath(board,walls,squares,start,end)
        print(path)
        board = drawSearch(board,squareLength,path)
    except:
        print('There is no solution to this puzzle')

    cv2.imshow('Howdy',board)
    cv2.waitKey(0)

if __name__ == "__main__":
    run(500,50)
