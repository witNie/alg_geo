def binsearch(list, el):

    n = len(list)
    if el > list[n-1]:
        return n
    l, r = 0, n - 1
    while l < r - 1:
        #print(list[l], list[r])
        mid = (l + r) // 2
        #print(list[mid])
        if list[mid][0] > el[0]:
            r = mid
        else:
            l = mid + 1
    return r


q = [((1, 2), (4, 4)), ((5, 1), (6, 8)), ((7, 9), (8, 3))]
ind = binsearch(q, (2, 9))
q.insert(ind, (2, 9))
print(q)


