import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Animation:
    """
    Class for creating an animation of a system of springs and masses.

    :param sol: Solution object containing the time, position and velocity data
    :type sol: scipy.integrate.OdeSolution
    :param list_of_object_lists: List containing lists of Spring and Mass objects
    :type list_of_object_lists: list of lists of objects
    :param ax: Matplotlib axis object to plot the animation
    :type ax: matplotlib.axes.Axes

    :ivar sol: Solution object containing the time, position and velocity data
    :vartype sol: scipy.integrate.OdeSolution
    :ivar list_of_object_lists: List containing lists of Spring and Mass objects
    :vartype list_of_object_lists: list of lists of objects
    :ivar ax: Matplotlib axis object to plot the animation
    :vartype ax: matplotlib.axes.Axes
    :ivar spring_lines: List to store the plotted spring lines in the animation
    :vartype spring_lines: list of matplotlib.lines.Line2D
    :ivar mass_circles: List to store the plotted mass circles in the animation
    :vartype mass_circles: list of matplotlib.patches.Circle
    :ivar sb_rectangles: List to store the plotted steady body rectangles in the animation
    :vartype sb_rectangles: list of matplotlib.patches.Rectangle
    """

    def __init__(self, sol, list_of_object_lists, ax):
        """
        Initialize the Animation instance.

        :param sol: Solution object containing the time, position and velocity data
        :type sol: scipy.integrate.OdeSolution
        :param list_of_object_lists: List containing lists of Spring and Mass objects
        :type list_of_object_lists: list of lists of objects
        :param ax: Matplotlib axis object to plot the animation
        :type ax: matplotlib.axes.Axes
        """
        self.sol = sol
        self.list_of_object_lists = list_of_object_lists
        self.ax = ax
        self.spring_lines = []  # List to store spring line objects for updating animation
        self.mass_circles = []  # List to store mass circle objects for updating animation
        self.sb_rectangles = [] # List to store steady body rectangle objects for updating animation
        self.init_animation()   # Call initialization method to set up the initial animation

    def init_animation(self):
        """
        Initialize the animation by setting up the plot with springs and masses in the starting configuration, 
        which refers to the inital conditions of the Spring and Mass objects.
        """
        t = self.sol.t
        y = -self.sol.y    # - sign because the KOS is inverted in the simulated data 
        pos = y[0:int(len(y)/2)]
        x_pos = pos[::2]
        x_max = max((max(x) for x in x_pos))    #finds the maximum value of all x positions
        x_min = min((min(x) for x in x_pos))    #finds the minimum value of all x positions
        y_pos = pos[1::2]
        y_max = max((max(y) for y in y_pos))    #finds the maximum value of all y positions
        y_min = min((min(y) for y in y_pos))    #finds the minimum value of all y positions
        y_range = y_max - y_min

        # Set plot limits and aspect ratio
        self.ax.set_ylim(y_min - 3, y_max + 3)
        self.ax.set_xlim(x_min - 3, x_max + 3)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_title('Animation')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        list_of_springs, list_of_mass = self.list_of_object_lists

        # zorder is use in matplotlib to control the drawing order, the grid have a zorder of 2.5 by default
        # we want that the masses are plotted above the spring lines, so the zorder of the masses must have a higer values than the zorder of the spring lines
        # and both zorders must have a higher value than the zorder of the grid, because we want that the objects are shown over the grid

        # Create springs
        for i in range(len(list_of_springs)):
            x_sp, y_sp = list_of_springs[i].startingpoint
            x_ep, y_ep = list_of_springs[i].endpoint
            self.spring_lines.append(self.ax.plot([x_sp, x_ep], [y_sp, y_ep], lw=2, color=list_of_springs[i].color, zorder=3)[0])

        # Create masses
        for mass in list_of_mass:
            match mass.type:
                case "masspoint":
                    mass.set_diameter(y_range)
                    self.mass_circles.append(plt.Circle(mass.position, mass.diameter, color = mass.color, zorder=4))
                    self.ax.add_patch(self.mass_circles[-1])    # Add mass circle to the plot as a patch object

                case "steady body":
                    x, y = mass.position
                    # calculate position of the rectangle's bottom-left corner
                    x_left = x - mass.x_dim / 2
                    y_bottom = y - mass.y_dim / 2
                    self.sb_rectangles.append(patches.Rectangle((x_left, y_bottom), mass.x_dim, mass.y_dim, color=mass.color, zorder=4))
                    self.ax.add_patch(self.sb_rectangles[-1])    # Add steady body rectangle to the plot as a patch object

    def update_frame(self, num):
        """
        Update the animation frame based on the current time step.

        :param num: Current time step index
        :type num: int
        """
        y = -self.sol.y
        pos = y[0:int(len(y)/2)]
        x_pos = pos[::2]
        y_pos = pos[1::2]
        list_of_springs, list_of_mass = self.list_of_object_lists

        # Ensure num is within the range of positions
        if 0 <= num <= len(y_pos[0]):

            sb_index = 0
            mp_index = 0
            for i in range(len(list_of_mass)):
                match list_of_mass[i].type:
                    case "masspoint":
                        list_of_mass[i].move(x_pos[i][num],y_pos[i][num])   # Move masspoint to new coordinates
                        self.mass_circles[mp_index].set_center(list_of_mass[i].position)    # Update mass circle position
                        mp_index += 1
                        #print(list_of_mass[i].position)

                    case "steady body":
                        list_of_mass[i].move(x_pos[i][num], y_pos[i][num])  # Move steady body to new coordinates
                        x_center, y_center = list_of_mass[i].position
                        width, height = list_of_mass[i].x_dim, list_of_mass[i].y_dim
                        bottom_left = (x_center - width / 2, y_center - height / 2)
                        self.sb_rectangles[sb_index].set_xy(bottom_left)    # Update steady body rectangle position
                        sb_index += 1
                    
            for i in range(len(list_of_springs)):
                if list_of_springs[i].startingpoint[1] == 0:
                    list_of_springs[i].move(None, list_of_mass[i])
                    x_sp, y_sp = list_of_springs[i].startingpoint
                    x_ep, y_ep = list_of_springs[i].endpoint
                    self.spring_lines[i].set_data([x_sp, x_ep], [y_sp, y_ep])   # Update spring line coordinates
                else:
                    list_of_springs[i].move(list_of_mass[i-1], list_of_mass[i])
                    x_sp, y_sp = list_of_springs[i].startingpoint
                    x_ep, y_ep = list_of_springs[i].endpoint
                    self.spring_lines[i].set_data([x_sp, x_ep], [y_sp, y_ep])   # Update spring line coordinates
        
        # Update plot title with current time   
        time = f"{self.sol.t[num]:.2f}" 
        self.ax.set_title('Animation \nTime: '+time)