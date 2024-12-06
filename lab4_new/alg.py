from q_init import get_events
from web import Tree, Node


def bentley_ottman(section):
    Q = get_events(section)
    intersections = set()
    bst = Tree()
    while not Q.empty():
        q = Q.get()
        handle(q, intersections)

