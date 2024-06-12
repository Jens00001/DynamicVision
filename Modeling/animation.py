import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
    print("Länge y_0: "+str(len(y[0])))
    print(type(len(y[0])))
    list_of_springs, list_of_mass = list_of_object_lists

    y_range = y_max - y_min

    # Create figure and axis
    fig, ax = plt.subplots()
    #ax.set_xlim(y_min - y_buffer, y_max + y_buffer)
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
                ax.add_patch(mass_circle[-1])

            case "steady body":
                x, y = mass.position
                # Calculate position of the rectangle (center)
                x_left = x - mass.x_dim / 2
                y_bottom = y - mass.y_dim / 2
                sb_rectangles.append(patches.Rectangle((x_left, y_bottom), mass.x_dim, mass.y_dim, color=mass.color, zorder=4))
                ax.add_patch(sb_rectangles[-1])

    # for i in range(len(list_of_mass)):
    #     list_of_mass[i].set_diameter(y_range)
    #     mass_circle.append(plt.Circle(list_of_mass[i].position, list_of_mass[i].diameter, color = list_of_mass[i].color, zorder=4))
    #     ax.add_patch(mass_circle[i])

    # for steadyBody in list_of_sbs:
    #     x, y = steadyBody.position
    #     # Calculate position of the rectangle (center)
    #     x_left = x - steadyBody.x_dim / 2
    #     y_bottom = y - steadyBody.y_dim / 2
    #     sb_rectangles.append(patches.Rectangle((x_left, y_bottom), steadyBody.x_dim, steadyBody.y_dim, color=steadyBody.color, zorder=4))
    #     ax.add_patch(sb_rectangles[-1])
    #plt.show()
    # springline1, = ax.plot([list_of_springs[0].startingpoint[0], list_of_springs[0].endpoint[0]],[list_of_springs[0].startingpoint[1], list_of_springs[0].endpoint[1]],lw=2)
    # springline2, = ax.plot([list_of_springs[1].startingpoint[0], list_of_springs[1].endpoint[0]],[list_of_springs[1].startingpoint[1], list_of_springs[1].endpoint[1]],lw=2)
    # masscircle1 = plt.Circle(list_of_mass[0].position, 0.1, color='r')
    # ax.add_patch(masscircle1)
    # masscircle2 = plt.Circle(list_of_mass[1].position, 0.1, color='r')
    # ax.add_patch(masscircle2)

    # Function to update the animation
    
    def update_system(num): 

        sb_index = 0
        mp_index = 0
        for i in range(len(list_of_mass)):
            match list_of_mass[i].type:
                case "masspoint":
                    list_of_mass[i].move(x_pos[i][num],y_pos[i][num])
                    mass_circle[mp_index].set_center(list_of_mass[i].position)
                    mp_index += 1
                    #print(list_of_mass[i].position)

                case "steady body":
                    list_of_mass[i].move(x_pos[i][num], y_pos[i][num])
                    x_center, y_center = list_of_mass[i].position
                    width, height = list_of_mass[i].x_dim, list_of_mass[i].y_dim
                    bottom_left = (x_center - width / 2, y_center - height / 2)
                    sb_rectangles[sb_index].set_xy(bottom_left)
                    sb_index += 1
        
        for i in range(len(list_of_springs)):
            if list_of_springs[i].startingpoint[1] == 0:
                list_of_springs[i].move(None, list_of_mass[i])
                x_sp, y_sp = list_of_springs[i].startingpoint
                x_ep, y_ep = list_of_springs[i].endpoint
                spring_line[i][0].set_data([x_sp, x_ep], [y_sp, y_ep])
            else:
                list_of_springs[i].move(list_of_mass[i-1], list_of_mass[i])
                x_sp, y_sp = list_of_springs[i].startingpoint
                x_ep, y_ep = list_of_springs[i].endpoint
                spring_line[i][0].set_data([x_sp, x_ep], [y_sp, y_ep])

        # list_of_springs[0].move(list_of_springs[0].startingpoint, list_of_mass[0].position)
        # x_sp, y_sp = list_of_springs[0].startingpoint
        # x_ep, y_ep = list_of_springs[0].endpoint
        # spring_line[0][0].set_data([x_sp, x_ep],[y_sp,y_ep])

        # list_of_springs[1].move(list_of_mass[0].position, list_of_sbs[0].position)
        # x_sp, y_sp = list_of_springs[1].startingpoint
        # x_ep, y_ep = list_of_springs[1].endpoint
        # spring_line[1][0].set_data([x_sp, x_ep],[y_sp,y_ep])

            
        


        time = f"{sol.t[num]:.2f}" 
        plt.title('Animation \nTime: '+time)
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

            

    # Create animation range(0, len(y[0]), skip_sim_steps)
    ani = matplotlib.animation.FuncAnimation(fig, update_system, frames= range(0, len(t), skip_sim_steps), interval=dt*100,repeat=True, cache_frame_data=True) # intervall is the delay in ms between frames
    
    #plt.title('Animation\n Time:'+str(3))
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()
   