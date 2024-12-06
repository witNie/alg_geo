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
    for s in section:
        for p in s:
            x, y = p
            if (x, y) not in events:
                ind = binsearch(events, (x, y))
                if ind == len(events):
                    events.append((x, y))
                else:
                    events.insert(ind, (x,y))

    return events


q = [((1, 2), (4, 4)), ((7, 9), (8, 3)), ((5, 1), (6, 8))]

print(event_getter(q))

# q = [1, 2, 3, 5, 7, 9]
# q.insert(2, 3)
# print(q)

