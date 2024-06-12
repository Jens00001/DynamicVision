import newton as newton
from numpy import array
import sympy as sp
from matplotlib import pyplot as plt
from simsave import tex_save, save_system, load_system
import time
import os
from additions import eq_to_latex, show_equations_of_motion

# Setup system with new mechanics
system = newton.Mechanics()

# add masses
system.add_mass('m1', mass=sp.symbols('m1'))
system.add_mass('m2', mass=sp.symbols('m2'))

# define symbols
d, k1, k2, m1, m2, g, l1, l2 = sp.symbols('d k1 k2 m1 m2 g l1 l2')

# get coordinates for masses
x1 = system.coordinates['m1']['x']
y1 = system.coordinates['m1']['y']
x2 = system.coordinates['m2']['x']
y2 = system.coordinates['m2']['y']
dy1 = system.velocities['m1']['y']

# forces on m1
F_1d = -d * dy1
F_1 = -k1 * (y1 - l1)
F_2 = k2 * (y2 - y1 - l2)
F_1G = m1 * g

# force in x direction
F_x_m1 = 0
system.add_force('m1', (F_x_m1, 'x'))

# force in y direction
F_y_m1 = F_1 + F_2 + F_1G + F_1d
system.add_force('m1', (F_y_m1, 'y'))

# forces on m2
F_3 = -k2 * (y2 - y1 - l2)
F_2G = m2 * g

# force in x direction
F_x_m2 = 0
system.add_force('m2', (F_x_m2, 'x'))

# force in y direction
F_y_m2 = F_3 + F_2G
system.add_force('m2', (F_y_m2, 'y'))

# geometric relationships
# distance between global coordinate origin and first mass
system.generate_constraint("link", 'm1', 'm1', l1)
# distance between first mass and second mass
system.generate_constraint("link", 'm1', 'm2', l2)

# get equation of motion (only required for displaying purposes)
equations = system.generate_equations()
system.param_values = {m1: 1, m2: 2, k1: 100, k2: 150, d: 0.7, g: 9.81, l1: 0.5, l2: 0.4}

# get substituted equations (only required for displaying purposes)
sub_equations = system.substitute_parameters(equations, system.param_values)
rhs_eq = system.rhs_of_equation(sub_equations)
# print(rhs_eq)

z0 = [0, 0.5, 0, 0.4, 0, 0, 0, 0]  # [x1, y1, x2, y2, x1_dot, y1_dot, x2_dot, y2_dot]
t_span = (0, 20)

start = time.time()
res = system.simulate(system.param_values, z0, t_span, 100001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")

print("Saving data ...")
savepath = os.path.dirname(os.path.realpath(__file__))+"\data\\test.nc"
save_system(savepath, res, system)
print("Data saved.")

print("Loading data ...")
start = time.time()
data = load_system(savepath)
end = time.time()
print("Duration of loading data: ", end - start, "s.")

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
    i = i + 1

loaded_system.param_values = param_val
equ = loaded_system.generate_equations()
sub_eq = loaded_system.substitute_parameters(equ, loaded_system.param_values)
eq_rhs = loaded_system.rhs_of_equation(sub_eq)
# generate latex notion of equations of motion
eqm = eq_to_latex(loaded_system)

# plot/show equations of motion
show_equations_of_motion(eqm)

#path and name of the saved file
savepath_equation = os.path.dirname(os.path.realpath(__file__))+"\data\\tex_equation"
tex_save(savepath_equation, loaded_system)

# load simulation data
time = data['time']
res_pos = [d for d in data['results'][0:len(equ)]]

# Plot results
plt.figure(figsize=(16 * 1, 9 * 1))
for data in res_pos:
    plt.plot(time, data)

plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Double Mass Oscillator')
plt.legend()
plt.grid(True)
plt.show(block=True)