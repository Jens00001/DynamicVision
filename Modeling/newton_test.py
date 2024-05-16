import newton as n
from sympy import Function, pprint
import sympy as sp
import lagrange
from matplotlib import pyplot as plt
from simsave import save, load, tex_save
import time
from numpy import array
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

params = sp.symbols("m1, m2, g, k1, k2, l1, l2")
m1, m2, g, k1, k2, l1, l2 = params

# Define constants
k_1 = 1.0  # spring constant for the first spring (N/m)
k_2 = 1.0  # spring constant for the second spring (N/m)
m_1 = 1  # mass of the first object (kg)
m_2 = 1  # mass of the second object (kg)
gravity = 0 #9.81

t = sp.Symbol("t")  # create the symbol for the time
y1t = Function("y1")(t)  # x(t)
y2t = Function("y2")(t)  # x(t)
y1dt = y1t.diff(t)
y2dt = y2t.diff(t)
y1ddt = y1t.diff(t, 2)
y2ddt = y2t.diff(t, 2)

F1_1 = m1*g
F1_2 = k2*(y2t-y1t)
F1_3 = -k1*y1t
F2_1 = m2*g
F2_2 = -k2*(y2t-y1t)

# init class
newton = n.mechanics([[F1_1, F1_2, F1_3], [F2_1, F2_2]], [m1, m2], [y1t, y2t], [[0], [0]])

# get sum of forces per mass
F_sum = newton.sum_of_force()

# get equation of motion
Eq = newton.equation_of_motion()
# print(Eq)

# take equation of motion and substitute parameters
Eq = [Eq[i].subs([(m1, m_1), (m2, m_2), (k1, k_1), (k2, k_2), (g, gravity)]) for i in range(len(Eq))]
Eq_ = newton.get_eom(Eq)
# plot equation
xdd_expr1 = Eq_[y1ddt]
xdd_expr2 = Eq_[y2ddt]
y1, y2, y1d, y2d, y1dd, y2dd = sp.symbols("y1, y2, y1d, y2d, y1dd, y2dd")

rplmts = [(y1ddt, y1dd), (y2ddt, y2dd), (y1dt, y1d), (y2dt, y2d), (y1t, y1), (y2t, y2)]
Eq1a = sp.Eq(y1dd, xdd_expr1.subs(rplmts))
Eq2a = sp.Eq(y2dd, xdd_expr2.subs(rplmts))
# provide LaTey notation for the symbols
sn_dict = {y1dd: r"\ddot{y1}", y1d: r"\dot{\y1}",
           y2dd: r"\ddot{y2}", y2d: r"\dot{\y2}"}

preview(Eq1a, symbol_names=sn_dict)
preview(Eq2a, symbol_names=sn_dict)

# simulation
y1_0 = 1      # initial position of the first object (m)
v1_0 = 0.0      # initial velocity of the first object (m/s)
y2_0 = 1     # initial position of the second object (m)
v2_0 = 0.0      # initial velocity of the second object (m/s)
y0 = [y1_0, v1_0, y2_0, v2_0]
t_span = (0, 100)

start = time.time()
res = newton.simulate(Eq, y0, t_span, 100001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")

t_values = res.t
x1_values = res.y[0]
x2_values = res.y[2]

# Plot results
plt.plot(t_values, x1_values, label='Position of Mass 1 (m)')
plt.plot(t_values, x2_values, label='Position of Mass 2 (m)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Double Mass Oscillator')
plt.legend()
plt.grid(True)
plt.show()