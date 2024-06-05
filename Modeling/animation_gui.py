import numpy as np
import matplotlib.pyplot as plt

class Animation:
    def __init__(self, sol, list_of_object_lists, ax):
        self.sol = sol
        self.list_of_object_lists = list_of_object_lists
        self.ax = ax
        self.spring_lines = []
        self.mass_circles = []
        self.init_animation()

    def init_animation(self):
        t = self.sol.t
        y = -self.sol.y
        pos = y[0:int(len(y)/2)]
        x_pos = pos[::2]
        x_max = max((max(x) for x in x_pos))
        x_min = min((min(x) for x in x_pos))
        y_pos = pos[1::2]
        y_max = max((max(y) for y in y_pos))
        y_min = min((min(y) for y in y_pos))
        
        self.ax.set_ylim(y_min - 3, y_max + 3)
        self.ax.set_xlim(x_min - 3, x_max + 3)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_title('Animation')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        list_of_springs, list_of_mass = self.list_of_object_lists

        for i in range(len(list_of_springs)):
            x_sp, y_sp = list_of_springs[i].startingpoint
            x_ep, y_ep = list_of_springs[i].endpoint
            self.spring_lines.append(self.ax.plot([x_sp, x_ep], [y_sp, y_ep], lw=2, color=list_of_springs[i].color)[0])

        for i in range(len(list_of_mass)):
            self.mass_circles.append(plt.Circle(list_of_mass[i].position, list_of_mass[i].diameter, color=list_of_mass[i].color))
            self.ax.add_patch(self.mass_circles[i])

    def update_frame(self, num):
        y = -self.sol.y
        pos = y[0:int(len(y)/2)]
        x_pos = pos[::2]
        y_pos = pos[1::2]
        list_of_springs, list_of_mass = self.list_of_object_lists

        # Ensure num is within the range of positions
        if 0 <= num < len(y_pos[0]):

            for i in range(len(list_of_mass)):
                list_of_mass[i].move(x_pos[i][num], y_pos[i][num])
                self.mass_circles[i].set_center(list_of_mass[i].position)

            for i in range(len(list_of_springs)):
                if list_of_springs[i].startingpoint[1] == 0:
                    list_of_springs[i].move(list_of_springs[i].startingpoint, list_of_mass[i].position)
                    x_sp, y_sp = list_of_springs[i].startingpoint
                    x_ep, y_ep = list_of_springs[i].endpoint
                    self.spring_lines[i].set_data([x_sp, x_ep], [y_sp, y_ep])
                else:
                    list_of_springs[i].move(list_of_mass[i-1].position, list_of_mass[i].position)
                    x_sp, y_sp = list_of_springs[i].startingpoint
                    x_ep, y_ep = list_of_springs[i].endpoint
                    self.spring_lines[i].set_data([x_sp, x_ep], [y_sp, y_ep])
