# Case 3: X button (regular)
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
def isNumberFour(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 0

# Case 5: O button (regular)
def isNumberFive(block,x,y):
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
def isNumberSix(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1

# Case 7: teleport  and split
def isNumberSeven(block,x,y):  
    board = block.board
    array = []    

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                array.append([bX,bY])
    (block.y,block.x,block.y1,block.x1) = \
            (array[0][0],array[0][1],array[1][0], array[1][1])
    block.rot = "SPLIT"

# Case 8: X button (open only)
def isNumberEight(block,x,y):
    board = block.board

    for item in map_buttons:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1
