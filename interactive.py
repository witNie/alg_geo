import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

class InteractiveLineDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Click to draw line segments')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.points = []
        self.lines = []
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        # self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.cid_close = self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.result = []

    def on_click(self, event):
        if not event.inaxes:
            return

        self.points.append((event.xdata, event.ydata))


        if len(self.points) == 2:
            x_vals = [self.points[0][0], self.points[1][0]]
            y_vals = [self.points[0][1], self.points[1][1]]
            line, = self.ax.plot(x_vals, y_vals, marker='o')
            if x_vals[0] <= x_vals[1]:
                self.lines.append((self.points[0], self.points[1]))
            else:
                self.lines.append((self.points[1], self.points[0]))
            self.points = []


            self.fig.canvas.draw()

    def on_close(self, event):
        if self.lines:
            # print("\n[")
            for segment in self.lines:
                # print((tuple(map(float, segment[0])), tuple(map(float, segment[1]))), end=", \n")
                self.result.append((tuple(map(float, segment[0])), tuple(map(float, segment[1]))))
            last_segment = (tuple(map(float, self.lines[-1][0])), tuple(map(float, self.lines[-1][1])))
            # print(last_segment)
            # print("]")
        else:
            print("No line segments to display.")

    def run(self):
        plt.show()

if __name__ == '__main__':
    drawer = InteractiveLineDrawer()
    drawer.run()
