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


# params = sp.symbols("m, g, k, d")
# m, g, k, d = params
#
# t = sp.Symbol("t")  # create the symbol for the time
# xt = Function("x")(t)  # x(t)
# xdt = xt.diff(t)
# xddt = xt.diff(t, 2)
# q = [[xt, xdt, xddt],]
#
# T = 1/2 * m * xdt**2
# U = 1/2 * k * xt**2 - m * g * xt
#
# mass = 0.05
# gravity = 9.81
# spring_constant = 5
# damping = 0.1
#
# T = T.subs(m, mass)
# U = U.subs([(m, mass), (g, gravity), (k, spring_constant)])
# D = d * xdt
# D = D.subs(d, damping)
# L1 = lagrange.Lagrange(q, t, T, U, D)
#
# L_eq = L1.lagrangian()[q[0][-1]]
# pprint(L_eq)
#
# # plot equation
# xdd_expr = L_eq
# x, xd, xdd = sp.symbols("x, xd, xdd")
# rplmts = [(xddt, xdd), (xdt, xd), (xt, x)]
# Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))
# # provide LaTeX notation for the symbols
# sn_dict = {xd: r"\dot{x}", xdd: r"\ddot{x}"}
#
# preview(Eq1a, symbol_names=sn_dict)

# # simulation
# x0 = [0, 0]
# t_span = (0, 40)


params = sp.symbols("m1, m2, l, g, d")
m1, m2, l, g, d = params

t = sp.Symbol("t")  # create the symbol for the time
xt = Function("x")(t)  # x(t)
phit = Function("phi")(t)  # phi(t)
xdt = xt.diff(t)
phidt = phit.diff(t)
xddt = xt.diff(t, 2)
phiddt = phit.diff(t, 2)
x2t = xt + l*sp.sin(phit)
y2t = -l*sp.cos(phit)

x2dt = x2t.diff(t)
y2dt = y2t.diff(t)
T = (m1*xdt**2 + m2*(x2dt**2 + y2dt**2))/2
U = y2t*g*m2
F = [0,0]
T = T.subs([(m1, 0.8), (m2, 0.3), (l, 0.5)])
U = U.subs([(m2, 0.3), (l, 0.5), (g, 9.81)])
q = [[xt, xdt, xddt], [phit, phidt, phiddt]]

L1 = lagrange.Lagrange(q, t, T, U, F)

L_eq = L1.lagrangian()

# simulation
x0 = [0,  sp.pi*0.5, 0, 0]
t_span = (0, 10)

start = time.time()
sol = L1.simulate(x0, t_span, 10001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")
# save (symbolic data must be converted to a string)
save("data/test.nc", ["time", "position", "angle", "position_velocity", "angular_velocity", "Energy and Variables"], [sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3], array([str(q), str(t), str(T), str(U), str(F)])])

# load
start = time.time()
data = load("data/test.nc")
end = time.time()
print("Duration of loading data: ", end - start, "s.")

# load simulation data
time = data[0][:]
position = data[1][:]
angle = data[2][:]
position_velocity = data[3][:]
angular_velocity = data[4][:]

# load simulation variables and transform them into symbolic variables
q_l = sp.sympify(data[5][0])
t_l = sp.sympify(data[5][1])
T_l = sp.sympify(data[5][2])
U_l = sp.sympify(data[5][3])
D_l = sp.sympify(data[5][4])

xt = q_l[0][0]
xdt = q_l[0][1]
xddt = q_l[0][2]
phit = q_l[1][0]
phidt = q_l[1][1]
phiddt = q_l[1][2]

# construct symbolic equation of motion with loaded data
L1 = lagrange.Lagrange(q_l, t_l, T_l, U_l, D_l)
L_eq_l = L1.lagrangian()
# pprint(L_eq_l)

# plot equation
xdd_expr = L_eq_l[q_l[0][-1]]
phidd_expr = L_eq_l[q_l[1][-1]]
x, phi, xd, phid, xdd, phidd = sp.symbols("x, phi, xd, phid, xdd, phidd")

rplmts = [(xddt, xdd), (phiddt, phidd), (xdt, xd), (phidt, phid),
          (xt, x), (phit, phi)]
Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))
Eq2a = sp.Eq(phidd, phidd_expr.subs(rplmts))
# provide LaTeX notation for the symbols
# provide LaTeX notation for the symbols
sn_dict = {phi: r"\varphi", phid: r"\dot{\varphi}",
           xdd: r"\ddot{x}", phidd: r"\ddot{\varphi}"}

preview(Eq1a, symbol_names=sn_dict)
preview(Eq2a, symbol_names=sn_dict)

# plot
plt.figure(figsize=(20,12))
plt.subplot(2, 2, 1)
plt.plot(time, position)
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position x")
plt.grid()
plt.subplot(2, 2, 2)
plt.plot(time, position_velocity)
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity")
plt.grid()
plt.subplot(2, 2, 3)
plt.plot(time, angle)
plt.xlabel("Time (s)")
plt.ylabel("angle (rad°)")
plt.title("Angle phi")
plt.grid()
plt.subplot(2, 2, 4)
plt.plot(time, angular_velocity)
plt.xlabel("Time (s)")
plt.ylabel("angular speed (rad°/s)")
plt.title("Angular Speed")
plt.grid()
plt.show()