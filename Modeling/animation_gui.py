import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Animation:
    def __init__(self, sol, list_of_object_lists, ax):
        self.sol = sol
        self.list_of_object_lists = list_of_object_lists
        self.ax = ax
        self.spring_lines = []
        self.mass_circles = []
        self.sb_rectangles = []
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
        y_range = y_max - y_min

        self.ax.set_ylim(y_min - 3, y_max + 3)
        self.ax.set_xlim(x_min - 3, x_max + 3)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_title('Animation')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        list_of_springs, list_of_mass, list_of_sbs = self.list_of_object_lists

        # zorder is use in matplotlib to control the drawing order, the grid have a zorder of 2.5 by default
        # we want that the masses are plotted above the spring lines, so the zorder of the masses must have a higer values than the zorder of the spring lines
        # and both zorders must have a higher value than the zorder of the grid, because we want that the animation is over the grid
        for i in range(len(list_of_springs)):
            x_sp, y_sp = list_of_springs[i].startingpoint
            x_ep, y_ep = list_of_springs[i].endpoint
            self.spring_lines.append(self.ax.plot([x_sp, x_ep], [y_sp, y_ep], lw=2, color=list_of_springs[i].color, zorder=3)[0])

        for i in range(len(list_of_mass)):
            list_of_mass[i].set_diameter(y_range)
            self.mass_circles.append(plt.Circle(list_of_mass[i].position, list_of_mass[i].diameter, color=list_of_mass[i].color, zorder=4))
            self.ax.add_patch(self.mass_circles[i])

        
        for steadyBody in list_of_sbs:
            x, y = steadyBody.position
            # Calculate position of the rectangle (center)
            x_left = x - steadyBody.x_dim / 2
            y_bottom = y - steadyBody.y_dim / 2
            self.sb_rectangles.append(patches.Rectangle((x_left, y_bottom), steadyBody.x_dim, steadyBody.y_dim, color=steadyBody.color, zorder=4))
            self.ax.add_patch(self.sb_rectangles[-1])

    def update_frame(self, num):
        y = -self.sol.y
        pos = y[0:int(len(y)/2)]
        x_pos = pos[::2]
        y_pos = pos[1::2]
        list_of_springs, list_of_mass, list_of_sbs= self.list_of_object_lists

        # Ensure num is within the range of positions
        if 0 <= num <= len(y_pos[0]):

            for i in range(len(list_of_mass)):
                list_of_mass[i].move(x_pos[i][num], y_pos[i][num])
                self.mass_circles[i].set_center(list_of_mass[i].position)

            for i in range(len(list_of_sbs)):
                list_of_sbs[i].move(x_pos[i][num], y_pos[i][num])
                x_center, y_center = list_of_sbs[i].position
                width, height = list_of_sbs[i].x_dim, list_of_sbs[i].y_dim
                bottom_left = (x_center - width / 2, y_center - height / 2)
                self.sb_rectangles[i].set_xy(bottom_left)

            # for i in range(len(list_of_springs)):
            #     if list_of_springs[i].startingpoint[1] == 0:
            #         list_of_springs[i].move(list_of_springs[i].startingpoint, list_of_mass[i].position)
            #         x_sp, y_sp = list_of_springs[i].startingpoint
            #         x_ep, y_ep = list_of_springs[i].endpoint
            #         self.spring_lines[i].set_data([x_sp, x_ep], [y_sp, y_ep])
            #     else:
            #         list_of_springs[i].move(list_of_mass[i-1].position, list_of_mass[i].position)
            #         x_sp, y_sp = list_of_springs[i].startingpoint
            #         x_ep, y_ep = list_of_springs[i].endpoint
            #         self.spring_lines[i].set_data([x_sp, x_ep], [y_sp, y_ep])

            # for i in range(len(list_of_springs)):
            #     if list_of_springs[i].startingpoint[1] == 0:
            #         list_of_springs[i].move(list_of_springs[i].startingpoint, list_of_sbs[i].position)
            #         #print(list_of_springs[i].endpoint)
            #         x_sp, y_sp = list_of_springs[i].startingpoint
            #         x_ep, y_ep = list_of_springs[i].endpoint
            #         self.spring_lines[i].set_data([x_sp, x_ep],[y_sp,y_ep])
            #     else: 
            #         list_of_springs[i].move(list_of_sbs[i-1].position, list_of_sbs[i].position)
            #         #print(list_of_springs[i].startingpoint)
            #         #print(list_of_springs[i].endpoint)
            #         x_sp, y_sp = list_of_springs[i].startingpoint
            #         x_ep, y_ep = list_of_springs[i].endpoint
            #         self.spring_lines[i].set_data([x_sp, x_ep],[y_sp,y_ep])
            #         #print(list_of_springs[i])

            list_of_springs[0].move(list_of_springs[0].startingpoint, list_of_mass[0].position)
            x_sp, y_sp = list_of_springs[0].startingpoint
            x_ep, y_ep = list_of_springs[0].endpoint
            self.spring_lines[0].set_data([x_sp, x_ep],[y_sp,y_ep])

            list_of_springs[1].move(list_of_mass[0].position, list_of_sbs[0].position)
            x_sp, y_sp = list_of_springs[1].startingpoint
            x_ep, y_ep = list_of_springs[1].endpoint
            self.spring_lines[1].set_data([x_sp, x_ep],[y_sp,y_ep])
            
        time = f"{self.sol.t[num]:.2f}" 
        self.ax.set_title('Animation \nTime: '+time)