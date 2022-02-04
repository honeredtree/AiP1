import math
from random import randint, sample

class Vertex:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        visited = False
        self.neighbors = []

    def equals(self, cmp):
        if(self.x == cmp.x and self.y == cmp.y):
            return True
        return False


class CellTable:
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.table = [ [ False for y in range(ySize)]  for x in range(xSize)]
        self.blockRandomTiles()
        self.generateStartAndGoal()
        self.generateVertexGrid()
        self.populateNeighbors()

    #will generate the text file needed based on the 'table' stored
    #@param desiredPath string with the path and file name desired
    def generateTextFile(self, desiredPath):
        f = open(desiredPath, "w+")
        point = str(self.startVertex.x) + " " + str(self.startVertex.y) + "\n"
        f.write(point)
        point = str(self.goalVertex.x) + " " + str(self.goalVertex.y) + "\n"
        f.write(point)
        dem = str(self.xSize) + " " + str(self.ySize) +"\n"
        f.write(point)
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
                for neighbor in potentialNeighbors:
                    #print((neighbor.x))
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
        #print(amountToBlock)
        totalCells = self.xSize * self.ySize
        toBlock = sample(range(totalCells), amountToBlock)
        for i in toBlock:
            x = math.floor(i / self.xSize)
            y = i % self.xSize
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
        for i in range(3):
            if( v.x + (i-1) < 0 or v.x + (i-1) > (self.xSize - 1)):
                continue
            for j in range(3):
                #print("i = " + str(i) + ". j = " + str(j) + ".v.x = " + str(v.x) + ".v.y = " + str(v.y) +"\n")
                if(v.y + (j-1) < 0 or v.y + (j-1) >(self.ySize-1)):
                    continue
                if(self.table[v.x+i-1][v.y+j-1]):
                    return False
        return True 



#all of this was just me testing various portions
tbl = CellTable(10,10)
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

tbl.generateTextFile("qwerty.txt")
