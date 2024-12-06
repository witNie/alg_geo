# from web import Tree, Node
from queue import PriorityQueue

def bin_search(list, element):
    n = len(list)
    l, r = 0, n - 1
    while l <= r:
        mid = (l + r) // 2
        if list[mid][0][1] == element[1]:
            return mid
        elif list[mid][0][1] > element[1]:
            right = mid - 1
        else:
            left = mid + 1


def sweep(section):
    n = len(section)

    Q = PriorityQueue()

    for s in section:
        print(s)
        for p in s:
            x, y = p
            if (x, y) not in Q:
                Q.put((x,y))
    return Q.e


q = [((1,2),(2,3))]
print(sweep(q))

