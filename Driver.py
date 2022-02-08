import Search
import Generator

def generateDriver():
    xSize = int(input("input X dimension (positive int): "))
    ySize = int(input("input Y dimension (positive int): "))
    quantity = int(input("input quantity of files to generate(positive int): "))
    desiredPath = input("enter desired path, note that the file they are from 0 to quantity-1 and '.txt' will be appended: ")
    Generator.generate(xSize, ySize, quantity, desiredPath)

def searchDriver():
    pathToFile = input("input the path to the file containing the grid to search on: ")
    searchTable = Search.CellTable(pathToFile)
    print("Start Vertex = (" + str(searchTable.startVertex.x) + ", " + str(searchTable.startVertex.y) + ")")
    print("Goal Vertex = (" + str(searchTable.goalVertex.x) + ", " + str(searchTable.goalVertex.y) + ")")
    searchType = int(input("which search would you like to perform? For A*, enter 1: "))
    if(searchType == 1):
        AStarDriver(searchTable)
    else:
        print("Error")


def AStarDriver(searchTable):
    goal = searchTable.AStar()
    if (goal == False):
        print("Unable to complete AStar")
        return
    path = []
    child = goal
    parent = child.parent
    path.append(child)
    while(not parent.equals(child)):
        path.append(parent)
        child = parent
        parent = parent.parent
    path.reverse()
    for vertex in path:
        print("(" + str(vertex.x) + ", " + str(vertex.y) + "). g = " + str(vertex.g) + ". h = " + str(vertex.h) + ". f = " + str(vertex.f))
    print("total cost = " + str(path[-1].g))






isGenerating = input("would you like to generate grid files(y/n): ")
if (isGenerating.lower() == "y"):
   
    generateDriver()
    searchDriver()
elif (isGenerating.lower() == "n"):
    searchDriver()
else:
    print("Error")


