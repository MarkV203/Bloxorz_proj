def readMap(fileMap):
    with open(fileMap) as f:
        map_x, map_y, start_x, start_y = [int(x) for x in next(f).split()] # read map dimensions and start Coordinates
        sourceMap = []
        countMapLine = 1
        for line in f: # read map
            countMapLine += 1
            sourceMap.append([int(x) for x in line.split()])
            if countMapLine > map_x: break

        # read buttons on map
        map_buttons = []
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
