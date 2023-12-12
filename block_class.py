# -*- coding: utf-8 -*- 
# CMPSC 441 Final Project - Bloxorz AI Solver
# Author: Krish Parikh, Mark Vernachio, Donovan Biedermann 


import copy
import sys
import queue as Q

def readMap(fileMap):
    with open(fileMap) as f:
        map_x, map_y, start_x, start_y = [int(x) for x in next(f).split()] # read map dimensions and start Coordinates
        sourceMap = []
        countMapLine = 1
        for line in f: # reads map
            countMapLine += 1
            sourceMap.append([int(x) for x in line.split()])
            if countMapLine > map_x: break

        # read buttons on map
        map_buttons = []
        for line in f: # read buttons on map like this: (button x, button y, number of affected tiles, tile1 x, tile1 y, etc)
            map_buttons.append([int(x) for x in line.split()])

    print("\nMAP LAYOUT:")
    for item in sourceMap:
        print(item)
    print("Starting at (",start_x, ",", start_y,")")
    print("Button Coordinates:")
    for item in map_buttons:
        print(item)
    print("======================================")
    return map_x, map_y, start_x, start_y, sourceMap, map_buttons

#Object to track all the attributes while searching for goal and contains functions for moving the block.
class Block_class:

    def __init__(self, x, y, rot, parent, board, x1=None,y1=None):
        self.x      = x
        self.y      = y
        self.rot    = rot  
        self.parent = parent
        self.board  = copy.deepcopy(board)
        self.x1     = x1
        self.y1     = y1
    
    def __lt__(self, block):
        return True
    def __gt__(self, block):
        return True

    def move_block(self, direction):
        newBlock = Block_class(self.x, self.y, self.rot, self, self.board)

        if direction == 'left':
            if newBlock.rot == "STANDING":
                newBlock.rot = "LAYING_X"
                newBlock.x -= 2

            elif newBlock.rot == "LAYING_X":
                newBlock.x -= 1
                newBlock.rot = "STANDING"

            elif newBlock.rot == "LAYING_Y":
                newBlock.x -= 1

            return newBlock

        elif direction == 'right':
            if newBlock.rot == "STANDING":
                newBlock.x += 1
                newBlock.rot = "LAYING_X"

            elif newBlock.rot == "LAYING_X":
                newBlock.x += 2
                newBlock.rot = "STANDING"

            elif newBlock.rot == "LAYING_Y":
                newBlock.x += 1
             
            return newBlock

        elif direction == 'up':
            if self.rot == "STANDING":
                newBlock.y -= 2 
                newBlock.rot = "LAYING_Y"

            elif newBlock.rot == "LAYING_X":
                newBlock.y -= 1
        
            elif newBlock.rot == "LAYING_Y":
                newBlock.y -= 1
                newBlock.rot = "STANDING"
        
            return newBlock

        else:
            if newBlock.rot == "STANDING":
                newBlock.y += 1
                newBlock.rot = "LAYING_Y"

            elif newBlock.rot == "LAYING_X":
                newBlock.y += 1

            elif newBlock.rot == "LAYING_Y":
                newBlock.y += 2
                newBlock.rot = "STANDING"

            return newBlock

    # function to move when block is split
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

        return Block_class(self.x + delta_x, self.y + delta_y, self.rot, self.parent, self.board, self.x1, self.y1)

    #function for second split block
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

        return Block_class(self.x, self.y, self.rot, self.parent, self.board, self.x1 + delta_x, self.y1 + delta_y)

    def display_position(self):
        if self.rot != "SPLIT":
            print(self.rot, self.x, self.y)
        else:
            print(self.rot, self.x, self.y, self.x1, self.y1)
    
    def display_board(self):
        
        # defines variables from object locally
        x   = self.x
        y   = self.y
        x1  = self.x1
        y1  = self.y1
        rot = self.rot
        board = self.board

        #for normal case when block isn't split
        if rot != "SPLIT":
            
            for i in range(len(board)): # for row
                print("",end='  ')
                for j in range(len(board[i])): # for column in row

                    if (i==y and j==x and rot=="STANDING") or \
                            ((i==y and j==x) or (i==y and j==x+1) and rot=="LAYING_X") or \
                            ((i==y and j==x) or (i==y+1 and j==x) and rot=="LAYING_Y"):

                        print("x",end=' ')

                    elif(board[i][j]==0):
                        print(" ",end=' ')
                    else:
                        print(board[i][j], end=' ')
                print("")
        else: # For when block is split
            for i in range(len(board)): # for row
                print("",end='  ')
                for j in range(len(board[i])): # for column

                    if (i==y and j==x) or (i==y1 and j==x1):
                        print("x",end=' ')

                    elif(board[i][j]==0):
                        print(" ",end=' ')
                    else:
                        print(board[i][j], end=' ')
                print("")
    
# Button 3 regular X switch
def is_three(block,x,y):
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

                # closes the bridge
                if index < len(item):
                    numClose = item[index]
                    for i in range(numClose):
                        bX = item[index+2*i+1]
                        bY = item[index+2*i+2]
                        board[bX][bY]=0
                    index = index + 1 + 2 * numClose
            
                # opens the bridge
                if index < len(item):
                    numOpen = item[index]
                    for i in range(numOpen):
                        bX = item[index+2*i+1]
                        bY = item[index+2*i+2]
                        board[bX][bY]=1


# Button 4 O switch that only closes
def is_four(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 0

# Button 5 regular O switch
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

            # closes the bridge
            if index < len(item):
                numClose = item[index]
                    
                for i in range(numClose):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=0

                index = index + 1 + 2 * numClose
            

            # opens the bridge
            if index < len(item):
                numOpen = item[index]

                for i in range(numOpen):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=1


# Button 6 O switch that only opens
def is_six(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1

# Button 7 switch that teleports and switches block
def is_seven(block,x,y):  
    board = block.board
    array = []    
    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            # format x7 y7 2 x y x1 y1
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                array.append([bX,bY])

    (block.y,block.x,block.y1,block.x1) = (array[0][0],array[0][1],array[1][0], array[1][1])

    block.rot = "SPLIT"

# Button 8 X switch that only opens
def is_eight(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):

            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1




# checks to make sure the block is valid
def is_block(block):
    
    if is_floor(block):
        
        # local definition
        x     = block.x
        y     = block.y
        x1    = block.x1
        y1    = block.y1
        rot   = block.rot
        board = block.board
        
        
        if rot == "STANDING" and board[y][x] == 2:
            return False 

        # Button 3
        if rot == "STANDING" and board[y][x] == 3:
            is_three(block,x,y)
        
        # Button 4
        if board[y][x] == 4:
            is_four(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 4:
            is_four(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 4:
            is_four(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 4:
            is_four(block,x1,y1)


        # Button 5
        if board[y][x] == 5:
            is_five(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 5:
            is_five(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 5:
            is_five(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 5:
            is_five(block,x1,y1)

        # Button 6
        if board[y][x] == 6:
            is_six(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 6:
            is_six(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 6:
            is_six(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 6:
            is_six(block,x1,y1)

        # Button 7
        if rot == "STANDING" and board[y][x] == 7:
            is_seven(block,x,y)
        # Split case when it is button 7
        if rot == "SPLIT": 
            # when LAYING_X
            if y == y1 and x == x1 -1:
                block.rot = "LAYING_X"

            # when LAYING_X
            if y == y1 and x == x1 + 1:
                block.rot = "LAYING_X"
                block.x   = x1

            # when LAYING_Y
            if x == x1 and y == y1 - 1:
                block.rot = "LAYING_Y"
            
            # when LAYING_Y
            if x == x1 and y == y1 + 1:
                block.rot = "LAYING_Y"
                block.y   = y1

        # Button 8
        if rot == "STANDING" and board[y][x] == 8:
            is_eight(block,x,y)
            
        return True
    else:
        return False


def is_floor(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board
    
    if x >= 0 and y >= 0 and y < map_x and x < map_y and board[y][x] != 0:

        if rot == "STANDING":
            return True
        elif rot == "LAYING_Y":
            if y+1 < map_x and board[y+1][x] != 0 :
                return True
        elif rot == "LAYING_X":
            if x+1 < map_y and board[y][x+1] != 0 :
                return True
        else: # when block is split 
            x1 = block.x1
            y1 = block.y1

            if x1 >= 0 and y1 >= 0 and y1 < map_x and x1 < map_y and board[y1][x1] != 0:
                    return True

    else:
        return False


def is_goal(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board

    if rot == "STANDING" and board[y][x] == 9:
        return True
    else:
        return False

# function checks if visited when move function is called
def is_visited(block):
    #For regular case
    if block.rot != "SPLIT":

        for item in passState:
            if item.x == block.x and item.y == block.y and item.rot == block.rot and item.board == block.board:
                return True
    #only when block is split
    else: 
        for item in passState:
            if item.x  == block.x and item.y == block.y and item.x1 == block.x1 \
            and item.y1 == block.y1 and item.rot == block.rot and item.board == block.board:
                return True

    return False

def move(Stack, block):

    if is_block(block):
        #checks if visited
        if is_visited(block):
            return None

        Stack.append(block)
        passState.append(block)

        return True 

    return False   

def final_path(block):
    
    print("\nPath: ")
    print("================================")
    
    path = [block]
    temp = block.parent
    
    while temp != None:
        
        if temp.rot != "SPLIT":
            newBlock = Block_class(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board)
        else: # case SPLIT
            newBlock = Block_class(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board, temp.x1, temp.y1)

        path = [newBlock] + path
        
        temp = temp.parent
    
    step = 0
    for item in path:
        step += 1
        print("\nStep:", step, end=' >>>   ')
        item.display_position()
        print("=============================")
        item.display_board()

    print("The level was solved in", step, "steps")

    return False

def move(Stack, block):

    if is_block(block):
        #checks if visited
        if is_visited(block):
            return None

        Stack.append(block)
        passState.append(block)

        return True 

    return False   

def final_path(block):
    
    print("\nPath: ")
    print("================================")
    
    path = [block]
    temp = block.parent
    
    while temp != None:
        
        if temp.rot != "SPLIT":
            newBlock = Block_class(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board)
        else: # case SPLIT
            newBlock = Block_class(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board, temp.x1, temp.y1)

        path = [newBlock] + path
        
        temp = temp.parent
    
    step = 0
    for item in path:
        step += 1
        print("\nStep:", step, end=' >>>   ')
        item.display_position()
        print("=============================")
        item.display_board()

    print("The level was solved in", step, "steps")
    

# solve BFS
def BFS(block):

    board = block.board
    Queue = []
    Queue.append(block)
    passState.append(block)
    
    while Queue:
        current = Queue.pop(0)

        if is_goal(current):
            final_path(current)
            print("SUCCESS")
            return True

        if current.rot != "SPLIT":
            move(Queue,current.move_block('left'))
            move(Queue,current.move_block('right'))
            move(Queue,current.move_block('up'))
            move(Queue,current.move_block('down'))
        else: 
            move(Queue,current.split_move('left'))
            move(Queue,current.split_move('right'))
            move(Queue,current.split_move('up'))
            move(Queue,current.split_move('down'))
            
            move(Queue,current.split_move1('left'))
            move(Queue,current.split_move1('right'))
            move(Queue,current.split_move1('up'))
            move(Queue,current.split_move1('down'))
    return False



# START PROGRAM HERE
passState = []

map_x, map_y, start_x, start_y, sourceMap, map_buttons = readMap('map08.txt')

block = Block_class(start_x, start_y, "STANDING", None, sourceMap)
 
BFS(block)
