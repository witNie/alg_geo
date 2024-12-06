def binsearch(lst, el):
    n = len(lst)

    # If the new element is larger than the last element, return n
    if n == 0 or el[0] > lst[-1][0]:
        return n

    l, r = 0, n - 1
    while l <= r:
        mid = (l + r) // 2
        if lst[mid][0] < el[0]:
            l = mid + 1
        else:
            r = mid - 1

    return l



def event_getter(section):
    events = []
    n = len(section)
    for s in range(n):

        x, y = section[s][0]
        if (x, y, "s") not in events:
            ind = binsearch(events, (x, y, "s", s))
            if ind == len(events):
                events.append((x, y, "s", s))
            else:
                events.insert(ind, (x, y, "s", s))

        x, y = section[s][1]
        if (x, y, "t", s) not in events:
            ind = binsearch(events, (x, y, "t", s))
            if ind == len(events):
                events.append((x, y, "t", s))
            else:
                events.insert(ind, (x, y, "t", s))



    return events



q = [((1, 2), (4, 4)), ((7, 9), (8, 3)), ((5, 1), (6, 8))]

print(event_getter(q))
