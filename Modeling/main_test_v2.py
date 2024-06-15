from sympy import Function, pprint
import sympy as sp
import newton
from matplotlib import pyplot as plt
from simsave import save_system, tex_save, load_system
import time
from numpy import array
import objects
import os
import animation
from additions import eq_to_latex, show_equations_of_motion, LoadedSystem

def create_objects():
    """
    Creates instances of Masspoint, SteadyBody, and Spring objects with specified parameters
    and initial conditions.

    :return: List containing lists of Spring and Mass objects
    :rtype: list of lists of objects
    """
    m1 = objects.Masspoint(mass=2, index=1)
    m2 = objects.Masspoint(mass=2, index=2)
    m3 = objects.Masspoint(mass=2, index=3)
    m1 = objects.SteadyBody(x_dim= 0.2, y_dim=0.1, z_dim=0.03, density=2700, index=1)
    #m2 = objects.SteadyBody(x_dim= 0.2, y_dim=0.1, z_dim=0.03, density=2700, index=2)
    #m3 = objects.SteadyBody(x_dim= 0.2, y_dim=0.1, z_dim=0.03, density=2700, index=3)
    #print("mass 2 = "+str(m2.mass))
    s1 = objects.Spring(rest_length=0.5, stiffness=100, index=1, type="linear")
    s2 = objects.Spring(rest_length=0.4, stiffness=100, index=2, type="linear")
    s3 = objects.Spring(rest_length=0.6, stiffness=100, index=3, type="linear")

    # Setting initial conditions for each object
    m1.setInitialConditions([0,-0.5], [0,0])
    m2.setInitialConditions([0,-0.9], [0,0])
    m3.setInitialConditions([0,-1.5], [0,0])

    s1.setInitialConditions(None, m1 , [0,0])
    s2.setInitialConditions(m1,  m2, [0,0])
    s3.setInitialConditions(m2,  m3, [0,0])

    list_of_mass = [m1, m2, m3]
    list_of_springs = [s1, s2, s3] 
    list_of_object_lists = [list_of_springs, list_of_mass]
 
    return list_of_object_lists

def get_list_of_all_forces(list_of_object_lists):
    """
    Calculates forces acting on each mass due to springs and the gravitaion.

    :param list_of_object_lists: List containing lists of Spring and Mass objects
    :type list_of_object_lists: list of lists of objects
    :return: List of forces in x and y directions for each mass
    :rtype: list of lists of sympy.Add or sympy.Mul
    """
    list_of_springs, list_of_mass =list_of_object_lists
    list_of_forces_all_x = []  
    list_of_forces_all_y = []

    for i in range(len(list_of_mass)):
        pos = list_of_mass[i].position 
        list_of_force_y = [list_of_mass[i].force()]  #initializes the list of force for each mass with the gravitational force of each mass
        list_of_force_x = []
        #print(i)
        match list_of_mass[i].type:
            case "masspoint":
                for j in range(len(list_of_springs)): 
                    # compares the startingpoint of all springs with the position of the mass
                    # if the points are the same, this means that the spring is below the mass and the force is positiv
                    if pos == list_of_springs[j].startingpoint: 
                        Fx,Fy =list_of_springs[j].force(list_of_mass[j-1], list_of_mass[j])
                        list_of_force_y.append(Fy)
                        list_of_force_x.append(Fx)
                    # if the points are the same, this means that the spring is above the mass and the force is negativ
                    elif pos == list_of_springs[j].endpoint:
                        # if j=0, this means that this is the first spring in the system which is usally attached to the origin instead of a mass.
                        # Therefore the value of the first argument should be None in this case.
                        if j == 0:
                            Fx,Fy =list_of_springs[j].force(None, list_of_mass[j])
                            list_of_force_y.append(-Fy)
                            list_of_force_x.append(-Fx)
                        else:
                            Fx,Fy = list_of_springs[j].force(list_of_mass[j-1], list_of_mass[j])
                            list_of_force_y.append(-Fy)
                            list_of_force_x.append(-Fx)
            
            case "steady body":
                for j in range(len(list_of_springs)): 
                    # compares the startingpoint of all springs with the position of the mass where the spring should be attached
                    # if the points are the same, this means that the spring is below the mass and the force is positiv
                    if [pos[0],pos[1]-list_of_mass[i].y_dim/2] == list_of_springs[j].startingpoint: 
                        # in the computed point of the conection is a - sign because the KOS for the simulation is inverted to the KOS for the animation
                        Fx,Fy =list_of_springs[j].force(list_of_mass[j-1], list_of_mass[j])
                        list_of_force_y.append(Fy)
                        list_of_force_x.append(Fx)
                    # if the points are the same, this means that the spring is above the mass and the force is negativ
                    elif [pos[0],pos[1]+list_of_mass[i].y_dim/2] == list_of_springs[j].endpoint:
                        # in the computed point of the conection is a + sign because the KOS for the simulation is inverted to the KOS for the animation
                        # if j=0, this means that this is the first spring in the system which is usally attached to the origin instead of a mass.
                        # Therefore the value of the first argument should be None in this case.
                        if j == 0:
                            Fx,Fy =list_of_springs[j].force(None, list_of_mass[j])
                            list_of_force_y.append(-Fy)
                            list_of_force_x.append(-Fx)
                        else:
                            # list_of_force_y.append(-list_of_springs[j].force(list_of_springs[j-1].yt))
                            Fx,Fy = list_of_springs[j].force(list_of_mass[j-1], list_of_mass[j])
                            list_of_force_y.append(-Fy)
                            list_of_force_x.append(-Fx)
                    
        list_of_forces_all_y.append(list_of_force_y) # write the list of forces attached to each mass in the list of all forces
        list_of_forces_all_x.append(list_of_force_x)
    #print("forces x:"+str(list_of_forces_all_x))
    #print("forces y:"+str(list_of_forces_all_y))

    return [list_of_forces_all_x, list_of_forces_all_y]

def run_simulation(list_of_object_lists, simulation_points=10001):
    """
    Runs simulation using Newton mechanics for the given system of masses and springs.

    :param list_of_object_lists: List containing lists of Spring and Mass objects
    :type list_of_object_lists: list of lists of objects
    :param simulation_points: Number of points to simulate, default is 10001
    :type simulation_points: int
    :return: Result of simulation and system object
    :rtype: tuple
    """

    list_of_springs, list_of_mass =list_of_object_lists

    # list of masses
    sym_mass_list = [mass.sym_mass for mass in list_of_mass]
    #print(sym_mass_list)

    #creating the list of forces attached to each mass
    list_of_forces_all_x, list_of_forces_all_y = get_list_of_all_forces(list_of_object_lists)

    # Setup system with Newton mechanics
    system = newton.Mechanics()

    # add masses
    for i in range(len(list_of_mass)):
        system.add_mass(name=str(sym_mass_list[i]), mass=sym_mass_list[i]) # add mass i to the system  

    for i in range(len(sym_mass_list)):
        system.add_force(str(sym_mass_list[i]), (sum(list_of_forces_all_x[i]), 'x'))
        #system.add_force(str(sym_mass_list[i]), (0, 'x'))
        system.add_force(str(sym_mass_list[i]), (sum(list_of_forces_all_y[i]), 'y'))

    #create dictionary of parameter values of each mass 
    param_values_mass = {}
    for mass in list_of_mass:
        param_values_mass.update(mass.get_param_values())
    #print(param_values_mass)

    #create dictionary of parameter values of each spring 
    param_values_spring ={}
    for spring in list_of_springs:
        param_values_spring.update(spring.get_param_values())
        #print(param_values_spring)

    g = sp.Symbol('g')
    # ** unpacks the dictionary into positional arguments  
    system.param_values = {**param_values_mass, **param_values_spring, g: 9.81}
    #print({**param_values_mass, **param_values_spring, g: 9.81})

    # geometric relationships
    # distance between global coordinate origin and first mass
    # system.generate_constraint("link", 'm1', 'm1', l1_0)
    # distance between first mass and second mass
    # system.generate_constraint("link", 'm1', 'm2', l2_0)

    # print(system.constraints)

    # get equation of motion (only required for displaying purposes), not needed for simulation
    equations = system.generate_equations()
    sub_equations = system.substitute_parameters(equations, system.param_values)
    rhs_eq = system.rhs_of_equation(sub_equations)

    # create list of inital conditions
    # format of z0: [x1, y1, x2, y2, ..., x1_dot, y1_dot, x2_dot, y2_dot, ...]
    z0 = []
    for mass in list_of_mass:
        z0.append(-mass.position[0])
        z0.append(-mass.position[1])

    for mass in list_of_mass:
        z0 += mass.velocity

    #print(z0)

    t_span = (0, 10)

    start = time.time()
    res = system.simulate(system.param_values, z0, t_span, simulation_points)
    end = time.time()
    print("Duration of simulation: ", end - start, "s.")
    
    return res,system

def save_created_system(name, res, system):
    """
    Saves the simulation results and system parameters to a NetCDF file with a given name.

    :param name: Name of the file to save (without extension)
    :type name: str
    :param res: Simulation results to save
    :type res: scipy.integrate.OdeSolution
    :param system: System object containing simulation parameters and equations
    :type system: Newtonian mechanics system object
    """
    print("Saving data ...")
    savepath = os.path.dirname(os.path.realpath(__file__))+"\data\\"+ name + ".nc"
    print(savepath)
    save_system(savepath, res, system)
    print("Data saved.")

def load_list(name):
    """
    Loads a system configuration and initial conditions from a saved file, reconstructing Masspoint, Steady Body, and Spring objects for animation.

    :param name: Name of the file to load (without extension)
    :type name: str
    :return: List containing reconstructed Spring and Mass objects
    :rtype: list of lists of objects
    """
    # I think we both know how terrible this function is but we have a deadline so here we go
    savepath = os.path.dirname(os.path.realpath(__file__)) + "\data\\" + name + ".nc"
    loaded_sys = load_system(savepath)

    # load simulation results to get inital conditions
    load_res = loaded_sys['results']
    res_pos = load_res[:int(len(load_res[:])/2)]
    res_vel = load_res[int(len(load_res[:])/2):]

    loaded_params = loaded_sys['system']['param_values']
    params_keys = [str(key) for key in list(loaded_params.keys())]
    # print(loaded_params)

    # find Masspoints, Steady Body and Spring to reconstruct the list_of_object_lists for animation
    masspoints = []
    steady_bodies = []
    springs = []
    masses = {}

    # Identify Masspoints, Steady Bodies, and Springs based on loaded parameters
    # iterate through the list to check each pair of neighboring elements
    for i in range(len(params_keys) - 2):
        current_item = params_keys[i]
        next_item = params_keys[i + 1]
        second_next_item = params_keys[i + 2]

        if current_item.startswith('m') and next_item.startswith('l') and second_next_item.startswith("h"):
            steady_bodies.append(i)
            masses[f'sb{i}'] = i
        elif current_item.startswith('m'):
            masspoints.append(i)
            masses[f'm{i}'] = i
        elif current_item.startswith('l') and next_item.startswith('k'):
            springs.append(i+1)

    # reconstruct Masspoints objects and Steady Bodies objects
    list_of_mass = []
    i = 1
    for key in masses:
        if key.startswith('m'):
            m = objects.Masspoint(mass=float(loaded_params[sp.Symbol(params_keys[masses[key]])]), index=i)
            list_of_mass.append(m)
            i = i + 1
        elif key.startswith('sb'):
            dens = (loaded_params[sp.Symbol(params_keys[masses[key]])] /
                    (loaded_params[sp.Symbol(params_keys[masses[key] + 1])] *
                    loaded_params[sp.Symbol(params_keys[masses[key] + 2])] *
                    loaded_params[sp.Symbol(params_keys[masses[key] + 3])]))
            b = objects.SteadyBody(x_dim=float(loaded_params[sp.Symbol(params_keys[masses[key] + 1])]),
                                   y_dim=float(loaded_params[sp.Symbol(params_keys[masses[key] + 2])]),
                                   z_dim=float(loaded_params[sp.Symbol(params_keys[masses[key] + 3])]),
                                   density=float(dens), index=i)

            list_of_mass.append(b)
            i = i + 1
        else:
            print(f'Unknown key{key}')


    # set initial conditions of masses
    j = 0
    for m in list_of_mass:
        m.setInitialConditions([float(res_pos[j][0]), -float(res_pos[j+1][0])], [float(res_vel[j][0]), float(res_vel[j+1][0])])
        j = j + 2
    # print(list_of_mass)

    # reconstruct Spring Objects
    list_of_spring = []
    n = 1
    for spring in springs:
        s = objects.Spring(rest_length=float(loaded_params[sp.Symbol(params_keys[spring-1])]),
                           stiffness=float(loaded_params[sp.Symbol(params_keys[spring])]),
                           index=n, type="linear")
        list_of_spring.append(s)
        n = n + 1

    # set initial conditions of springs
    m = 0
    for s in list_of_spring:
        if m == 0:
            s.setInitialConditions(None, list_of_mass[m],[0,0])
        else:
            s.setInitialConditions(list_of_mass[m-1], list_of_mass[m],[0,0])
        m = m + 1

    return [list_of_spring, list_of_mass]

def load_sys(name):
    """
    Loads a system configuration and equations of motion from a saved file.

    :param name: Name of the file to load (without extension)
    :type name: str
    :return: LoadedSystem object containing time, results, and loaded system
    :rtype: LoadedSystem
    """
    savepath = os.path.dirname(os.path.realpath(__file__)) + "\\data\\" + name + ".nc"
    data = load_system(savepath)

    # construct equations of motion with saved data
    param_val = data['system']['param_values']
    masses = data['system']['masses']
    coordinates = data['system']['coordinates']
    forces = data['system']['forces']
    force_list = [f for f in forces]

    # set up system with loaded data
    loaded_system = newton.Mechanics()
    i = 0
    for m in masses:
        loaded_system.add_mass(m, mass=sp.symbols(m))
        force = force_list[i]
        for f in force:
            loaded_system.add_force(m, f)
        i += 1

    loaded_system.param_values = param_val
    equ = loaded_system.generate_equations()
    sub_eq = loaded_system.substitute_parameters(equ, loaded_system.param_values)
    eq_rhs = loaded_system.rhs_of_equation(sub_eq)
    # generate latex notion of equations of motion
    eqm = eq_to_latex(loaded_system)

    # load simulation data
    t = data['time']
    y = array(data['results'][:])

    results = LoadedSystem(t, y, loaded_system)
    return results

def plot_results(res,ax):
    """
    Plots the position of masses over time from the simulation results.

    :param res: Simulation results containing time and position data
    :type res: scipy.integrate.OdeSolution
    :param ax: Matplotlib axis object to plot on
    :type ax: matplotlib.axes.Axes
    """
    t = res.t
    y = res.y
    pos = y[0:int(len(y)/2)]
    x_pos = pos[::2]
    y_pos = pos[1::2]

    # Plot results
    for i in range(len(y_pos)):
        ax.plot(t, y_pos[i], label='Position of Mass '+str(i+1)+ '(m)')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.set_title('Spring Mass Oscillator')
    ax.legend()
    ax.grid(True)

# plot equations
def generate_latex(system):
    """
    Generates LaTeX representation of equations of motion for the given system.

    :param system: System object containing simulation parameters and equations
    :type system: Newtonian mechanics system object
    """
    # generate latex notion of equations of motion
    eqm = eq_to_latex(system)

    # plot/show equations of motion
    show_equations_of_motion(eqm)

    #path and name of the saved file
    savepath_equation = os.path.dirname(os.path.realpath(__file__))+"\data\\tex_equation"
    tex_save(savepath_equation, system)


def main():
    # Run the simulation
    list_of_object_lists=create_objects()
    res, system = run_simulation(list_of_object_lists, simulation_points=100001)

    #save system
    save_created_system("test3", res, system)

    # load list_of_object_lists with saved data
    loaded_list_of_object_lists = load_list('test3')

    # load system and simulation data
    loaded_res = load_sys('test3')
    loaded_system = loaded_res.loaded_system


    #plot results     
    fig = plt.figure (figsize=(10,4))
    ax1 = fig.add_subplot(1,1,1)
    canvas = fig.canvas
    plot_results(res, ax1)
    generate_latex(system)
    canvas.draw()
    plt.show(block=False)

    # animation
    ani=animation.animation(loaded_res, loaded_list_of_object_lists,skip_sim_steps=150)
    plt.show(block=True)

if __name__ == "__main__":
    main()