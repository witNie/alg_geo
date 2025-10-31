from avltree import *
from queue import PriorityQueue

CURR_X = 0
EPS = 10**(-11)


class Segment:
    def __init__(self, start, end, ind):
        self.start = start
        self.end = end
        self.ind = ind

        x1, y1 = self.start
        x2, y2 = self.end
        self.v = (x2 - x1, y2 - y1)

    def find_intersection(self, other):
        x1, y1 = self.start
        x2, y2 = self.end
        x3, y3 = other.start
        x4, y4 = other.end
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / den

        if 0 <= t <= 1 and 0 <= u <= 1:
            intersect_x = x1 + t * (x2 - x1)
            intersect_y = y1 + t * (y2 - y1)
            return (intersect_x, intersect_y)

        return None

    def find_y_at_x(self, x):
        x1, y1 = self.start
        x2, y2 = self.end
        if x1 == x2:
            return y1 if y1 == y2 else None
        slope = (y2 - y1) / (x2 - x1)
        return y1 + slope * (x - x1)

    def __gt__(self, other):
        global CURR_X, EPS

        y_self = self.find_y_at_x(CURR_X)
        y_other = other.find_y_at_x(CURR_X)

        if y_self is None or y_other is None:
            raise ValueError("Jedna z prostych jest pionowa :(")

        if y_self > y_other + EPS:
            return True
        elif y_self + EPS < y_other:
            return False
        else:
            slope_self = self.v[1] / self.v[0] if self.v[0] != 0 else float('inf')
            slope_other = other.v[1] / other.v[0] if other.v[0] != 0 else float('inf')
            return slope_self > slope_other

    def __eq__(self, other):
        return self.ind == other.ind

    def __str__(self):
        return str(self.ind)


def algorithm(sections):
    global CURR_X
    n = len(sections)
    T = Tree()
    Q = PriorityQueue()
    Intersections = []
    toInsert = []
    segments = []
    for i in range(n):
        Q.put((sections[i][0][0], 0, i))
        Q.put((sections[i][1][0], -1, i))
        segments.append(Segment(sections[i][0], sections[i][1], i))
    while not Q.empty():
        event = Q.get()
        X, event_type, index = event
        if event_type == 0:
            CURR_X = X
            newSeg = Segment(sections[index][0], sections[index][1], index)
            T.insert_key(newSeg)
            pred = T.get_predecessor(T.root, newSeg)
            succ = T.get_successor(T.root, newSeg)
            if pred and newSeg.find_intersection(pred):
                intersection_point = newSeg.find_intersection(pred)
                if intersection_point[0] > CURR_X:
                    Intersections.append((intersection_point, pred, newSeg))
                    Q.put((intersection_point[0], -2, (pred.ind, newSeg.ind)))
            if succ and newSeg.find_intersection(succ):
                intersection_point = newSeg.find_intersection(succ)
                if intersection_point[0] > CURR_X:
                    Intersections.append((intersection_point, newSeg, succ))
                    Q.put((intersection_point[0], -2, (newSeg.ind, succ.ind)))
        elif event_type == -1:
            CURR_X = X
            delSeg = Segment(sections[index][0], sections[index][1], index)
            pred = T.get_predecessor(T.root, delSeg)
            succ = T.get_successor(T.root, delSeg)
            if succ and pred and pred.find_intersection(succ):
                intersection_point = pred.find_intersection(succ)
                if intersection_point[0] > CURR_X:
                    Intersections.append((intersection_point, pred, succ))
                    Q.put((intersection_point[0], -2, (pred.ind, succ.ind)))
            T.delete_key(delSeg)
        elif event_type == -2:
            lower = Segment(sections[index[0]][0], sections[index[0]][1], index[0])
            higher = Segment(sections[index[1]][0], sections[index[1]][1], index[1])
            l_pred = T.get_predecessor(T.root, lower)
            h_succ = T.get_successor(T.root, higher)
            if l_pred and h_succ and (l_pred == h_succ or l_pred > h_succ):
                continue
            if h_succ and lower.find_intersection(h_succ):
                intersection_point = lower.find_intersection(h_succ)
                if intersection_point[0] > X:
                    Intersections.append((intersection_point, lower, h_succ))
                    Q.put((intersection_point[0], -2, (lower.ind, h_succ.ind)))
            if l_pred and higher.find_intersection(l_pred):
                intersection_point = higher.find_intersection(l_pred)
                if intersection_point[0] > X:
                    Intersections.append((intersection_point, l_pred, higher))
                    Q.put((intersection_point[0], -2, (l_pred.ind, higher.ind)))
            T.delete_key(lower)
            T.delete_key(higher)
            if Q.queue[0][0] != -2 and Q.queue[0][1] != X:
                CURR_X = X
                T.insert_key(higher)
                T.insert_key(lower)
                while len(toInsert) > 0:
                    T.insert_key(toInsert.pop(0))
            else:
                toInsert.append(higher)
                toInsert.append(lower)
    # format
    Int_points = [(x[0], x[1].ind, x[2].ind) for x in Intersections]
    Int_points = sorted(set(Int_points))
    index = 0
    result = []
    while index != len(Int_points):
        point = Int_points[index][0]
        lines = {Int_points[index][1], Int_points[index][2]}
        j = index + 1
        while j < len(Int_points) and point == Int_points[j][0]:
            lines.add(Int_points[j][1])
            lines.add(Int_points[j][2])
            j += 1
            index += 1
        result.append((point, sorted(lines, key=lambda x: segments[x])))
        index += 1
    index = 0
    while index + 1 < len(result):
        if result[index][1] == result[index + 1][1]:
            result.pop(index+1)
        else:
            index += 1
    return result

if __name__ == "__main__":
    B = [
        ((0.8225806451612905, 3.5064935064935066), (8.951612903225806, 3.917748917748918)),
        ((1.4193548387096775, 2.4025974025974026), (6.580645161290322, 9.220779220779221)),
        ((2.5161290322580645, 9.675324675324674), (7.887096774193548, 2.554112554112554)),
        ((2.5483870967741935, 6.147186147186147), (4.435483870967742, 2.467532467532468)),
        ((2.2419354838709675, 2.770562770562771), (4.419354838709678, 5.238095238095238)),
        ((3.4193548387096775, 2.5324675324675328), (5.516129032258064, 4.3939393939393945)),
        ((4.919354838709678, 5.77922077922078), (6.64516129032258, 6.58008658008658)),
        ((6.225806451612904, 5.411255411255412), (6.5, 4))
    ]
    print(algorithm(B))
