from sympy import Function, pprint
import sympy as sp
import lagrange
from matplotlib import pyplot as plt
from simsave import save, load
import time
from numpy import array


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

params = sp.symbols("m, g, k, d")
m, g, k, d = params

t = sp.Symbol("t")  # create the symbol for the time
xt = Function("x")(t)  # x(t)
xdt = xt.diff(t)
xddt = xt.diff(t, 2)
q = [xt, xdt, xddt]

T = 1/2 * m * xdt**2
U = 1/2 * k * xt**2 - m * g * xt

mass = 0.1
gravity = 9.81
spring_constant = 5
damping = 0.7

T = T.subs(m, mass)
U = U.subs([(m, mass), (g, gravity), (k, spring_constant)])
D = d * xdt
D = D.subs(d, damping)

L1 = lagrange.Lagrange(q, t, T, U, D)

L_eq = L1.lagrangian()[0]
pprint(L_eq)
# plot equation
xdd_expr = L_eq
x, xd, xdd = sp.symbols("x, xd, xdd")
rplmts = [(xddt, xdd), (xdt, xd), (xt, x)]
Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))
# provide LaTeX notation for the symbols
sn_dict = {xd: r"\dot{x}", xdd: r"\ddot{x}"}

preview(Eq1a, symbol_names=sn_dict)

# simulation
x0 = [0, 0]
t_span = (0, 40)

start = time.time()
sol = L1.simulate(x0, t_span, 10001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")
# save (symbolic data must be converted to a string)
save("data/test.nc", ["time", "position", "velocity", "Energy and Variables"], [sol.t, sol.y[0], sol.y[1], array([str(q), str(t), str(T), str(U), str(D)])])


# load
start = time.time()
data = load("data/test.nc", (0,))
end = time.time()
print("Duration of loading data: ", end - start, "s.")

# load simulation data
time = data[0][:]
position = data[1][:]
velocity = data[2][:]

# load simulation variables and transform them into symbolic variables
q_l = sp.sympify(data[3][0])
t_l = sp.sympify(data[3][1])
T_l = sp.sympify(data[3][2])
U_l = sp.sympify(data[3][3])
D_l = sp.sympify(data[3][4])
xt = q_l[0]
xdt = q_l[1]
xddt = q_l[2]

# construct symbolic equation of motion with loaded data
L1 = lagrange.Lagrange(q_l, t_l, T_l, U_l, D_l)
L_eq_l = L1.lagrangian()[0]
pprint(L_eq_l)
# plot equation
xdd_expr = L_eq_l
x, xd, xdd = sp.symbols("x, xd, xdd")
rplmts = [(xddt, xdd), (xdt, xd), (xt, x)]
Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))
# provide LaTeX notation for the symbols
sn_dict = {xd: r"\dot{x}", xdd: r"\ddot{x}"}

preview(Eq1a, symbol_names=sn_dict)

# plot
plt.plot(time, position)
plt.plot(time, velocity)
plt.legend(["position", "velocity"])
plt.show()