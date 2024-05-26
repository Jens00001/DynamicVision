import newton as newton
from numpy import array
import sympy as sp
from matplotlib import pyplot as plt
from simsave import tex_save, save_system, load_system
import time
import os


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
    plt.show()


# Setup system with new mechanics
system = newton.Mechanics()

# add masses
system.add_mass('m1', mass=sp.symbols('m1'))
system.add_mass('m2', mass=sp.symbols('m2'))

# define symbols
k1, k2, m1, m2, g, l1, l2 = sp.symbols('k1 k2 m1 m2 g l1 l2')

# get coordinates for masses
x1 = system.coordinates['m1']['x']
y1 = system.coordinates['m1']['y']
x2 = system.coordinates['m2']['x']
y2 = system.coordinates['m2']['y']

# forces on m1
F_1 = -k1 * (y1 - l1)
F_2 = k2 * (y2 - y1 - l2)
F_1G = m1 * g

# force in x direction
F_x_m1 = 0
system.add_force('m1', (F_x_m1, 'x'))

# force in y direction
F_y_m1 = F_1 + F_2 + F_1G
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
print(system.constraints)

# get equation of motion (only required for displaying purposes)
equations = system.generate_equations()
system.param_values = {m1: 1, m2: 2, k1: 100, k2: 150, g: 9.81, l1: 0.5, l2: 0.4}

# get substituted equations (only required for displaying purposes)
sub_equations = system.substitute_parameters(equations, system.param_values)
rhs_eq = system.rhs_of_equation(sub_equations)
# print(rhs_eq)

z0 = [0, 1, 0, 2, 0, 0, 0, 0]  # [x1, y1, x2, y2, x1_dot, y1_dot, x2_dot, y2_dot]
t_span = (0, 10)

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

# load simulation data
time = data['time']
y1_val = data['results'][1]
y2_val = data['results'][3]

# Plot results
plt.plot(time, y1_val, label='Position of Mass 1 (m)')
plt.plot(time, y2_val, label='Position of Mass 2 (m)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Double Mass Oscillator')
plt.legend()
plt.grid(True)
plt.show()

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

equ = loaded_system.generate_equations()
sub_eq = loaded_system.substitute_parameters(equ, param_val)
eq_rhs = loaded_system.rhs_of_equation(sub_eq)

# plot equation
ydd_expr1 = eq_rhs[1]
ydd_expr2 = eq_rhs[3]

y1t = data['system']['coordinates']['m1']['y']
y1dt = data['system']['velocities']['m1']['y']
y1ddt = data['system']['accelerations']['m1']['y']
y2t = data['system']['coordinates']['m2']['y']
y2dt = data['system']['velocities']['m2']['y']
y2ddt = data['system']['accelerations']['m2']['y']

y1, y2, y1d, y2d, y1dd, y2dd = sp.symbols("y1, y2, y1d, y2d, y1dd, y2dd")

rplmts = [(y1ddt, y1dd), (y2ddt, y2dd), (y1dt, y1d), (y2dt, y2d), (y1t, y1), (y2t, y2)]
Eq1a = sp.Eq(y1dd, ydd_expr1.subs(rplmts))
Eq2a = sp.Eq(y2dd, ydd_expr2.subs(rplmts))
# provide LaTey notation for the symbols
sn_dict = {y1dd: r"\ddot{y1}", y1d: r"\dot{\y1}",
           y2dd: r"\ddot{y2}", y2d: r"\dot{\y2}"}

preview(Eq1a, symbol_names=sn_dict)
preview(Eq2a, symbol_names=sn_dict)

#path and name of the saved file
savepath_equation = os.path.dirname(os.path.realpath(__file__))+"\data\\tex_equation"
tex_save(savepath_equation, [Eq1a, Eq2a])