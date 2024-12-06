def orient(a, b, c):
    return (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0]) > 0


def check_int(s1, s2):
    a, b = s1
    c, d = s2
    return orient(a, b, c) != orient(a, b, d)

#
# q = ((0, 4), (4, 0))
# p = ((4, 3), (5, 3))
# print(check_int(q, p))

def find_int(s1, s2):
    x1, y1 = s1[0]
    x2, y2 = s1[1]
    a1, b1 = s2[0]
    a2, b2 = s2[1]

    v1 = (x2 - x1, y2 - y1)
    v2 = (a2 - a1, b2 - b1)

    det = v1[0] * v2[1] - v1[1] * v2[0]


    t = ((a1 - x1) * v2[1] - (b1 - y1) * v2[0]) / det
    u = ((a1 - x1) * v1[1] - (b1 - y1) * v1[0]) / det


    int_x = x1 + t * v1[0]
    int_y = y1 + t * v1[1]
    return (int_x, int_y)


q = ((0, 4), (4, 0))
p = ((2, 0), (5, 3))
print(find_int(q, p))
