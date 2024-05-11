import geometric_relation as gr
import lagrange
import sympy as sp
from sympy import Function, pprint, sin, cos, atan2, atan
import time
from matplotlib import pyplot as plt
from simsave import tex_save
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


params = sp.symbols("m, g, k, d, l, y0")
m, g, k, d, l, y0 = params

mass = 0.05
gravity = 9.81
spring_constant = 5
spring_init_length = 0.03
damping = 0.1
length = 0.05

t = sp.Symbol("t")  # create the symbol for the time
xt = Function("x")(t)  # x(t)
yt = Function("y")(t)
ydt = yt.diff(t)
yddt = yt.diff(t, 2)
xdt = xt.diff(t)
xddt = xt.diff(t, 2)

y1t = Function("y1")(t)
x1t = Function("x1")(t)  # x(t)
x1dt = x1t.diff(t)
y1dt = y1t.diff(t)
y1ddt = y1t.diff(t, 2)

y2t = Function("y2")(t)
x2t = Function("x2")(t)  # x(t)
x2dt = x2t.diff(t)
y2dt = y2t.diff(t)
y2ddt = y2t.diff(t, 2)

q = [[xt, xdt, xddt], [yt, ydt, yddt]]

T = 1/2 * m * (x2dt**2 + y2dt**2)
U = 1/2 * k * y1t**2 + m * g * y2t
D = 0 #-d * ydt

E1 = gr.Relation([U, T, D], [0, y0], [x2t, y2t], [x1t, y1t])
# pprint(E1.compute_relation())
# pprint(E2.compute_relation())

U1 = E1.compute_energy()[0]
T1 = E1.compute_energy()[1]
D1 = E1.compute_energy()[2]
# pprint(E1.compute_energy())

E2 = gr.Relation([U1, T1, D1], [l * sin(atan2(xt, yt)), l * cos(atan2(xt, yt))], [x1t, y1t], [xt, yt])
U2 = E2.compute_energy()[0]
T2 = E2.compute_energy()[1]
D2 = E2.compute_energy()[2]
#path and name of the saved file
savepath_energy = os.path.dirname(os.path.realpath(__file__))+"\data\\tex_energy"
tex_save(savepath_energy, [U2, T2])
# pprint(E2.compute_energy())

T = T2.subs([(m, mass), (g, gravity), (k, spring_constant), (y0, spring_init_length), (l, length), (d, damping)])
U = U2.subs([(m, mass), (g, gravity), (k, spring_constant), (y0, spring_init_length), (l, length), (d, damping)])
#D = D2.subs([(m, mass), (g, gravity), (k, spring_constant), (l, length), (d, damping)])
L1 = lagrange.Lagrange(q, t, T, U, [D, D])

L_eq = L1.lagrangian()
#path and name of the saved file
savepath_equation = os.path.dirname(os.path.realpath(__file__))+"\data\\tex_equation"
tex_save(savepath_equation, [L_eq[q[0][-1]], L_eq[q[1][-1]]])
#pprint(L_eq)

# plot equation
xdd_expr = L_eq[q[0][-1]]
ydd_expr = L_eq[q[1][-1]]
x, y, xd, yd, xdd, ydd = sp.symbols("x, y, xd, yd, xdd, ydd")
rplmts = [(xddt, xdd), (yddt, ydd), (xdt, xd), (ydt, yd),(xt, x), (yt, y)]
Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))
Eq2a = sp.Eq(ydd, ydd_expr.subs(rplmts))
# provide LaTeX notation for the symbols
sn_dict = {xd: r"\dot{x}", yd: r"\dot{y}",
           xdd: r"\ddot{x}", ydd: r"\ddot{y}"}

preview(Eq1a, symbol_names=sn_dict)
preview(Eq2a, symbol_names=sn_dict)

# simulation
x0 = [0.035, 0, 0.08, 0]
t_span = (0, 20)

start = time.time()
sol = L1.simulate(x0, t_span, 20001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")

# plot
plt.figure(figsize=(20,12))
plt.subplot(1, 2, 1)
plt.plot(sol.t, sol.y[0])
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position x")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(sol.t, sol.y[1])
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position y")
plt.grid()
plt.show()