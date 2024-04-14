from sympy import Function, pprint
import sympy as sp
import lagrange
from matplotlib import pyplot as plt
from simsave import save, load
import time
import objects


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



t = sp.Symbol("t")  # create the symbol for the time
xt = Function("x")(t)  # x(t)
xdt = xt.diff(t)
xddt = xt.diff(t, 2)
q = [xt, xdt]

params = sp.symbols("g, d")
g , d = params
gravity = 9.81

m1 = objects.Mass(2.0,[0,0])
s1 = objects.Spring([0,0], 10.0, 15)
T_m1, U_m1 = m1.enery(xt, xdt,g)
U_s1 = s1.energy(xt)


eq_type = "Values" # Symbols oder Values 
match eq_type:
    case "Symbols":
        pass
    case "Values":
        T_m1 = T_m1.subs(m1.sym_mass,m1.mass)
        U_m1 = U_m1.subs([(m1.sym_mass,m1.mass), (g,gravity)])
        U_s1 = U_s1.subs(s1.sym_stiffness,s1.stiffness)


T = T_m1
U = U_m1 + U_s1
D = d * xdt
# T = 1/2 * m * xdt**2
# U = 1/2 * k * xt**2 - m * g * xt

# mass = 0.1
# gravity = 9.81
# spring_constant = 5
# damping = 0.1

# T = T.subs(m, mass)
# U = U.subs([(m, mass), (g, gravity), (k, spring_constant)])

# D = D.subs(d, damping)

L1 = lagrange.Lagrange(q, t, T, U, D, 0)

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

# save
save("data/test.hdf5", ["time", "position", "velocity"], [sol.t, sol.y[0], sol.y[1]])

# load
start = time.time()
data = load("data/test.hdf5", (0,))
end = time.time()
print("Duration of loading data: ", end - start, "s.")
time = data[1][:]
position = data[0][:]
velocity = data[2][:]

# plot
plt.plot(time, position)
plt.plot(time, velocity)
plt.legend(["position", "velocity"])
plt.show()