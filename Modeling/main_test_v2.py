from sympy import Function, pprint
import sympy as sp
import newton
from matplotlib import pyplot as plt
from simsave import save_system, tex_save
import time
from numpy import array
import objects
import create_objects
import os
import animation

def preview(expr, **kwargs):
    """
    Auxiliary function for "nice" display of extensive expressions (in LaTeX)
    """
    import matplotlib.pyplot as plt
    latex_str = "$ %s $" % sp.latex(expr, **kwargs)
    latex_str = latex_str.replace("operatorname", "mathrm")
    plt.figure(figsize=(12, 5))  # 12x5 Zoll
    plt.text(0.5, 0.5, latex_str, fontsize=30, horizontalalignment="center")
    plt.axis("off")
    plt.show(block=False)


initializeObjects = "manual" 
match initializeObjects:
    case "manual":
        list_of_springs = [objects.Spring(startingpoint=[0,0], rest_length=0.5, stiffness=10, index=1), objects.Spring(startingpoint=[0,-0.5], rest_length=0.4, stiffness=15, index=2),
                           objects.Spring(startingpoint=[0,-0.9], rest_length=0.6, stiffness=5, index=3)]
        list_of_mass = [objects.Mass(position=[0,-0.5],mass=1, diameter= 0.2,index=1), objects.Mass(position=[0,-0.9],mass=2, diameter= 0.2,index=2), 
                        objects.Mass(position=[0,-1.5],mass=0.5, diameter= 0.2, index=3)]
        list_of_object_lists = [list_of_springs, list_of_mass]
        
    case "with_create_objects":
        list_of_object_lists= create_objects.create_objects("Value") # enter stop as object to stop the creating process
        list_of_springs, list_of_mass = list_of_object_lists
        s1 = list_of_springs[0]
        m1 = list_of_mass[0]

# coordinate direction of the corresponding forces (not needed, class newton.Mechanics generates coordinates)
yt = [mass.yt for mass in list_of_mass]
# print(yt)

# list of masses
sym_mass_list = [mass.sym_mass for mass in list_of_mass]
# print(sym_mass_list)

#list of angles (not needed)
# angle_list = [spring.angle for spring in list_of_springs]

#creating the list of forces attached to each mass
list_of_forces_all = []  
for mass in list_of_mass:
    pos = mass.position 
    list_of_force = [mass.force()]  #initializes the list of force for each mass with the gravitational force of each mass
    
    for j in range(len(list_of_springs)): 
        # compares the startingpoint of all springs with the position of the mass
        # if the points are the same, this means that the spring is below the mass and the force is positiv
        if pos == list_of_springs[j].startingpoint: 
            list_of_force.append(list_of_springs[j].force(list_of_springs[j-1].xt))
        # if the points are the same, this means that the spring is above the mass and the force is negativ
        elif pos == list_of_springs[j].endpoint:
            #if j=0, this means that this is the first spring and the displacement is of the spring above, which dosen't exist, is 0
            if j == 0:
                list_of_force.append(-list_of_springs[j].force(0))
            else:
                list_of_force.append(-list_of_springs[j].force(list_of_springs[j-1].xt))
                
    list_of_forces_all.append(list_of_force) # write the list of forces attached to each mass in the list of all forces
print(list_of_forces_all)

# eq_type = "Values" # Symbols oder Values
# match eq_type:
#     case "Symbols":
#         pass
#     case "Values":
#         pass

# Setup system with Newton mechanics
system = newton.Mechanics()

# add masses
for i in range(len(list_of_mass)):
    system.add_mass(name=str(sym_mass_list[i]), mass=sym_mass_list[i]) # add mass i to the system 

for i in range(len(sym_mass_list)):
    system.add_force(str(sym_mass_list[i]), (0, 'y'))
    system.add_force(str(sym_mass_list[i]), (sum(list_of_forces_all[i]), 'x'))

# # force in x direction of m1
# F_x_m1 = sum(list_of_forces_all[0])
# system.add_force(str(sym_mass_list[0]), (F_x_m1, 'x'))
# # force in y direction of m1
# F_y_m1 = 0
# system.add_force(str(sym_mass_list[0]), (F_y_m1, 'y'))

# # force in x direction of m2
# F_x_m2 = sum(list_of_forces_all[1])
# system.add_force(str(sym_mass_list[1]), (F_x_m2, 'x'))

# # force in y direction of m2
# F_y_m2 = 0
# system.add_force(str(sym_mass_list[1]), (F_y_m2, 'y'))

# # force in x direction of m3
# F_x_m3 = sum(list_of_forces_all[2])
# system.add_force(str(sym_mass_list[2]), (F_x_m3, 'x'))

# # force in y direction of m3
# F_y_m3 = 0
# system.add_force(str(sym_mass_list[2]), (F_y_m3, 'y'))


#create dictionary of parameter values of each mass 
param_values_mass = {}
for mass in list_of_mass:
    param_values_mass.update(mass.get_param_values())

#create dictionary of parameter values of each spring 
param_values_spring ={}
for spring in list_of_springs:
    param_values_spring.update(spring.get_param_values())
    #print(param_values_spring)

g = sp.Symbol('g')
# ** unpacks the dictionary into positional arguments  
param_values =  {**param_values_mass, **param_values_spring, g: 9.81}
#print(param_values)

# geometric relationships
# distance between global coordinate origin and first mass
# system.generate_constraint("link", 'm1', 'm1', l1_0)
# distance between first mass and second mass
# system.generate_constraint("link", 'm1', 'm2', l2_0)

print(system.constraints)

# get equation of motion (only required for displaying purposes), not needed for simulation
equations = system.generate_equations()
sub_equations = system.substitute_parameters(equations, param_values)
rhs_eq = system.rhs_of_equation(sub_equations)

#create list of inital conditions
z0 = []
for mass in list_of_mass:
    z0.append(-mass.position[1])
    z0.append(-mass.position[0])
z0 += [0]*2*len(list_of_mass)
print(z0)
#z0 = [0.5, 0, 0.9, 0, 1.5, 0, 0, 0, 0, 0, 0, 0]  # [x1, y1, x2, y2, x1_dot, y1_dot, x2_dot, y2_dot]

t_span = (0, 10)

start = time.time()
res = system.simulate(param_values, z0, t_span, 100001) 
end = time.time()
print("Duration of simulation: ", end - start, "s.")

print("Saving data ...")
savepath = os.path.dirname(os.path.realpath(__file__))+"\data\\test.nc"
save_system(savepath, res, system)
print("Data saved.")

t = res.t
# x1_val = res.y[1]
# x2_val = res.y[3]
# x3_val = res.y[5]
x1_val = res.y[0]
x2_val = res.y[2]
x3_val = res.y[4]

# Plot results
plt.plot(t, x1_val, label='Position of Mass 1 (m)')
plt.plot(t, x2_val, label='Position of Mass 2 (m)')
plt.plot(t, x3_val, label='Position of Mass 3 (m)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Double Mass Oscillator')
plt.legend()
plt.grid(True)
plt.show(block=False)

# plot equations
x1, x2, x1d, x2d, x1dd, x2dd = sp.symbols("x1, x2, x1d, x2d, x1dd, x2dd")
x1t = system.coordinates['m1']['x']
x1dt = system.velocities['m1']['x']
x1ddt = system.accelerations['m1']['x']
x2t = system.coordinates['m1']['x']
x2dt = system.velocities['m1']['x']
x2ddt = system.accelerations['m1']['x']

rplmts = [(x1ddt, x1dd), (x2ddt, x2dd), (x1dt, x1d), (x2dt, x2d), (x1t, x1), (x2t, x2)]
Eq1a = sp.Eq(x1dd, rhs_eq[0].subs(rplmts))
Eq2a = sp.Eq(x2dd, rhs_eq[2].subs(rplmts))
# provide LaTey notation for the symbols
sn_dict = {x1dd: r"\ddot{x1}", x1d: r"\dot{\x1}",
           x2dd: r"\ddot{x2}", x2d: r"\dot{\x2}"}

preview(Eq1a, symbol_names=sn_dict)
preview(Eq2a, symbol_names=sn_dict)

#path and name of the saved file
savepath_equation = os.path.dirname(os.path.realpath(__file__))+"\data\\tex_equation"
tex_save(savepath_equation, [Eq1a, Eq2a])

# animation
animation.animation(res, list_of_object_lists,skip_sim_steps=150)
# animation.animation(res, list_of_object_lists)

######################################################
#init class newton
# newton = n.mechanics(list_of_forces_all, sym_mass_list, yt, angle_list)
# # get sum of forces per mass
# F_sum = newton.sum_of_force()
#
# # get equation of motion
# Eq = newton.equation_of_motion()
# print(Eq)
#
# # take equation of motion and substitute parameters
# #create list of tuple of each mass to substitue the parameters
# subs_mass = [mass.substitution_list() for mass in list_of_mass]
# #create list of tuple of each spring to substitue the parameters
# subs_spring =[]
# for spring in list_of_springs:
#     subs_spring += spring.substitution_list()
#     print(subs_spring)
# rplmts = subs_mass+subs_spring+[(g, 9.81)]
# print(rplmts)
# Eq = [Eq[i].subs(rplmts) for i in range(len(Eq))]
# Eq_ = newton.get_eom(Eq)
#
# # plot equation
# # create equation in the form yddt = rhs for each mass/generalized coordinate
# Eqa = [sp.Eq(mass.yddt,Eq_[mass.yddt]) for mass in list_of_mass]
# # y1, y2, y1d, y2d, y1dd, y2dd = sp.symbols("y1, y2, y1d, y2d, y1dd, y2dd")
#
# # rplmts = [(mass.yddt, y1dd), (y2ddt, y2dd), (y1dt, y1d), (y2dt, y2d), (y1t, y1), (y2t, y2)]
# # Eq1a = sp.Eq(y1dd, xdd_expr1.subs(rplmts))
# # Eq2a = sp.Eq(y2dd, xdd_expr2.subs(rplmts))
# # provide LaTey notation for the symbols
# # sn_dict = {xd: r"\dot{x}", xdd: r"\ddot{x}"}
# # rplmts = [(xddt, xdd), (xdt, xd), (xt, x)]
# # Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))
# # preview(Eq1a, symbol_names=sn_dict)
# # provide LaTeX notation for the symbols
# sn_dict = {list_of_mass[0].yddt: r"\ddot{y1}", list_of_mass[0].ydt: r"\dot{\y1}",
#            list_of_mass[1].yddt: r"\ddot{y2}", list_of_mass[1].ydt: r"\dot{\y2}"}
#
# preview(Eqa[0], symbol_names=sn_dict)
# preview(Eqa[1], symbol_names=sn_dict)
#
#
# # simulation
# y1_0 = 1      # initial position of the first object (m)
# v1_0 = 0.0      # initial velocity of the first object (m/s)
# y2_0 = 1     # initial position of the second object (m)
# v2_0 = 0.0      # initial velocity of the second object (m/s)
# y0 = [y1_0, v1_0, y2_0, v2_0]
# t_span = (0, 100)
#
# start = time.time()
# res = newton.simulate(Eq, y0, t_span, 100001)
# end = time.time()
# print("Duration of simulation: ", end - start, "s.")
#
# t_values = res.t
# x1_values = res.y[0]
# x2_values = res.y[2]
#
# # Plot results
# plt.plot(t_values, x1_values, label='Position of Mass 1 (m)')
# plt.plot(t_values, x2_values, label='Position of Mass 2 (m)')
# plt.xlabel('Time (s)')
# plt.ylabel('Position (m)')
# plt.title('Double Mass Oscillator')
# plt.legend()
# plt.grid(True)
# plt.show()


################################################################
# #save (symbolic data must be converted to a string)
# sym_data = array([str(q), str(t), str(T), str(U), str(F)])
# # save time
# save_data = [sol.t]
# # save simulation result
# save_data.extend(sol.y)
# save_data.append(sym_data)
# # save (symbolic data must be converted to a string)
# #path and name of the saved file
# savepath = os.path.dirname(os.path.realpath(__file__))+"\data\\test.nc"
# save(savepath, data=save_data)

# # load
# start = time.time()
# data = load(savepath, (0,))
# end = time.time()
# print("Duration of loading data: ", end - start, "s.")

# # load simulation data
# time = data[0][:]
# #y = data[1]
# position = data[1][:]
# velocity = data[2][:]

# # load simulation variables and transform them into symbolic variables
# q_l = sp.sympify(data[3][0])
# t_l = sp.sympify(data[3][1])
# T_l = sp.sympify(data[3][2])
# U_l = sp.sympify(data[3][3])
# F_l = sp.sympify(data[3][4])
# xt = q_l[0][0]
# xdt = q_l[0][1]
# xddt = q_l[0][2]

# # construct symbolic equation of motion with loaded data
# L1 = lagrange.Lagrange(q_l, t_l, T_l, U_l, F_l)
# L_eq_l = L1.lagrangian()[q_l[0][-1]]
# pprint(L_eq_l)
# # plot equation
# xdd_expr = L_eq_l
# x, xd, xdd = sp.symbols("x, xd, xdd")
# rplmts = [(xddt, xdd), (xdt, xd), (xt, x)]
# Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))
# # provide LaTeX notation for the symbols
# sn_dict = {xd: r"\dot{x}", xdd: r"\ddot{x}"}

# #preview(Eq1a, symbol_names=sn_dict)

# # plot
# plt.plot(time, position)
# plt.plot(time, velocity)
# plt.legend(["position", "velocity"])
# plt.show()