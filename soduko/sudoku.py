import numpy as np


class Table:
    """
    This class represents a sudoku table

    colors is a list of colors, colors with smaller index has more priority
    content is the real table
    size is the size of content (row or columns)
    domains is valid answers for each cell, each answer is a cell stored in corresponding index
    domains is -1 if that position of table is filled already and indicates that this cell should not be changed 
    """

    def __init__(self, input_string, colors):
        self.colors = colors
        self.size = len(input_string)
        self.content = []
        self.domains = [[[] for x in range(self.size)] for y in range(self.size)]

        # Fill content
        for i in range(self.size):
            self.content.append([])
            for j in range(self.size):
                self.content[i].append(Cell(input_string[i][j][0], input_string[i][j][1]))

        # Fill initial valid domains
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
        # Calculate number of remaining values for unfilled cells
        # return index of next cell to work with

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
                    min_val = remaining_values[i][j]
                    min_index[0] = i
                    min_index[1] = j
        return min_index

    def updateDomains(self,x , y, cell):
        # Update domains of valid candidates
        # for effected cells according to the given cell
        # return false if at least one cell has no domain left
        # meaning this solution gets stuck

        # Set the given cell domain -1
        # it means that it's fixed and should not be changed
        self.domains[x][y] = -1

        # Update domain values for this column
        for i in range(self.size):
            if self.domains[i][y] == -1:
                continue
            else:
                for domain in self.domains[i][y]:
                    if not self.isValid(i, y, domain):
                        self.domains[i][y].remove(domain)
        
        # Update domain values for this row
        for j in range(self.size):
            if self.domains[x][j] == -1:
                continue
            else:
                for domain in self.domains[x][j]:
                    if not self.isValid(x, j, domain):
                        self.domains[x][j].remove(domain)

        # Check if any cell has domain values to work with
        for i in range(self.size):
            for j in range(self.size):
                if self.domains[i][j] == -1:
                    continue
                if len(self.domains[i][j]) == 0:
                    return False
        
        return True
    
    def solve(self):
        # Solve the problem
        # Return false if the puzzle is not solvable

        # Get next table cell to set values in
        next = self.mrv()
        
        # Check if minimum remaining value is filled
        # in this case there is no "real" value remaining so the puzzle is solved
        if self.content[next[0]][next[1]].isFilled():
            return True
        
        # Save a backup in the case of need
        original_cell = self.content[next[0]][next[1]]
        original_domains = self.domains

        # Set all valid values and backtracks using recursion
        for domain in self.domains[next[0]][next[1]]:
            # Set valid domain
            self.content[next[0]][next[1]] = domain
            # Forward check to see if this change locks the problem or not
            # Update domains according to this change
            res = self.updateDomains(next[0], next[1], domain)

            # proceed to solve the problem
            if self.solve() and res:
                return True
            # backtrack if not successful
            else:
                self.content[next[0]][next[1]] = original_cell
                self.domains = original_domains
        
        return False        

    def isValid(self, x, y, cell):
        # Check if a given cell is valid in place (x, y) in the table
        # return true if it's valid

        # Check columnwise uniqueness
        for i in range(self.size):
            if i == x:
                continue
            if cell.number == self.content[i][y].number:
                return False
        
        # Check rowwise uniqueness
        for j in range(self.size):
            if j == y:
                continue
            if cell.number == self.content[x][j].number:
                return False

        # Check neighbors
        for n in self.getNeighbors(x, y):
            # Check if neighbors have distinct colors
            if cell.color == self.content[n[0]][n[1]].color:
                return False
            
            # Check set color priority match the numbers
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
        # Find neighbors of a given cell
        # Note that diagonal adjacent cells are not considers neighbors
        neighbors = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]

        for n in neighbors:
            if n[0] < 0  or n[0] >= self.size or n[1] < 0 or n[1] >= self.size:
                neighbors.remove(n)

        return neighbors

    def display(self):
        for row in self.content:
            print(row[0].display(),"   ",row[1].display(),"   ",row[2].display(),"   ")


class Cell:
    """
    This class represents each cell of the sudoku table

    number is a string representing the number of cell
    color is a string representing the number of cell
    """

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def display(self):
        return self.number + self.color

    def isFilled(self):
        # return true if the cell has both number and color set
        if self.number != "*" and self.color != "#":
            return True
        return False

    def hasOnlyNumber(self):
        # return true if color value is set to default and number is set
        if self.number != "*" and self.color == "#":
            return True
        return False

    def hasOnlyColor(self):
        # return true if number value is set to default and color is set
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

# Read inputs
colors, tableList = read_input()
# Generate table using given input
table = Table(tableList, colors)

# Solve sudoku
result = table.solve()
if result:
    table.display()
else:
    print("Could not find the answer")