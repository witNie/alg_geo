def bin_search(list, element):
    n = len(list)
    l, r = 0, n - 1
    while l < r:
        mid = (l + r) // 2
        if list[mid][0] > element[0]:
            l = mid+1
        else:
            r = mid
    return r


def fun(lines):
    list = []
    for s in lines:
        for p in s:
            x, y = p
            if (x, y) not in list:
                ind = bin_search(list, (x, y))
                list.insert(ind, (x, y))

    return list

# l = [((1,2),(4,5)),((3,3),(1,2))]
# print(fun(l))

list = [(1,2),(2,3),(4,1)]
print(bin_search(list, (3,3)))
