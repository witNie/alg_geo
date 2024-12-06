from sortedcontainers import SortedSet
from enum import Enum

EPS = 10 ** -12


def sgn(x):
    if x > EPS:
        return 1
    elif x < -EPS:
        return -1

    return 0


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        return (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        return self.x > other.x

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"


def det(a: Point, b: Point, c: Point):
    return (b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x)


class Equation():
    def __init__(self, a, b):
        self.a = a
        self.b = b


class EventType(Enum):
    START = 0,
    STOP = 1,
    INTERSECT = 2


class Event():
    def __init__(self, type, event_point, params):
        self.type = type
        self.params = params
        self.event_point = event_point


class Section():
    def __init__(self, start, end, id=None):
        if start.x > end.x:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end

        self.equation = self.get_line_equation(start, end)
        self.id = id

    def move_sweep(x):
        Section.x = x

    def get_line_equation(self, A, B) -> Equation:
        a = (B.y - A.y) / (B.x - A.x)
        b = A.y - a * A.x

        return Equation(a, b)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __gt__(self, other):
        return self.equation.a * Section.x + self.equation.b > other.equation.a * Section.x + other.equation.b



    def __hash__(self):
        return hash((self.start, self.end))


def check_intersection(section_1: Section, section_2: Section):
    A = section_1.start
    B = section_1.end

    C = section_2.start
    D = section_2.end

    d1 = sgn(det(A, B, C))
    d2 = sgn(det(A, B, D))
    d3 = sgn(det(C, D, A))
    d4 = sgn(det(C, D, B))

    if d1 == 0 or d2 == 0 or d3 == 0 or d4 == 0:
        return True

    return d1 * d2 < 0 and d3 * d4 < 0


def get_intersection(section_1: Section, section_2: Section):
    a_1, b_1 = section_1.equation.a, section_1.equation.b
    a_2, b_2 = section_2.equation.a, section_2.equation.b

    return Point((b_1 - b_2) / (a_2 - a_1), (a_2 * b_1 - a_1 * b_2) / (a_2 - a_1))


def is_intersection(sections):
    sections = [Section(Point(p1[0], p1[1]), Point(p2[0], p2[1])) for p1, p2 in sections]

    T = SortedSet()
    Q = SortedSet(key=lambda event: event[0])

    for i, section in enumerate(sections):
        Q.add((section.start, i))
        Q.add((section.end, i))

    while Q:
        p, index = Q.pop(0)

        if p == sections[index].start:
            Section.move_sweep(p.x)
            T.add(sections[index])
            i = T.index(sections[index])

            if (i - 1 >= 0 and check_intersection(T[i - 1], T[i])) or (
                    i + 1 < len(T) and check_intersection(T[i + 1], T[i])):
                return True

        elif p == sections[index].end:
            Section.move_sweep(p.x)
            T.remove(sections[index])

    return False


def if_intersects(Q, T, events_set: set, section_a: Section, section_b: Section):
    if not check_intersection(section_a, section_b):
        return

    intersection = get_intersection(section_a, section_b)
    intersection_identifier = (min(section_a.id, section_b.id), max(section_a.id, section_b.id))
    if not intersection_identifier in events_set:
        Q.add(Event(EventType.INTERSECT, intersection, (section_a, section_b)))
        events_set.add(intersection_identifier)


def find_intersections(sections):
    sections = [Section(Point(p1[0], p1[1]), Point(p2[0], p2[1]), i) for i, (p1, p2) in enumerate(sections)]

    T = SortedSet()
    Q = SortedSet(key=lambda event: event.event_point)
    event_points_set = set()

    for i, section in enumerate(sections):
        Q.add(Event(EventType.START, section.start, i))
        Q.add(Event(EventType.STOP, section.end, i))

    intersections = []

    while Q:
        event: Event = Q.pop(0)

        if event.type == EventType.START:
            Section.move_sweep(event.event_point.x)
            T.add(sections[event.params])
            s = T.index(sections[event.params])

            if s - 1 >= 0: if_intersects(Q, T, event_points_set, T[s - 1], T[s])
            if s + 1 < len(T): if_intersects(Q, T, event_points_set, T[s], T[s + 1])

        elif event.type == EventType.STOP:
            Section.move_sweep(event.event_point.x)
            s = T.index(sections[event.params])
            if s + 1 < len(T) and s - 1 >= 0:
                if_intersects(Q, T, event_points_set, T[s - 1], T[s + 1])
            T.pop(s)

        else:
            s1, s2 = event.params

            intersections.append((event.event_point, s1.id, s2.id))

            i_s1, i_s2 = T.index(s1), T.index(s2)

            T.remove(s1)
            T.remove(s2)

            Section.move_sweep(event.event_point.x + EPS)

            T.add(s1)
            T.add(s2)

            if i_s2 + 1 < len(T):
                if_intersects(Q, T, event_points_set, s1, T[i_s2 + 1])
            if i_s1 - 1 >= 0:
                if_intersects(Q, T, event_points_set, T[i_s1 - 1], s2)

    intersections = [((point.x, point.y), id1 + 1, id2 + 1) for point, id1, id2 in intersections]

    return intersections


q = [((0, 0), (4, 4)), ((0, 4), (4, 0))]

print(find_intersections(q))
