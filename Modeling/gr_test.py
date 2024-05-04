import geometric_relation as gr
import lagrange
import sympy as sp
from sympy import Function, pprint
import time
from matplotlib import pyplot as plt

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


params = sp.symbols("m, g, k, d, l")
m, g, k, d, l = params

t = sp.Symbol("t")  # create the symbol for the time
xt = Function("x")(t)  # x(t)
yt = Function("y")(t)
ydt = yt.diff(t)
yddt = yt.diff(t, 2)


y1t = Function("y1")(t)
x1t = Function("x1")(t)  # x(t)
y1dt = y1t.diff(t)
y1ddt = y1t.diff(t, 2)

q = [[yt, ydt, yddt],]

T = 1/2 * m * y1dt**2
U = 1/2 * k * y1t**2 + m * g * y1t
D = -d * ydt

E = gr.Relation([U, T, D], [0, l], [x1t, y1t], [0, yt])
# pprint(E.compute_relation())
pprint(E.compute_energy())

U = E.compute_energy()[0]
T = E.compute_energy()[1]
D = E.compute_energy()[2]

mass = 0.05
gravity = 9.81
spring_constant = 5
damping = 0.1
length = 0.03

T = T.subs(m, mass)
U = U.subs([(m, mass), (g, gravity), (k, spring_constant), (l, length)])
D = D.subs(d, damping)
L1 = lagrange.Lagrange(q, t, T, U, D)

L_eq = L1.lagrangian()[q[0][-1]]
pprint(L_eq)

# plot equation
ydd_expr = L_eq
y, yd, ydd = sp.symbols("y, yd, ydd")
rplmts = [(yddt, ydd), (ydt, yd), (yt, y)]
Eq1a = sp.Eq(ydd, ydd_expr.subs(rplmts))
# provide LaTeX notation for the symbols
sn_dict = {yd: r"\dot{y}", ydd: r"\ddot{y}"}

preview(Eq1a, symbol_names=sn_dict)

# simulation
x0 = [0, 0]
t_span = (0, 10)

start = time.time()
sol = L1.simulate(x0, t_span, 10001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")

# plot
plt.figure(figsize=(20,12))
plt.plot(sol.t, sol.y[0])
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position y")
plt.grid()
plt.show()