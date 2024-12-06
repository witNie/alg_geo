from sortedcontainers import SortedSet


class Point:
    def __init__(self, x, y):
        self.x = x  # współrzędna x-owa
        self.y = y  # współrzędna y-owa

    def __eq__(self, other):  # przeciążenie operatora (==)
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):  # przeciążenie operatora (>)
        return self.x > other.x

    def __hash__(self):
        return hash((self.x, self.y))


class Section:
    def __init__(self, L, R):
        self.L = L  # lewy koniec odcinka
        self.R = R  # prawy koniec odcinka
        self.a = (self.L.y - self.R.y) / (self.L.x - self.R.x)  # współczynnik nachylenia
        self.b = self.L.y - self.a * self.L.x  # wyraz wolny
        self.x = L.x

    def update_x(x):  # metoda statyczna (pole wspólne dla klasy)
        Section.x = x

    def __eq__(self, other):
        return (self.L == other.L and self.R == other.R)

    def __gt__(self, other):
        return self.a * Section.x + self.b > other.a * Section.x + other.b

    def __hash__(self):
        return hash((self.L, self.R))


def is_intersection(sections):
    """
    Funkcja sprawdza, czy jakakolwiek para podanych odcinków się przecina
    :param sections: tablica odcinków w postaci krotek zawierających krotki współrzędnych końców odcinków
    :return: wartość typu Bool: True jeśli jakakolwiek para odcinków się przecina, False w przeciwnym razie
    """
    T = SortedSet()
    Q = SortedSet()
    n = len(sections)
    checked_pairs = set()
    class_sections = []

    for i in range(n):
        l = Point(sections[i][0][0], sections[i][0][1])
        r = Point(sections[i][1][0], sections[i][1][1])
        class_sections.append(Section(l, r))
        Q.add((l, 'l', i))
        Q.add((r, 'r', i))
    while len(Q) > 0:
        event = Q.pop(0)
        Section.update_x(event[0].x)
        new_neighbours = []
        if event[1] == 'l':
            T.add((class_sections[event[2]], event[2]))
            index = T.index((class_sections[event[2]], event[2]))
            if index > 0:
                s_one = T[index - 1][1]
                index_one, index_two = min(s_one, event[2]), max(s_one, event[2])
                if not (index_one, index_two) in checked_pairs:
                    checked_pairs.add((index_one, index_two))
                    new_neighbours.append((index_one, index_two))
            if index < len(T) - 1:
                s_two = T[index + 1][1]
                index_one, index_two = min(s_two, event[2]), max(s_two, event[2])
                if not (index_one, index_two) in checked_pairs:
                    checked_pairs.add((index_one, index_two))
                    new_neighbours.append((index_one, index_two))
        else:
            index = T.index((class_sections[event[2]], event[2]))
            if index > 0 and index < len(T) - 1:
                s_one = T[index - 1][1]
                s_two = T[index + 1][1]
                index_one, index_two = min(s_one, s_two), max(s_one, s_two)
                if not (index_one, index_two) in checked_pairs:
                    checked_pairs.add((index_one, index_two))
                    new_neighbours.append((index_one, index_two))
            del T[index]
        for (s_one, s_two) in new_neighbours:
            if intersects(class_sections[s_one], class_sections[s_two]):
                return True
    return False


def intersects(section_one, section_two):
    """
    Funkcja sprawdza, czy podane odcinki się przecinają
    :param section_one: pierwszy sprawdzany odcinek
    :param section_two: drugi sprawdzany odcinek
    :return: współrzędne punktu przecięcia - jeżeli odcinki się przecinają, None w przeciwnym razie
    """
    (a_one, b_one) = section_one.a, section_one.b
    (a_two, b_two) = section_two.a, section_two.b
    (l_one, u_one) = section_one.L.x, section_one.R.x
    (l_two, u_two) = section_two.L.x, section_two.R.x

    if a_one == a_two:
        return None
    x = (b_two - b_one) / (a_one - a_two)
    if max(l_one, l_two) < x < min(u_one, u_two):
        y = a_two * x + b_two
        return (x, y)
    return None


q = [((0, 0), (4, 4)), ((0, 4), (4, 0)), ((-1, 2), (1, 2))]

print(is_intersection(q))
