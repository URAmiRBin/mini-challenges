import numpy as np


class Table:
    def __init__(self, input_string, colors):
        self.colors = colors
        self.size = len(input_string)
        self.content = []
        for i in range(self.size):
            self.content.append([])
            for j in range(self.size):
                self.content[i].append(Cell(input_string[i][j][0], input_string[i][j][1]))

    def mrv(self):
        result = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                if self.content[i][j].isFilled():
                    result[i, j] = 10000
                elif self.content[i][j].hasOnlyColor():
                    for n in range(1, self.size + 1):
                        if self.isValid(i, j, Cell(str(n), self.content[i][j].color)):
                            result[i, j] += 1
                elif self.content[i][j].hasOnlyNumber():
                    for c in self.colors:
                        if self.isValid(i, j, Cell(self.content[i][j].number, c)):
                            result[i, j] += 1
                else:
                    for n in range(1, self.size + 1):
                        for c in self.colors:
                            if self.isValid(i, j, Cell(str(n), c)):
                                result[i, j] += 1
        
        return np.argwhere(result == np.min(result))[0]

    def solve(self):
        next = self.mrv()
        
        if self.content[next[0]][next[1]].isFilled():
            return True
        
        if self.content[next[0]][next[1]].hasOnlyColor():
            for n in range(1, self.size + 1):
                if self.isValid(next[0], next[1], Cell(str(n), self.content[next[0]][next[1]].color)):
                    self.content[next[0]][next[1]].number = str(n)

                    # TODO: Forward check here

                    if self.solve():
                        return True
                    else:
                        self.content[next[0]][next[1]].number = "*"
        elif self.content[next[0]][next[1]].hasOnlyNumber():
            for c in self.colors:
                if self.isValid(next[0], next[1], Cell(self.content[next[0]][next[1]].number, c)):
                    self.content[next[0]][next[1]].color = c

                    # TODO: Forward check here

                    if self.solve():
                        return True
                    else:
                        self.content[next[0]][next[1]].color = "#"
        else:
            for c in self.colors:
                for n in range(1, self.size + 1):
                    if self.isValid(next[0], next[1], Cell(str(n), c)):
                        self.content[next[0]][next[1]].color = c
                        self.content[next[0]][next[1]].number = str(n)

                        # TODO: Forward check here

                        if self.solve():
                            return True
                        else:
                            self.content[next[0]][next[1]].color = "#"
                            self.content[next[0]][next[1]].number = "*"

        

        return False
                    
        

    def isSolved(self):
        for row in self.content:
            for cell in row:
                if not cell.isFilled():
                    return False
        return True
                
                        

    def isValid(self, x, y, cell):
        for i in range(self.size):
            if i == x:
                continue
            if cell.number == self.content[i][y].number:
                return False

        for j in range(self.size):
            if j == y:
                continue
            if cell.number == self.content[x][j].number:
                return False

        for n in self.getNeighbors(x, y):
            if cell.color == self.content[n[0]][n[1]].color:
                return False
            
            


        return True

    
    def getNeighbors(self, x, y):
        neighbors = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]

        for n in neighbors:
            if n[0] < 0  or n[0] >= self.size or n[1] < 0 or n[1] >= self.size:
                neighbors.remove(n)

        return neighbors

    def display(self):
        for row in self.content:
            print(row[0].display(),"   ",row[1].display(),"   ",row[2].display(),"   ")


class Cell:
    def __init__(self, number, color):
        self.number = number
        self.color = color

    def display(self):
        return self.number + self.color

    def isFilled(self):
        if self.number != "*" and self.color != "#":
            return True
        return False

    def hasOnlyNumber(self):
        if self.number != "*" and self.color == "#":
            return True
        return False

    def hasOnlyColor(self):
        if self.number == "*" and self.color != "#":
            return True
        return False


def read_input():
    colorCount, dim = input().split(" ")
    colors = input().split(" ")
    
    table = [[] for x in range(int(dim))]
    for i in range(int(dim)):
        table[i] = input().split(" ")

    return colors, table


colors, tableList = read_input()
table = Table(tableList, colors)

table.solve()
table.display()