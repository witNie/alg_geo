from sortedcontainers import SortedSet


class Segment:
    x = None

    def __init__(self, startP, endP, ind):
        self.startP = startP
        self.endP = endP
        self.ind = ind

    def move_sweep(x):
        Segment.x = x

    def __gt__(self, other):
        v = ((self.endP[0] - self.startP[0]), (self.endP[1] - self.startP[1]))
        v2 = ((other.endP[0] - other.startP[0]), (other.endP[1] - other.startP[1]))

        t = (Segment.x - self.startP[0]) / v[0] if v[0] != 0 else float('inf')
        t2 = (Segment.x - other.startP[0]) / v2[0] if v2[0] != 0 else float('inf')

        tb = (Segment.x - 0.001 - self.startP[0]) / v[0] if v[0] != 0 else float('inf')
        t2b = (Segment.x - 0.001 - self.startP[0]) / v[0] if v[0] != 0 else float('inf')

        return self.startP[1] + t * v[1] > other.startP[1] + t2 * v2[1] or (
                    self.startP[1] + t * v[1] == other.startP[1] + t2 * v2[1] and self.startP[1] + tb * v[1] <
                    other.startP[1] + t2b * v2[1])

    # def __lt__(self,other):
    #     v = ((self.endP[0] - self.startP[0]), (self.endP[1] - self.startP[1]))
    #     v2 = ((other.endP[0] - other.startP[0]), (other.endP[1] - other.startP[1]))
    #
    #     t = (Segment.x - self.startP[0]) / v[0] if v[0] != 0 else float('inf')
    #     t2 = (Segment.x - other.startP[0]) / v2[0] if v2[0] != 0 else float('inf')
    #
    #
    #     return self.startP[1] + t * v[1] < other.startP[1] + t2 * v2[1]

    def __eq__(self, other):
        return (self.startP == other.startP) and (self.endP == other.endP) and (self.ind == other.ind)

    def __hash__(self):
        return hash((self.startP, self.endP, self.ind))






def orient(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def if_intersect(segment1, segment2):
    p1, p2 = segment1.startP, segment1.endP
    q1, q2 = segment2.startP, segment2.endP
    return (orient(p1, q1, q2) != orient(p2, q1, q2)) and (orient(p1, p2, q1) != orient(p1, p2, q2))


def section_intersection(segment1, segment2):
    p1, p2 = segment1.startP, segment1.endP
    q1, q2 = segment2.startP, segment2.endP

    A1 = p2[1] - p1[1]
    B1 = p1[0] - p2[0]
    C1 = A1 * p1[0] + B1 * p1[1]
    A2 = q2[1] - q1[1]
    B2 = q1[0] - q2[0]
    C2 = A2 * q1[0] + B2 * q1[1]
    det = A1 * B2 - A2 * B1

    if det == 0:
        return None

    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det

    return (x, y)


def alg(sections):
    n = len(sections)
    vis = Visualizer()

    Q = SortedSet(key=lambda x: x[0][0])
    T = SortedSet()

    for i in range(n):
        (x1, y1), (x2, y2) = sections[i]
        Q.add(((x1, y1), 0, i))
        Q.add(((x2, y2), 1, i))
    # printSet(Q)
    intersections = set()
    while len(Q) > 0:
        # print(Q)
        event = Q.pop(0)
        # print(event)
        point, event_type, ind = event
        # print(point[0])

        if event_type == 0:
            Segment.move_sweep(point[0])
            s, t = sections[ind]
            T.add(Segment(s, t, ind))
            # printSet(T)
            # print(Segment(s, t, ind))
            # if len(T) > 1:
            #     print(Segment(s, t, ind) == T[1])
            #     print(T.index(T[0]))
            index = T.index(Segment(s, t, ind))
            if index > 0 and if_intersect(T[index - 1], T[index]):
                intersection_point = section_intersection(T[index - 1], T[index])
                if intersection_point and intersection_point[0] > Segment.x:
                    intersections.add(intersection_point)
                    vis.add_point(intersection_point, color='brown')
                    Q.add(((intersection_point[0], intersection_point[1]), 2, (T[index - 1].ind, T[index].ind)))
            if index < len(T) - 1 and if_intersect(T[index], T[index + 1]):
                intersection_point = section_intersection(T[index], T[index + 1])
                if intersection_point and intersection_point[0] > Segment.x:
                    intersections.add(intersection_point)
                    vis.add_point(intersection_point, color='brown')
                    Q.add(((intersection_point[0], intersection_point[1]), 2, (T[index].ind, T[index + 1].ind)))
        elif event_type == 1:

            s, t = sections[ind]
            temp = Segment(s, t, ind)
            # print("x: ")
            # print(Segment.x)
            # print("temp: ")
            # print(temp)
            # print(temp == T[1])
            # if len(T) > 1:
            #     print(T[0] < T[1])
            #     print(intersections)
            # print("Tree:")
            # printSet(T)
            idx = T.index(temp)
            # print(idx)
            if len(T) - 1 > idx > 0 and if_intersect(T[idx - 1], T[idx + 1]):
                intersection_point = section_intersection(T[idx - 1], T[idx + 1])
                if intersection_point and intersection_point[0] > Segment.x:
                    intersections.add(intersection_point)
                    vis.add_point(intersection_point, color='brown')
                    Q.add(((intersection_point[0], intersection_point[1]), 2, (T[idx-1].ind, T[idx + 1].ind)))
            del T[idx]
            Segment.move_sweep(point[0])


            # del T[index]
            # Segment.move_sweep(point[0])
            # if len(T) - 1> index > 0 and if_intersect(T[index-1], T[index]):
            #     intersection_point = section_intersection(T[index-1], T[index])
            #     if intersection_point:
            #         intersections.add(intersection_point)
            #         Q.add(((intersection_point[0], intersection_point[1]), 2, (T[index-1].ind, T[index].ind)))
        elif event_type == 2:
            # print(event)
            sL = sections[ind[0]]
            sU = sections[ind[1]]

            segL = Segment(sL[0], sL[1], ind[0])
            segU = Segment(sU[0], sU[1], ind[1])
            # print(segL, segU)
            # printSet(T)
            idxL = T.index(segL)
            idxU = idxL + 1
            if idxU < len(T) - 1 and if_intersect(segL, T[idxU + 1]):
                intersection_point = section_intersection(segL, T[idxU + 1])
                if intersection_point and intersection_point[0] > Segment.x:
                    intersections.add(intersection_point)
                    vis.add_point(intersection_point, color='brown')
                    Q.add(((intersection_point[0], intersection_point[1]), 2, (segL.ind, T[idxU + 1].ind)))
            if idxL > 0 and if_intersect(T[idxL - 1], segU):
                intersection_point = section_intersection(T[idxL - 1], segU)
                if intersection_point and intersection_point[0] > Segment.x:
                    intersections.add(intersection_point)
                    vis.add_point(intersection_point, color='brown')
                    Q.add((intersection_point, 2, (T[idxL - 1].ind, segU.ind)))

            del T[idxU]
            del T[idxL]
            Segment.move_sweep(point[0])
            # print(segU < segL)
            T.add(segL)
            T.add(segU)
            # printSet(T)

            # print(index2)
            #     s1, t1 = seg1
            #     s2, t2 = seg2
            #     # printSet(T)
            #
            #     T.discard(Segment(s1, t1, ind[0]))
            #     T.discard(Segment(s2, t2, ind[1]))
            #     Segment.move_sweep(point[0])
            #     a = Segment(s2, t2, ind[1])
            #     b = Segment(s1, t1, ind[0])
            #     printSet(T)
            #     T.add(a)
            #     T.add(b)
            # index1 = T.index(seg2)
            # index2 = T.index(seg1)
            # print(index1, index2)
            # printSet(T)
        #     if index2 < len(T) - 1 and if_intersect(T[index2], T[index2+1]):
        #         intersection_point = section_intersection(T[index2], T[index2+1])
        #         if intersection_point:
        #             intersections.add(intersection_point)
        #             Q.add((intersection_point, 2, (T[index2], T[index2+1])))
        #     if index1 > 0 and if_intersect(T[index1], T[index1-1]):
        #         intersection_point = section_intersection(T[index1], T[index1-1])
        #         if intersection_point:
        #             intersections.add(intersection_point)
        #             Q.add((intersection_point, 2, (T[index1-1], T[index1])))
        # printSet(T)


    return intersections, vis
