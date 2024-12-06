from sortedcontainers import SortedList


def orient(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def if_intersect(p1, p2, q1, q2):
    return (orient(p1, q1, q2) != orient(p2, q1, q2)) and (orient(p1, p2, q1) != orient(p1, p2, q2))


def section_intersection(s1, s2):
    p1, p2 = s1
    q1, q2 = s2

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

def bin_insert(sorted_list, element):
    left, right = 0, len(sorted_list)
    while left < right:
        mid = (left + right) // 2
        if sorted_list[mid][0] < element[0]:
            left = mid + 1
        else:
            right = mid

    sorted_list.insert(left, element)


def find_intersections(sections):
    events = []
    for i, (p1, p2) in enumerate(sections):
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        events.append((p1[0], 0, i, p1, p2))
        events.append((p2[0], 1, i, p1, p2))


    sections2 = sections
    events.sort()
    active_sections = SortedList(key=lambda i: (sections2[i][0][1], sections2[i][1][1]))
    intersections = []

    while len(events) > 0:
        event = events.pop(0)
        x, event_type, index, p1, p2 = event
        if event_type == 0:
            active_sections.add(index)
            idx = active_sections.index(index)

            if idx != 0 and if_intersect(sections[active_sections[idx - 1]][0], sections[active_sections[idx - 1]][1],
                                         p1, p2):
                inter = section_intersection(sections[active_sections[idx - 1]], (p1, p2))
                if inter:
                    intersections.append((inter, active_sections[idx-1], active_sections[idx]))
                    bin_insert(events, (inter[0], 2, None, active_sections[idx-1], active_sections[idx]))
            if idx != len(active_sections) - 1 and if_intersect(sections[active_sections[idx + 1]][0],
                                                                sections[active_sections[idx + 1]][1], p1, p2):
                inter = section_intersection(sections[active_sections[idx + 1]], (p1, p2))
                if inter:
                    intersections.append((inter, active_sections[idx], active_sections[idx+1]))
                    bin_insert(events, (inter[0], 2, None, active_sections[idx], active_sections[idx+1]))
        elif event_type == 1:
            idx = active_sections.index(index)
            if 0 < idx < len(active_sections) - 1:
                if if_intersect(sections[active_sections[idx - 1]][0], sections[active_sections[idx - 1]][1],
                                sections[active_sections[idx + 1]][0], sections[active_sections[idx + 1]][1]):
                    inter = section_intersection(sections[active_sections[idx - 1]], sections[active_sections[idx + 1]])
                    if inter:
                        intersections.append((inter, active_sections[idx-1], active_sections[idx+1]))
                        bin_insert(events, (inter[0], 2, None, active_sections[idx-1], active_sections[idx+1]))
            active_sections.remove(index)
        # elif event_type == 2:
        #     i1 = active_sections.index(p1)
        #     i2 = active_sections.index(p2)
        #     sections2[p2], sections2[p1] = sections2[p1], sections2[p2]
        #     del active_sections[i1]
        #     del active_sections[i2-1]
        #     active_sections.add(p1)
        #     active_sections.add(p2)
        #     if i1 < len(active_sections)-1 and if_intersect(sections[active_sections[i1]][0], sections[active_sections[i1]][1],
        #                         sections[active_sections[i1 + 1]][0], sections[active_sections[i1 + 1]][1]):
        #         inter = section_intersection(sections[active_sections[i1]], sections[active_sections[i1 + 1]])
        #         if inter:
        #             intersections.append((inter, active_sections[i1], active_sections[i1+1]))
        #             bin_insert(events, (inter[0], 2, None, active_sections[i1], active_sections[i1+1]))
        #     if i2 > 0 and if_intersect(sections[active_sections[i2-1]][0], sections[active_sections[i2-1]][1],
        #                         sections[active_sections[i2]][0], sections[active_sections[i2]][1]):
        #         inter = section_intersection(sections[active_sections[i2-1]], sections[active_sections[i2]])
        #         if inter:
        #             intersections.append((inter, active_sections[i2-1], active_sections[i2]))
        #             bin_insert(events, (inter[0], 2, None, active_sections[i2-1], active_sections[i2]))

    return intersections


segments = [
    ((0, 0), (4, 4)),
    ((0, 4), (4, 0)),
    ((-1, 2), (1, 2))
]

print(find_intersections(segments))
