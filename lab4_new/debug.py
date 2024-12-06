from sortedcontainers import SortedSet

class Segment:

    def __init__(self, start, end, ind):
        self.start = start
        self.end = end
        self.ind = ind

    def move_sweep(x):
        Segment.x = x

    def __gt__(self, other):
        v = ((self.end[0] - self.start[0]), (self.end[1] - self.start[1]))
        v2 = ((other.end[0] - other.start[0]), (other.end[1] - other.start[1]))

        t = (Segment.x - self.start[0]) / v[0]
        t2 = (Segment.x - other.start[0]) / v2[0]

        return self.start[1] + t * v[1] > other.start[1] + t2 * v2[1]

    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end) and (self.ind == other.ind)

    def __hash__(self):
        return hash((self.start, self.end, self.ind))

    def __str__(self):
        return str(self.ind)+"-\ " + "(" + str(self.start[0]) + ", "+str(self.start[1])+")"+ "->"+ "("+str(self.end[0]) + ", "+str(self.end[1])+")"

def printSet(sortedset):
    print()
    for i in range(len(sortedset)):
        print(sortedset[i], end=" ")
    print()
    print()

# Q = SortedSet()
# Q.add(((1,3),100))
# Q.add(((2,1),1))
# print(Q)

def f():


print(f())
