from visualizer import *

from interactive import *
import time

def main():
    drawer = InteractiveLineDrawer()
    drawer.run()
    sections = drawer.result
    print("\nsections =", sections)
    starttime = time.time()
    result = algorithm(sections)
    endtime = time.time()
    print("result =", result)
    print(len(result))
    print("runtime: ", endtime - starttime, " [s]")
    vis(sections, result)

main()