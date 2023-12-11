import copy
import sys
import queue as Q
import Gameboard

class Block_class:

    def __init__(self, x, y, rotation, parent, board, x1=None, y1=None):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.parent = parent
        self.board = copy.deepcopy(board)
        self.x1 = x1
        self.y1 = y1
        
    def read_map(self, fileMap):
        with open(fileMap) as f:
            MAP_ROW, MAP_COL, xStart, yStart = [int(x) for x in next(f).split()] # read first line
            sourceMap = []
            countMapLine = 1
            for line in f: # read map
                countMapLine += 1
                sourceMap.append([int(x) for x in line.split()])
                if countMapLine > MAP_ROW:
                    break

            # read managedBoard
            manaBoa = []
            for line in f: # read manaBoa
                manaBoa.append([int(x) for x in line.split()])

        return MAP_ROW, MAP_COL, xStart, yStart, sourceMap, manaBoa

    def display_map(self):
        for item in self.sourceMap:
            print(item)
        print("Start at (", self.xStart, ",", self.yStart,")")
        print("ManaBoa:")
        for item in self.ManaBoa:
            print(item)
        print("======================================")

    def move(self, direction):
        delta_x, delta_y = 0, 0
        rotation_change = None

        if direction == 'right':
            delta_x = 1 if self.rotation in ["STAND", "LAY_Y"] else 2
            rotation_change = "LAY_X" if self.rotation == "STAND" else "STAND"
        elif direction == 'left':
            delta_x = -1 if self.rotation in ["STAND", "LAY_Y"] else -2
            rotation_change = "LAY_X" if self.rotation == "STAND" else "STAND"
        elif direction == 'up':
            delta_y = -1 if self.rotation in ["STAND", "LAY_X"] else -2
            rotation_change = "LAY_Y" if self.rotation == "STAND" else "STAND"
        elif direction == 'down':
            delta_y = 1 if self.rotation in ["STAND", "LAY_X"] else 2
            rotation_change = "LAY_Y" if self.rotation == "STAND" else "STAND"

        return Block_class(self.x + delta_x, self.y + delta_y, rotation_change or self.rotation, self.parent, self.board)

    def split_move(self, direction, split_part='first'):
        delta_x, delta_y = 0, 0
        if direction == 'up':
            delta_y = -1
        elif direction == 'down':
            delta_y = 1
        elif direction == 'left':
            delta_x = -1
        elif direction == 'right':
            delta_x = 1

        if split_part == 'first':
            return Block_class(self.x + delta_x, self.y + delta_y, self.rotation, self.parent, self.board, self.x1, self.y1)
        else:
            return Block_class(self.x, self.y, self.rotation, self.parent, self.board, self.x1 + delta_x, self.y1 + delta_y)
        
    def read_map(self, fileMap):
        with open(fileMap) as f:
            MAP_ROW, MAP_COL, xStart, yStart = [int(x) for x in next(f).split()] # read first line
            sourceMap = []
            countMapLine = 1
            for line in f: # read map
                countMapLine += 1
                sourceMap.append([int(x) for x in line.split()])
                if countMapLine > MAP_ROW:
                    break

            # read managedBoard
            manaBoa = []
            for line in f: # read manaBoa
                manaBoa.append([int(x) for x in line.split()])

        return MAP_ROW, MAP_COL, xStart, yStart, sourceMap, manaBoa

    def display_map(self):
        for item in self.sourceMap:
            print(item)
        print("Start at (", self.xStart, ",", self.yStart,")")
        print("ManaBoa:")
        for item in self.ManaBoa:
            print(item)
        print("======================================")
        
    def display_position(self):
        position = f"{self.rotation} at ({self.x}, {self.y})"
        if self.rotation == "SPLIT":
            position += f" and ({self.x1}, {self.y1})"
        print(position)

    def display_board(self):
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if self.is_block_position(row_index, col_index):
                    print("x", end=' ')
                elif col == 0:
                    print(" ", end=' ')
                else:
                    print(col, end=' ')
            print("")
    
    def is_block_position(self, row_index, col_index):
        if self.rotation != "SPLIT":
            if (self.y, self.x) == (row_index, col_index):
                return True
            if self.rotation == "LAY_X" and (self.y, self.x + 1) == (row_index, col_index):
                return True
            if self.rotation == "LAY_Y" and (self.y + 1, self.x) == (row_index, col_index):
                return True
        else:
            return (self.y, self.x) == (row_index, col_index) or (self.y1, self.x1) == (row_index, col_index)
        return False
    
    
# isValidBLock
def isValidBlock(block):
    
    if isFloor(block):
        
        # local definition
        x     = block.x
        y     = block.y
        x1    = block.x1
        y1    = block.y1
        rot   = block.rot
        board = block.board
        
        
        # Case 2: Đo đỏ
        if rot == "STANDING" and board[y][x] == 2:
            return False 

        # Case 3: Chữ X
        if rot == "STANDING" and board[y][x] == 3:
            isNumberThree(block,x,y)
        
        # Case 4: Cục tròn đặc (only đóng).
        if board[y][x] == 4:
            isNumberFour(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 4:
            isNumberFour(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 4:
            isNumberFour(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 4:
            isNumberFour(block,x1,y1)


        # Case 5: Cục tròn đặc (toggle)
        if board[y][x] == 5:
            isNumberFive(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 5:
            isNumberFive(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 5:
            isNumberFive(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 5:
            isNumberFive(block,x1,y1)

        # Case 6: Cục tròn đặc (only mở)
        if board[y][x] == 6:
            isNumberSix(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 6:
            isNumberSix(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 6:
            isNumberSix(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 6:
            isNumberSix(block,x1,y1)

        # Case 7: Phân thân 
        if rot == "STANDING" and board[y][x] == 7:
            isNumberSeven(block,x,y)
        # Case7_1: MERGE BLOCK
        if rot == "SPLIT": # check IS_MERGE
            # case LAYING_X: x first
            if y == y1 and x == x1 -1:
                block.rot = "LAYING_X"

            # case LAYING_X: x1 first
            if y == y1 and x == x1 + 1:
                block.rot = "LAYING_X"
                block.x   = x1

            # case LAYING_Y: y first
            if x == x1 and y == y1 - 1:
                block.rot = "LAYING_Y"
            
            # case LAYING_Y: y1 first
            if x == x1 and y == y1 + 1:
                block.rot = "LAYING_Y"
                block.y   = y1

        # Case 8: Chữ X (only mở)
        if rot == "STANDING" and board[y][x] == 8:
            isNumberEight(block,x,y)
            
        return True
    else:
        return False


def isFloor(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board
    
    if x >= 0 and y >= 0 and \
            y < MAP_ROW and x < MAP_COL and \
            board[y][x] != 0:

        if rot == "STANDING":
            return True
        elif rot == "LAYING_Y":
            if y+1 < MAP_ROW and board[y+1][x] != 0 :
                return True
        elif rot == "LAYING_X":
            if x+1 < MAP_COL and board[y][x+1] != 0 :
                return True
        else: # case SPLIT
            x1 = block.x1
            y1 = block.y1

            if x1 >= 0 and y1 >= 0 and \
                y1 < MAP_ROW and x1 < MAP_COL and \
                board[y1][x1] != 0:
                    return True

    else:
        return False


def isGoal(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board

    if rot == "STANDING" and  \
        board[y][x] == 9:
        return True
    else:
        return False


def isVisited(block):
    if block.rot != "SPLIT":

        for item in passState:
            if item.x == block.x     and item.y == block.y and \
                item.rot == block.rot and item.board == block.board:
                return True

    else: # case SPLIT
        for item in passState:
            if item.x  == block.x     and item.y  == block.y and \
               item.x1 == block.x1    and item.y1 == block.y1 and \
                item.rot == block.rot and item.board == block.board:
                return True

    return False

def move(Stack, block, flag):

    if isValidBlock(block):
        if isVisited(block):
            return None

        Stack.append(block)
        passState.append(block)
        #print(flag)
        return True 

    return False   

def printSuccess(block):
    
    print("\nTHIS IS SUCCESS ROAD")
    print("================================")
    
    successRoad = [block]
    temp = block.parent
    
    while temp != None:
        
        if temp.rot != "SPLIT":
            newBlock = Block(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board)
        else: # case SPLIT
            newBlock = Block(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board, temp.x1, temp.y1)

        successRoad = [newBlock] + successRoad
        
        temp = temp.parent
    
    step = 0
    for item in successRoad:
        step += 1
        print("\nStep:", step, end=' >>>   ')
        item.display_position()
        print("=============================")
        item.display_board()

    print("COMSUME",step,"STEP!!!!")