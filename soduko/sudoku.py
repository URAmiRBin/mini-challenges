import numpy as np


class Table:
    def __init__(self, input_string, colors):
        self.colors = colors
        self.size = len(input_string)
        self.content = []
        self.domains = [[[] for x in range(self.size)] for y in range(self.size)]
        for i in range(self.size):
            self.content.append([])
            for j in range(self.size):
                self.content[i].append(Cell(input_string[i][j][0], input_string[i][j][1]))

        for i in range(self.size):
            for j in range(self.size):
                if self.content[i][j].isFilled():
                    self.domains[i][j] = -1
                elif self.content[i][j].hasOnlyColor():
                    for n in range(1, self.size + 1):
                        if self.isValid(i, j, Cell(str(n), self.content[i][j].color)):
                            self.domains[i][j].append(Cell(str(n), self.content[i][j].color))
                elif self.content[i][j].hasOnlyNumber():
                    for c in self.colors:
                        if self.isValid(i, j, Cell(self.content[i][j].number, c)):
                            self.domains[i][j].append(Cell(self.content[i][j].number, c))
                else:
                    for n in range(1, self.size + 1):
                        for c in self.colors:
                            if self.isValid(i, j, Cell(str(n), c)):
                                self.domains[i][j].append(Cell(str(n), c))
        
    
    def mrv(self):
        min_index = [0, 0]
        min_val = 10000
        remaining_values = [[0 for x in range(self.size)] for y in range(self.size)]
        for i in range(len(self.domains)):
            for j in range(len(self.domains[i])):
                if self.domains[i][j] == -1:
                    remaining_values[i][j] = 1000
                else:
                    remaining_values[i][j] = len(self.domains[i][j])
                if remaining_values[i][j] < min_val:
                    if remaining_values[i][j] == 0:
                        return [-1, -1]
                    min_val = remaining_values[i][j]
                    min_index[0] = i
                    min_index[1] = j
        return min_index

    def updateDomains(self,x , y, cell):
        self.domains[x][y] = -1
        for i in range(self.size):
            if self.domains[i][y] == -1:
                continue
            else:
                for domain in self.domains[i][y]:
                    if not self.isValid(i, y, domain):
                        self.domains[i][y].remove(domain)
        
        for j in range(self.size):
            if self.domains[x][j] == -1:
                continue
            else:
                for domain in self.domains[x][j]:
                    if not self.isValid(x, j, domain):
                        self.domains[x][j].remove(domain)

        for i in range(self.size):
            for j in range(self.size):
                if self.domains[i][j] == -1:
                    continue
                if len(self.domains[i][j]) == 0:
                    return False
        
        return True
    
    def solve(self):
        next = self.mrv()
        
        if self.content[next[0]][next[1]].isFilled():
            return True
        
        original_cell = self.content[next[0]][next[1]]
        original_domains = self.domains

        for domain in self.domains[next[0]][next[1]]:
            if self.isValid(next[0], next[1], domain):
                self.content[next[0]][next[1]] = domain
                res = self.updateDomains(next[0], next[1], domain)

                if self.solve() and res:
                    return True
                else:
                    self.content[next[0]][next[1]] = original_cell
                    self.domains = original_domains
        
        return False        

    def isSolved(self):
        for row in self.content:
            for cell in row:
                if not cell.isFilled():
                    return False
        return True
                
                        

    def isValid(self, x, y, cell):
        # print("Checking validity of ", cell.display(), " in ", x, " ", y)
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
            
            if self.content[n[0]][n[1]].isFilled():
                if self.colors.index(cell.color) < self.colors.index(self.content[n[0]][n[1]].color):
                    if cell.number < self.content[n[0]][n[1]].number:
                        # print("Bad priority color ", cell.color, " more prior than neighbor ", self.content[n[0]][n[1]].color)
                        return False
                elif self.colors.index(cell.color) > self.colors.index(self.content[n[0]][n[1]].color):
                    if cell.number > self.content[n[0]][n[1]].number:
                        # print("Bad priority color ", cell.color, " less prior than neighbor ", self.content[n[0]][n[1]].color)
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

result = table.solve()
if result:
    table.display()
else:
    print("Could not find the answer")