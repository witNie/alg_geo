from queue import PriorityQueue


def get_events(section):
    Q = PriorityQueue()
    n = len(section)
    for s in range(n):
        x, y = section[s][0]
        Q.put((x, y, 0, s))

        x, y = section[s][1]
        Q.put((x, y, 1, s))

    while not Q.empty():
        el = Q.get()
        print(el)

    return PriorityQueue

q = [((1,0),(5,3)), ((3,7), (4,2))]

print(get_events(q))
