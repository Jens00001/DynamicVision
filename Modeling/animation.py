import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation 


def animation(sol, list_of_object_lists):
    t = sol.t
    dt = t[-1]/ len(t)
    y = sol.y
    pos = y[::2]
    list_of_springs, list_of_mass = list_of_object_lists
    # Create figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal')
    ax.grid()

    # Create spring lines
    spring_line = []
    for i in range(len(list_of_springs)):
        x_sp, y_sp = list_of_springs[i].startingpoint
        x_ep, y_ep = list_of_springs[i].endpoint
        spring_line.append(ax.plot([],[], lw=2))

    # Create mass 
    mass_circle = []
    for i in range(len(list_of_mass)):
        mass_circle.append(plt.Circle(list_of_mass[i].position, list_of_mass[i].diameter, color = list_of_springs[i].color))
        ax.add_patch(mass_circle[i])

    # Function to update the animation
    def update_system(num):

        #TODO geometric relations
        for i in range(len(list_of_springs)):
            if list_of_springs[i].startingpoint[1] == 0:
                list_of_springs[i].move(pos[0], list_of_springs[i].startingpoint)
            else: 
                list_of_springs[i].move(pos[1], list_of_mass[i].position)

        for i in range(len(list_of_mass)):
            list_of_mass[i].move(pos[i], list_of_springs[i].endpoint)

        for i in range(len(list_of_springs)):
            x_sp, y_sp = list_of_springs[i].startingpoint
            x_ep, y_ep = list_of_springs[i].endpoint
            spring_line[i].set_data = ([x_sp, x_ep],[y_sp,y_ep])

        for i in range(len(list_of_mass)):
            mass_circle[i].set_center(mass_circle[i].position)


    # Create animation
    ani = matplotlib.animation.FuncAnimation(fig, update_system, frames=len(y[0]), interval=dt*1000, repeat=True) # intervall is the delay in ms between frames

    plt.title('Animation')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()
