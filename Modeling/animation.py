import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation 

def animation(sol, list_of_object_lists,skip_sim_steps=150):
    '''
    :param sol: solution of the simulation of the system (See documentation of solve_ivp())
    :type Bunch object:
    :param list_of_object_lists: a list which contains lists of objects created in the system
    :type list_of_object_lists: list
    :param skip_sim_steps: value of how many simulated steps are skiped before the next update of the animation, in case the animation is to slow because of too many frames
    :type skip_sim_steps: int
    '''
    t = sol.t
    dt = t[-1]/ len(t)
    y = - sol.y # - sign because the KOS is inverted in the simulated data 
    pos = y[0:int(len(y)/2)]
    x_pos = pos[::2]
    x_max = max((max(x) for x in x_pos)) #finds the maximum value of all x positions
    x_min = min((min(x) for x in x_pos)) #finds the minimum value of all x positions
    y_pos = pos[1::2]
    y_max = max((max(y) for y in y_pos)) #finds the maximum value of all y positions
    y_min = min((min(y) for y in y_pos)) #finds the minimum value of all y positions
    #print(pos)
    list_of_springs, list_of_mass = list_of_object_lists

    # Create figure and axis
    fig, ax = plt.subplots()
    #ax.set_xlim(y_min - y_buffer, y_max + y_buffer)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(x_min - 3, x_max + 3)
    ax.set_aspect('equal')
    ax.grid()

    # Create spring lines
    spring_line = []
    for i in range(len(list_of_springs)):
        x_sp, y_sp = list_of_springs[i].startingpoint
        x_ep, y_ep = list_of_springs[i].endpoint
        spring_line.append(ax.plot([x_sp,x_ep],[y_sp,y_ep], lw=2, color = list_of_springs[i].color))

    # Create mass 
    mass_circle = []
    for i in range(len(list_of_mass)):
        mass_circle.append(plt.Circle(list_of_mass[i].position, list_of_mass[i].diameter, color = list_of_mass[i].color))
        ax.add_patch(mass_circle[i])

    # springline1, = ax.plot([list_of_springs[0].startingpoint[0], list_of_springs[0].endpoint[0]],[list_of_springs[0].startingpoint[1], list_of_springs[0].endpoint[1]],lw=2)
    # springline2, = ax.plot([list_of_springs[1].startingpoint[0], list_of_springs[1].endpoint[0]],[list_of_springs[1].startingpoint[1], list_of_springs[1].endpoint[1]],lw=2)
    # masscircle1 = plt.Circle(list_of_mass[0].position, 0.1, color='r')
    # ax.add_patch(masscircle1)
    # masscircle2 = plt.Circle(list_of_mass[1].position, 0.1, color='r')
    # ax.add_patch(masscircle2)

    # Function to update the animation
    
    def update_system(num): 
           
        for i in range(len(list_of_mass)):
            list_of_mass[i].move(y_pos[i][num],x_pos[i][num])
            mass_circle[i].set_center(list_of_mass[i].position)
            #print(list_of_mass[i].position)

        for i in range(len(list_of_springs)):
            if list_of_springs[i].startingpoint[1] == 0:
                list_of_springs[i].move(list_of_springs[i].startingpoint, list_of_mass[i].position)
                #print(list_of_springs[i].endpoint)
                x_sp, y_sp = list_of_springs[i].startingpoint
                x_ep, y_ep = list_of_springs[i].endpoint
                spring_line[i][0].set_data([x_sp, x_ep],[y_sp,y_ep])
            else: 
                list_of_springs[i].move(list_of_mass[i-1].position, list_of_mass[i].position)
                #print(list_of_springs[i].startingpoint)
                #print(list_of_springs[i].endpoint)
                x_sp, y_sp = list_of_springs[i].startingpoint
                x_ep, y_ep = list_of_springs[i].endpoint
                spring_line[i][0].set_data([x_sp, x_ep],[y_sp,y_ep])
                #print(list_of_springs[i])

        # list_of_springs[0].move(-x_pos[0][num],[0,0])
        # x_sp1, y_sp1 = list_of_springs[0].startingpoint
        # x_ep1, y_ep1 = list_of_springs[0].endpoint
        # spring_line[0][0].set_data([x_sp1, x_ep1],[y_sp1,y_ep1])

        # list_of_springs[1].move(-x_pos[1][num],list_of_springs[0].endpoint)
        # x_sp2, y_sp2 = list_of_springs[1].startingpoint
        # x_ep2, y_ep2 = list_of_springs[1].endpoint
        # spring_line[1][0].set_data([x_sp2, x_ep2],[y_sp2,y_ep2])

        # list_of_mass[0].move(list_of_springs[0].endpoint)
        # mass_circle[0].set_center(list_of_mass[0].position)

        # list_of_mass[1].move(list_of_springs[1].endpoint)
        # mass_circle[1].set_center(list_of_mass[1].position)

            

    # Create animation
    ani = matplotlib.animation.FuncAnimation(fig, update_system, frames=range(0, len(y[0]), skip_sim_steps), interval=dt*100, repeat=False, cache_frame_data=True) # intervall is the delay in ms between frames
    
    plt.title('Animation')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()
   