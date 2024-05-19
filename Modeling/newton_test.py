import newton as newton
from numpy import array
import sympy as sp
from matplotlib import pyplot as plt
from simsave import save, load, tex_save
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
F_1 = -k1 * (x1 - l1)
F_2 = k2 * (x2 - x1 - l2)
F_1G = m1 * g

# force in x direction
F_x_m1 = F_1 + F_2 + F_1G
system.add_force('m1', (F_x_m1, 'x'))

# force in y direction
F_y_m1 = 0
system.add_force('m1', (F_y_m1, 'y'))

# forces on m2
F_3 = -k2 * (x2 - x1 - l2)
F_2G = m2 * g

# force in x direction
F_x_m2 = F_3 + F_2G
system.add_force('m2', (F_x_m2, 'x'))

# force in y direction
F_y_m2 = 0
system.add_force('m2', (F_y_m2, 'y'))

# get equation of motion (only required for displaying purposes)
equations = system.generate_equations()
param_values = {m1: 1, m2: 2, k1: 100, k2: 150, g: 9.81, l1: 0.5, l2: 0.4}

# get substituted equations (only required for displaying purposes)
sub_equations = system.substitute_parameters(equations, param_values)
rhs_eq = system.rhs_of_equation(sub_equations)
# print(rhs_eq)

z0 = [1, 0, 2, 0, 0, 0, 0, 0]  # [x1, y1, x2, y2, x1_dot, y1_dot, x2_dot, y2_dot]
t_span = (0, 10)

start = time.time()
res = system.simulate(param_values, z0, t_span, 100001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")

print("Saving data ...")
# save (symbolic data must be converted to a string)
names = ["m1", "m2"]
forces = [system.forces.get(name, []) for name in names]
sym_data = array([str(param_values), str(system.coordinates), str(system.velocities), str(system.accelerations), str(forces)])
# save time
save_data = [res.t]
# save simulation result
save_data.extend(res.y)
save_data.append(sym_data)
# save (symbolic data must be converted to a string)
#path and name of the saved file
savepath = os.path.dirname(os.path.realpath(__file__))+"\data\\test.nc"
save(savepath, data=save_data)
print("Data saved.")

print("Loading data ...")
start = time.time()
data = load(savepath, (0,))
end = time.time()
print("Duration of loading data: ", end - start, "s.")

# load simulation data
time = data[0][:]
x1_val = data[1][:]
x2_val = data[3][:]

# construct equations of motion with saved data
param_val = data[9][0]
force_m1_x = sp.sympify(data[9][4])[0][0][0]
force_m1_y = sp.sympify(data[9][4])[0][1][0]
force_m2_x = sp.sympify(data[9][4])[1][0][0]
force_m2_y = sp.sympify(data[9][4])[1][1][0]

# set up system with loaded data
loaded_system = newton.Mechanics()
loaded_system.add_mass('m1', mass=sp.symbols('m1'))
loaded_system.add_mass('m2', mass=sp.symbols('m2'))
k1, k2, m1, m2 = sp.symbols('k1 k2 m1 m2')
x1 = loaded_system.coordinates['m1']['x']
y1 = loaded_system.coordinates['m1']['y']
x2 = loaded_system.coordinates['m2']['x']
y2 = loaded_system.coordinates['m2']['y']
loaded_system.add_force('m1', (force_m1_x, 'x'))
loaded_system.add_force('m1', (force_m1_y, 'y'))
loaded_system.add_force('m2', (force_m2_x, 'x'))
loaded_system.add_force('m2', (force_m2_y, 'y'))
equ = loaded_system.generate_equations()

sub_eq = loaded_system.substitute_parameters(equ, sp.sympify(param_val))
eq_rhs = loaded_system.rhs_of_equation(sub_eq)

# Plot results
plt.plot(time, x1_val, label='Position of Mass 1 (m)')
plt.plot(time, x2_val, label='Position of Mass 2 (m)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Double Mass Oscillator')
plt.legend()
plt.grid(True)
plt.show()

# plot equation
xdd_expr1 = eq_rhs[0]
xdd_expr2 = eq_rhs[2]

x1t = sp.sympify(data[9][1])['m1']['x']
x1dt = sp.sympify(data[9][2])['m1']['x']
x1ddt = sp.sympify(data[9][3])['m1']['x']
x2t = sp.sympify(data[9][1])['m2']['x']
x2dt = sp.sympify(data[9][2])['m2']['x']
x2ddt = sp.sympify(data[9][3])['m2']['x']

x1, x2, x1d, x2d, x1dd, x2dd = sp.symbols("x1, x2, x1d, x2d, x1dd, x2dd")

rplmts = [(x1ddt, x1dd), (x2ddt, x2dd), (x1dt, x1d), (x2dt, x2d), (x1t, x1), (x2t, x2)]
Eq1a = sp.Eq(x1dd, xdd_expr1.subs(rplmts))
Eq2a = sp.Eq(x2dd, xdd_expr2.subs(rplmts))
# provide LaTey notation for the symbols
sn_dict = {x1dd: r"\ddot{x1}", x1d: r"\dot{\x1}",
           x2dd: r"\ddot{x2}", x2d: r"\dot{\x2}"}

preview(Eq1a, symbol_names=sn_dict)
preview(Eq2a, symbol_names=sn_dict)

#path and name of the saved file
savepath_equation = os.path.dirname(os.path.realpath(__file__))+"\data\\tex_equation"
tex_save(savepath_equation, [Eq1a, Eq2a])