import copy
import sys
import queue as Q

def readMap(fileMap):
        with open(fileMap) as f:
            map_x, map_y, start_x, start_y = [int(x) for x in next(f).split()] # read map dimensions and start Coordinates
            sourceMap = []
            countMapLine = 1
            for line in f: # read map
                countMapLine += 1
                sourceMap.append([int(x) for x in line.split()])
                if countMapLine > map_x: break

            for line in f: # read buttons on bmap
                # 2 2 4 4 4 5
                map_buttons.append([int(x) for x in line.split()])

        print("\nYOUR MAP LOOK LIKE THIS:")
        for item in sourceMap:
            print(item)
        print("Start at (",start_x, ",", start_y,")")
        print("Button Coordinates:")
        for item in map_buttons:
            print(item)
        print("======================================")
        return map_x, map_y, start_x, start_y, sourceMap, map_buttons

class Block_class:

    def __init__(self, x, y, rotation, parent, board, x1=None, y1=None):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.parent = parent
        self.board = copy.deepcopy(board)
        self.x1 = x1
        self.y1 = y1

    def __lt__(self, block):
        return True
    
    def __gt__(self, block):
        return True
    
    def block_move(self, direction):
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

    def split_move(self, direction):
        """Moves the first part of the block in the first direction."""
        delta_x, delta_y = 0, 0
        if direction == 'up':
            delta_y = -1
        elif direction == 'down':
            delta_y = 1
        elif direction == 'left':
            delta_x = -1
        elif direction == 'right':
            delta_x = 1

        return Block_class(self.x + delta_x, self.y + delta_y, self.rotation, self.parent, self.board, self.x1, self.y1)

    def split_move1(self, direction):
        """Moves the second part of the block in the specified direction."""
        delta_x, delta_y = 0, 0
        if direction == 'up':
            delta_y = -1
        elif direction == 'down':
            delta_y = 1
        elif direction == 'left':
            delta_x = -1
        elif direction == 'right':
            delta_x = 1

        return Block_class(self.x, self.y, self.rotation, self.parent, self.board, self.x1 + delta_x, self.y1 + delta_y)
        
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
    
def isNumberThree(block,x,y):
    board = block.board

    for item in map_buttons:

        if (x,y) ==  (item[0], item[1]):
                # toggle
                numToggle = item[2]
                index = 2

                for i in range(numToggle):
                    bX = item[2*i+3]
                    bY = item[2*i+4]
                    if board[bX][bY] == 0:
                        board[bX][bY] = 1
                    else:
                        board[bX][bY] = 0
                index = index + 1 + 2 * numToggle

                # close
                if index < len(item):
                    numClose = item[index]
                    for i in range(numClose):
                        bX = item[index+2*i+1]
                        bY = item[index+2*i+2]
                        board[bX][bY]=0
                    index = index + 1 + 2 * numClose
            
                # open
                if index < len(item):
                    numOpen = item[index]
                    for i in range(numOpen):
                        bX = item[index+2*i+1]
                        bY = item[index+2*i+2]
                        board[bX][bY]=1



# Case 4: O button (close only)
def is_four(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 0

# Case 5: O button (regular)
def is_five(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            numToggle = item[2]
            index = 2
            for i in range(numToggle):
                bX = item[2*i+3]
                bY = item[2*i+4]

                if board[bX][bY] == 0:
                    board[bX][bY] = 1
                else:
                    board[bX][bY] = 0
            
            index = index + 1 + 2 * numToggle

            # close
            if index < len(item):
                numClose = item[index]
                    
                for i in range(numClose):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=0

                index = index + 1 + 2 * numClose
            

            # open
            if index < len(item):
                numOpen = item[index]

                for i in range(numOpen):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=1


# Case 6: O button (open only)
def is_six(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1

# Case 7: teleport and split
def is_seven(block,x,y):  
    array = []    

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                array.append([bX,bY])
    (block.y,block.x,block.y1,block.x1) = (array[0][0],array[0][1],array[1][0], array[1][1])
    block.rotation = "SPLIT"

    # Case 8: X button (open only)
def is_eight(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1
# is_valid
def is_block(block):
    
    if is_floor(block):
        
        # local definition
        x   = block.x
        y   = block.y
        x1  = block.x1
        y1  = block.y1
        rotation = block.rotation
        board = block.board
        
        
        if rotation == "STANDING" and board[y][x] == 2:
            return False 

 
        if rotation == "STANDING" and board[y][x] == 3:
            isNumberThree(block,x,y)
        
        if board[y][x] == 4:
            is_four(block,x,y)
        if rotation == "LAYING_X" and board[y][x+1] == 4:
            is_four(block,x+1,y)
        if rotation == "LAYING_Y" and board[y+1][x] == 4:
            is_four(block,x,y+1)
        if rotation == "SPLIT" and board[y1][x1] == 4:
            is_four(block,x1,y1)


        if board[y][x] == 5:
            is_five(block,x,y)
        if rotation == "LAYING_X" and board[y][x+1] == 5:
            is_five(block,x+1,y)
        if rotation == "LAYING_Y" and board[y+1][x] == 5:
            is_five(block,x,y+1)
        if rotation == "SPLIT" and board[y1][x1] == 5:
            is_five(block,x1,y1)

        
        if board[y][x] == 6:
            is_six(block,x,y)
        if rotation == "LAYING_X" and board[y][x+1] == 6:
            is_six(block,x+1,y)
        if rotation == "LAYING_Y" and board[y+1][x] == 6:
            is_six(block,x,y+1)
        if rotation == "SPLIT" and board[y1][x1] == 6:
            is_six(block,x1,y1)

        # Case 7: Phân thân 
        if rotation == "STANDING" and board[y][x] == 7:
            is_seven(block,x,y)
        # Case7_1: MERGE BLOCK
        if rotation == "SPLIT": # check IS_MERGE
            # case LAYING_X: x first
            if y == y1 and x == x1 -1:
                block.rotation = "LAYING_X"

            # case LAYING_X: x1 first
            if y == y1 and x == x1 + 1:
                block.rotation = "LAYING_X"
                block.x   = x1

            # case LAYING_Y: y first
            if x == x1 and y == y1 - 1:
                block.rotation = "LAYING_Y"
            
            # case LAYING_Y: y1 first
            if x == x1 and y == y1 + 1:
                block.rotation = "LAYING_Y"
                block.y   = y1

        # Case 8: Chữ X (only mở)
        if rotation == "STANDING" and board[y][x] == 8:
            is_eight(block,x,y)
            
        return True
    else:
        return False


def is_floor(block):
    x = block.x
    y = block.y
    rotation = block.rotation
    board = block.board
    
    # Check if the main part of the block is on the floor
    if x < 0 or y < 0 or y >= map_x or x >= map_y or board[y][x] == 0:
        return False

    if rotation in ["STAND", "LAY_X", "LAY_Y"]:
        # Additional checks for LAY_X and LAY_Y rotations
        if rotation == "LAY_X" and (x + 1 >= map_y or board[y][x + 1] == 0):
            return False
        if rotation == "LAY_Y" and (y + 1 >= map_x or board[y + 1][x] == 0):
            return False
        return True

    if rotation == "SPLIT":
        x1 = block.x1
        y1 = block.y1
        # Check if the split parts of the block are on the floor
        return x1 is not None and y1 is not None and \
               0 <= x1 < map_y and 0 <= y1 < map_x and \
               board[y1][x1] != 0

    return False


def is_goal(block):
    x = block.x
    y = block.y
    rotation = block.rotation
    board = block.board

    if rotation == "STANDING" and  \
        board[y][x] == 9:
        return True
    else:
        return False


def is_visited(block):
    if block.rotation != "SPLIT":

        for item in passState:
            if item.x == block.x     and item.y == block.y and \
                item.rotation == block.rotation and item.board == block.board:
                return True

    else: # case SPLIT
        for item in passState:
            if item.x  == block.x     and item.y  == block.y and \
               item.x1 == block.x1    and item.y1 == block.y1 and \
                item.rotation == block.rotation and item.board == block.board:
                return True

    return False

def move(Stack, block):

    if is_block(block):
        if is_visited(block):
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
        
        if temp.rotation != "SPLIT":
            newBlock = Block_class(temp.x, temp.y, \
                    temp.rotation, temp.parent, temp.board)
        else: # case SPLIT
            newBlock = Block_class(temp.x, temp.y, \
                    temp.rotation, temp.parent, temp.board, temp.x1, temp.y1)

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

def BFS(block):
#create local board variable from object block
    board = block.board
    #initialize queue and append block to 
    Queue = []
    Queue.append(block)
    passState.append(block)

    simulateStep = 0

    while Queue:
        current = Queue.pop(0)
        #current.disPlayPosition()
        #current.disPlayBoard()

        if is_goal(current):
            printSuccess(current)
            print("SUCCESS")
            print("CONSUME", simulateStep, "SIMULATION STEP")
            return True

        #
        if current.rotation != "SPLIT":
            simulateStep += 4

            move(Queue,current.block_move('up'))
            move(Queue,current.block_move('right'))
            move(Queue,current.block_move('down'))
            move(Queue,current.block_move('left'))
        else: 
            simulateStep += 8

            move(Queue,current.split_move('left'))
            move(Queue,current.split_move('right'))
            move(Queue,current.split_move('up'))
            move(Queue,current.split_move('down'))
            
            move(Queue,current.split_move1('left'))
            move(Queue,current.split_move1('right'))
            move(Queue,current.split_move1('up'))
            move(Queue,current.split_move1('down'))
    return False

passState = []
map_x, map_y, start_x, start_y, sourceMap, map_buttons = readMap('map01.txt')

block = Block_class(start_x, start_y, "STANDING", None, sourceMap)


BFS(block)