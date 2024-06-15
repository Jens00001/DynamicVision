import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation 

def animation(sol, list_of_object_lists,skip_sim_steps=150):
    '''
    Function to create an animation of a system of springs and masses.

    :param sol: Solution object containing the time, position, and velocity data from the simulation (output of solve_ivp())
    :type sol: scipy.integrate.OdeSolution
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
    # print("Länge y_0: "+str(len(y[0])))
    # print(type(len(y[0])))
    list_of_springs, list_of_mass = list_of_object_lists

    y_range = y_max - y_min

    # Create figure and axis
    fig, ax = plt.subplots()
    ax.set_ylim(y_min - 3, y_max + 3)
    ax.set_xlim(x_min - 3, x_max + 3)
    ax.set_aspect('equal')
    ax.grid()

    # Create spring lines
    spring_line = []
    for i in range(len(list_of_springs)):
        x_sp, y_sp = list_of_springs[i].startingpoint
        x_ep, y_ep = list_of_springs[i].endpoint
        spring_line.append(ax.plot([x_sp,x_ep],[y_sp,y_ep], lw=2, color = list_of_springs[i].color, zorder=3))

    # Create mass 
    mass_circle = []
    sb_rectangles = []

    for mass in list_of_mass:
        match mass.type:
            case "masspoint":
                mass.set_diameter(y_range)
                mass_circle.append(plt.Circle(mass.position, mass.diameter, color = mass.color, zorder=4))
                ax.add_patch(mass_circle[-1])    # Add mass circle to plot as a patch object

            case "steady body":
                x, y = mass.position
                # # calculate position of the rectangle's bottom-left corner
                x_left = x - mass.x_dim / 2
                y_bottom = y - mass.y_dim / 2
                sb_rectangles.append(patches.Rectangle((x_left, y_bottom), mass.x_dim, mass.y_dim, color=mass.color, zorder=4))
                ax.add_patch(sb_rectangles[-1]) # Add steady body rectangle to plot as a patch object


    # Function to update the animation
    def update_system(num): 

        sb_index = 0
        mp_index = 0
        for i in range(len(list_of_mass)):
            match list_of_mass[i].type:
                case "masspoint":
                    list_of_mass[i].move(x_pos[i][num],y_pos[i][num])   # Move masspoint to new coordinates
                    mass_circle[mp_index].set_center(list_of_mass[i].position)  # Update mass circle position
                    mp_index += 1
                    #print(list_of_mass[i].position)

                case "steady body":
                    list_of_mass[i].move(x_pos[i][num], y_pos[i][num])  # Move steady body to new coordinates
                    x_center, y_center = list_of_mass[i].position
                    width, height = list_of_mass[i].x_dim, list_of_mass[i].y_dim
                    bottom_left = (x_center - width / 2, y_center - height / 2)
                    sb_rectangles[sb_index].set_xy(bottom_left)  # Update steady body rectangle position
                    sb_index += 1
        
        for i in range(len(list_of_springs)):
            if list_of_springs[i].startingpoint[1] == 0:
                list_of_springs[i].move(None, list_of_mass[i])
                x_sp, y_sp = list_of_springs[i].startingpoint
                x_ep, y_ep = list_of_springs[i].endpoint
                spring_line[i][0].set_data([x_sp, x_ep], [y_sp, y_ep])  # Update spring line coordinates
            else:
                list_of_springs[i].move(list_of_mass[i-1], list_of_mass[i])
                x_sp, y_sp = list_of_springs[i].startingpoint
                x_ep, y_ep = list_of_springs[i].endpoint
                spring_line[i][0].set_data([x_sp, x_ep], [y_sp, y_ep])  # Update spring line coordinates

        # Update plot title with current time
        time = f"{sol.t[num]:.2f}" 
        plt.title('Animation \nTime: '+time)


    # Create animation 
    # intervall is the delay in ms between frames
    ani = matplotlib.animation.FuncAnimation(fig, update_system, frames= range(0, len(t), skip_sim_steps), interval=dt*100,repeat=True, cache_frame_data=True) 
    
    #plt.title('Animation\n Time:'+str(3))
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()  #Display animation
   