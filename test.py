from cmath import inf
import math
from random import randint, sample

class Vertex:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.__getattribute__
        self.visited = False
        self.g = inf
        self.parent = None
        self.h = 0
        self.f = inf
        self.neighbors = []

    def equals(self, cmp):
        if(self.x == cmp.x and self.y == cmp.y):
            #print("x1 = " + str(self.x) + "x2 = " + str(cmp.x) + "y1 = " + str(self.y) + "y2 = " + str(cmp.y))
            return True
        return False

class PriorityQueue:
    def __init__(self):
        self.queue = []
        
    #performs insertion sort on the queue, ascending
    def insertionSort(self):
        for i in range(len(self.queue)):
            minValue = inf
            minIdx = -1
            for j in range(len(self.queue)):
                if(self.queue[j].f < minValue):
                    minValue = self.queue[j].f
                    minIdx = j
            #print(i)
            #print(minValue)
            temp = self.queue[i]
            self.queue[i] = self.queue[minIdx]
            self.queue[minIdx] = temp
    
    #inserts the given vertex into the queue after assigning its f-value. calls insertion sort
    def insert(self, vertex, f):
        vertex.f = f
        for i in range(len(self.queue)):
            if(self.queue[i].equals(vertex)):
                
                self.queue[i] = vertex
                return True
           
        
        self.queue.append(vertex)
        if(len(self.queue) > 1):
            self.insertionSort()
        return True

    #return the head of the queue
    def pop(self):
        return self.queue.pop(0)

    #returns true if the queue is empty, false otherwise
    def isEmpty(self):
        if(len(self.queue) == 0):
            return True
        return False

    def printQueue(self):
        for vertex in self.queue:
            print("(" + str(vertex.x) + ", " + str(vertex.y) + ")" + ". g = " + str(vertex.g) + ". h = " + str(vertex.h) + ". f = " + str(vertex.f))
        print("\n")

class CellTable:

    #set path to None, i couldnt get it to read the file
    def __init__(self, xSize, ySize, path):
        if(path == None):
            self.xSize = xSize
            self.ySize = ySize
            self.table = [ [ False for y in range(ySize)]  for x in range(xSize)]
            self.blockRandomTiles()
            self.generateStartAndGoal()
        else:
            lines = []
            f = open(path)
            ctr = 0
            for i in f:
                if(len(i) < 1):
                    break
                if(ctr == 0):
                    tempX = int(i[0:1])
                    tempY = int(i[2])
                    self.startVertex = Vertex(tempX - 1, tempY - 1)
                    
                elif(ctr == 1):
                    tempX = int(i[0:1])
                    tempY = int(i[2])
                    self.goalVertex = Vertex(tempX - 1, tempY - 1)
                elif(ctr == 2):
                    self.xSize = int(i[0:1])
                    self.ySize = int(i[2])
                    self.table = [ [ False for y in range(ySize)]  for x in range(xSize)]
                elif(len(i) > 4 and i[4] == "1"):
                    
                    tempX = int(i[0:1])
                    tempY = int(i[2])
                    print("(" + str(tempX-1) + ", " + str(tempY-1) + ")")
                    self.table[tempX-1][tempY-1] = True
                
                ctr = ctr + 1
            f.close()


        self.generateVertexGrid()
        self.populateNeighbors()

    #will perfom the A* search. returns the goal node on success, false on failure
    def AStar(self):
        self.assignHValues()
        self.fringe = PriorityQueue()
        self.closed = []
        currentVertex = self.startVertex
        currentVertex.g = 0
        currentVertex.parent = currentVertex
        self.fringe.insert(currentVertex, currentVertex.g + currentVertex.f)
        while(not self.fringe.isEmpty()):
            currentVertex = self.fringe.pop()
            #print("current: " + "(" + str(currentVertex.x) + ", " + str(currentVertex.y) + ")")
            
            if(currentVertex.equals(self.goalVertex)):
                return currentVertex
            self.closed.append(currentVertex)
            for child in currentVertex.neighbors:
                if(not child in self.closed):
                    self.updateVertex(currentVertex, child)
        return False

    #determines if the child should be added to the fringe, and if so, sets the g, f, and parent values
    def updateVertex(self,current, child):
        if(current.g + self.cost(current, child) < child.g):
            child.g = current.g +self.cost(current, child)
            child.parent = current
            self.fringe.insert(child, child.g + child.h)

            

    #calculates and returns distance between vertices, simple distance formula, returns the distance
    def cost(self, v1, v2):
        ret = math.sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)
        return ret

    #assigns every vertex its h value
    def assignHValues(self):
        for row in self.vertexGrid:
            for current in row:
                firstTerm = math.sqrt(2) * min(abs(current.x - self.goalVertex.x), abs(current.y - self.goalVertex.y))
                secondTerm = max(abs(current.x - self.goalVertex.x), abs(current.y - self.goalVertex.y))
                thirdTerm = min(abs(current.x - self.goalVertex.x), abs(current.y - self.goalVertex.y))
                current.h = firstTerm +secondTerm - thirdTerm

    #prints the path A* took, from the goal node back up to start node. For use, have A* return into this, like printPath(AStar())
    def printPath(self, node):
        if(node == False):
            return
        parent = node.parent
        if node.equals(parent):
            return
        print("(" + str(node.x) + ", " + str(node.y) + "). g = " + str(node.g) + ". h = " + str(node.h) + ". f = " + str(node.f))
        if not node.equals(parent):
            self.printPath(parent)


    #will generate the text file needed based on the 'table' stored
    #@param desiredPath string with the path and file name desired
    def generateTextFile(self, desiredPath):
        f = open(desiredPath, "w+")
        point = str(self.startVertex.x) + " " + str(self.startVertex.y) + "\n"
        f.write(point)
        point = str(self.goalVertex.x) + " " + str(self.goalVertex.y) + "\n"
        f.write(point)
        dem = str(self.xSize) + " " + str(self.ySize) +"\n"
        f.write(dem)
        for i in range(self.xSize):
            for j in range(self.ySize):
                point = str(i) + " " + str(j) + " "
                f.write(point)
                if(self.table[i][j]):
                    f.write("1\n")
                else:
                    f.write("0\n")
        f.close()

    #performs DFS search via recursion. assumes vertexGrid is initialized
    #@vertex the current node being inspected, MUST INPUT StartVertex WHEN CALLING
    #@return true if it successfully finds the GoalVertex, false otherwise
    def DFS(self, vertex):
        if(vertex.equals(self.goalVertex)):
            return True
        vertex.visited = True
        children = vertex.neighbors
        for child in children:
            if(child.visited):
                continue
            recursed = self.DFS(child)
            if(recursed == True):
                return True
        return False
    #used by DFS, resets visted values
    def clearVisits(self):
        for row in self.vertexGrid:
            for vertex in row:
                vertex.visited = False

    #generates the representation based around the vertices, opposed to the cells
    #saves it to self.vertexGrid, no return
    def generateVertexGrid(self):
        grid = []
        for i in range(self.xSize +1):
            row = []
            for j in range(self.ySize + 1):
                
                if(self.startVertex.x == i and self.startVertex.y == j):
                    
                    row.append(self.startVertex)
                elif(self.goalVertex.x == i and self.goalVertex.y == j):
                    row.append(self.goalVertex)
                else:
                    tempVertex = Vertex(i, j)
                    row.append(tempVertex)
            grid.append(row)
        self.vertexGrid = grid

    #adds all immediately accessable neighbors to each vertex's "neighbor" list, which will be a list of Vertex
    def populateNeighbors(self):
        
        for row in self.vertexGrid:
            for vertex in row:
                potentialNeighbors = self.getPossibleNeighbors(vertex)
                #print("(" + str(vertex.x) + ", " + str(vertex.y) + ")")
                for neighbor in potentialNeighbors:
                   
                    if(not self.isPathBlocked(vertex, neighbor)):
                        
                        
                        vertex.neighbors.append(neighbor)


    #checks if a path is blocked between two adjacent vertices. 
    #translating between the vertex table and the cell table was annoying, and i may have messed up
    #but i believe that, when you consider a square with four vertices, the lowest, leftmost vertex's indices
    #should correspond with that cell's indices on the boolean table. for example, a cell constructed as such
    #(3,3), (4,3)
    #(3,2), (4,2)
    #self.table[3][2] should be the corresponding boolean value, with true meaning blocked
    #if i mess this up lmk
    def isPathBlocked(self, v1, v2):
        xDif = v1.x - v2.x
        yDif = v1.y - v2.y
        if(xDif == 0 and yDif == 0):
            return False
        if(xDif * yDif != 0):
            cellCoordX = min(v1.x, v2.x)
            cellCoordY = min(v1.y, v2.y)
            if(self.table[cellCoordX][cellCoordY] == True):
                return True
            return False
        elif(xDif == 0):
            if(v1.x != 0):
                if(not (self.table[v1.x - 1][min(v1.y, v2.y)])):
                    return False
            if(not v1.x >= len(self.table)):
                #print("guh")
                #print(yDif)
                #print(v2.y)
                #print(str(v1.y))
                if(not (self.table[v1.x][min(v1.y, v2.y)])):
                    return False
            return True
        else:
            if(v1.y != 0):
                if(not self.table[min(v1.x, v2.x)][v1.y - 1] ):
                    return False
            if(v1.y <len(self.table[min(v1.x, v2.x)])):
                if(not self.table[min(v1.x, v2.x)][v1.y]):
                    return False
            return True

    


    #determines which other vertices are neighbors with the given vertex, ignoring whether or not theyre blocked
    #@return a list of vertices that could be neighbors
    def getPossibleNeighbors(self, vertex):
        ret = []
        #print("the vertex = (" + str(vertex.x) + ", " + str(vertex.y) + ")")
        for i in range(-1, 2):
            #print(i)
            if(vertex.x + i < 0 or vertex.x + i >= len(self.vertexGrid)):
                continue
            for j in range(-1,2):
                if(i == j and i == 0):
                    continue
                if(vertex.y + j < 0 or vertex.y + j >= len(self.vertexGrid[i])):
                    continue
                #print(len(self.vertexGrid[i]))
                #print(str(vertex.x + i) + "    " + str(vertex.y + j))
                ret.append(self.vertexGrid[vertex.x + i][vertex.y + j])
        return ret

    #driver function to generate startVertex and goalVertex
    def generateStartAndGoal (self) :
        start = self.generateVertex()
        goal = self.generateVertex()
        while(start.equals(goal)):
            start = self.generateVertex()
            goal = self.generateVertex()
        self.startVertex = start
        self.goalVertex = goal

    #blocks random tiles by choosing random numbers from 0-totalCells, then converting that number to an index
    def blockRandomTiles (self):
        
        amountToBlock = math.floor(self.xSize * self.ySize * .1)
        totalCells = int(self.xSize)* int(self.ySize)
        
        toBlock = sample(range(totalCells), amountToBlock)
        for i in toBlock:
            x = i % self.xSize
            print(i)
            y = math.floor(i / self.xSize)
            print("(" + str(x) + ", " + str(y) + ")")
            
            self.table[x][y] = True



    #used to generate the start and goal vertices, ensures they aren't blocked to begin with
    def generateVertex(self) :
        tempX = randint(0, self.xSize)
        tempY = randint (0, self.ySize)
        ret = Vertex(tempX, tempY)
        while(self.isVertexBlocked(ret)):
               tempX = randint(0, self.xSize)
               tempY = randint (0, self.ySize)
               ret = Vertex(tempX, tempY)
        return ret
        

    #checks if there is any legal way to reach v
    def isVertexBlocked (self, v):
        for i in range(-1,2):
            if( v.x + (i) < 0 or v.x + (i) > (self.xSize - 1)):
                continue
            for j in range(-1,2):
                #print("i = " + str(i) + ". j = " + str(j) + ".v.x = " + str(v.x) + ".v.y = " + str(v.y) +"\n")
                if(v.y + (j) < 0 or v.y + (j) >(self.ySize-1)):
                    continue
                if(not self.table[v.x+i][v.y+j]):
                    return False
        return True 



#all of this was just me testing various portions
tbl = CellTable(4,3, "qwerty.txt")
ar = tbl.table
print("start = (" + str(tbl.startVertex.x) + ", " + str(tbl.startVertex.y) + ")")
print("goal = (" + str(tbl.goalVertex.x) + ", " + str(tbl.goalVertex.y) + ")")
for i in ar:
    for j in i:
        print(j, end = ', ')
    print('\n')

print("start nodes neighbors:")
for i in tbl.startVertex.neighbors:
    print("(" + str(i.x) + ", " + str(i.y) + ")")
tbl.clearVisits()
print("DFS result: " + str(tbl.DFS(tbl.startVertex)))


tbl.printPath(tbl.AStar())
