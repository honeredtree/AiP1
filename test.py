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
        
    def clearVisits(self):
        for row in self.vertexGrid:
            for vertex in row:
                vertex.visited = False
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

    def populateNeighbors(self):
        for row in self.vertexGrid:
            for vertex in row:
                potentialNeighbors = self.getPossibleNeighbors(vertex)
                for neighbor in potentialNeighbors:
                    #print((neighbor.x))
                    if(not self.isPathBlocked(vertex, neighbor)):
                        vertex.neighbors.append(neighbor)



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


    def generateStartAndGoal (self) :
        start = self.generateVertex()
        goal = self.generateVertex()
        while(start.equals(goal)):
            start = self.generateVertex()
            goal = self.generateVertex()
        self.startVertex = start
        self.goalVertex = goal

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

    def generateVertex(self) :
        tempX = randint(0, self.xSize)
        tempY = randint (0, self.ySize)
        ret = Vertex(tempX, tempY)
        while(self.isVertexBlocked(ret)):
               tempX = randint(0, self.xSize)
               tempY = randint (0, self.ySize)
               ret = Vertex(tempX, tempY)
        return ret
        

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
