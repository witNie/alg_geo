def handle(event, intersections, bst, section):
    if event[2] == 0:
        x, y = section[event[3]]
        bst.add(section[event[3]])
