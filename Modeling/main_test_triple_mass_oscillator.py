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


params = sp.symbols("m1, m2, m3, l1, l2, l3, g, d, c1, c2, c3")
m1, m2, m3, l1, l2, l3, g, d, c1, c2, c3 = params

t = sp.Symbol("t")
x1t = Function("x1t")(t)  # x1(t)
x2t = Function("x2t")(t)  # x2(t)
x3t = Function("x3t")(t)  # x3(t)

x1dt = x1t.diff(t)
x2dt = x2t.diff(t)
x3dt = x3t.diff(t)

x1ddt = x1t.diff(t, 2)
x2ddt = x2t.diff(t, 2)
x3ddt = x3t.diff(t, 2)

T = (m1*x1dt**2 + m2*x2dt**2 + m3*x3dt**2)/2
Uc1 = 1/2 * c1 * (x1t - l1)**2
Uc2 = 1/2 * c2 * (x2t - x1t - l2)**2
Uc3 = 1/2 * c3 * (x3t - x2t - x1t - l3)**2
Um1 = -m1 * g * x1t
Um2 = -m2 * g * x2t
Um3 = -m3 * g * x3t
U = Uc1 + Uc2 + Uc3 + Um1 + Um2 + Um3
F = [0, 0, 0]
T = T.subs([(m1, 0.05), (m2, 0.05), (m3, 0.05)])
U = U.subs([(m1, 0.05), (m2, 0.05), (m3, 0.05), (g, 9.81), (l1, 0.003), (l2, 0.004), (l3, 0.005), (c1, 10), (c2, 15), (c3, 20)])
q = [[x1t, x1dt, x1ddt], [x2t, x2dt, x2ddt], [x3t, x3dt, x3ddt]]

L1 = lagrange.Lagrange(q, t, T, U, F)

L_eq = L1.lagrangian()

# simulation
x0 = [0, 0, 0, 0, 0, 0]
t_span = (0, 20)

start = time.time()
sol = L1.simulate(x0, t_span, 100001)
end = time.time()
print("Duration of simulation: ", end - start, "s.")
# save (symbolic data must be converted to a string)

save("data/test.nc", ["time", "position1", "position2", "position3", "position_velocity1",
                      "position_velocity2", "position_velocity3", "Energy and Variables"],
                  [sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3], sol.y[4], sol.y[5],
                       array([str(q), str(t), str(T), str(U), str(F)])])

# load
start = time.time()
data = load("data/test.nc")
end = time.time()
print("Duration of loading data: ", end - start, "s.")

# load simulation data
time = data[0][:]
position1 = data[1][:]
position2 = data[2][:]
position3 = data[3][:]
position_velocity1 = data[4][:]
position_velocity2 = data[5][:]
position_velocity3 = data[6][:]

# load simulation variables and transform them into symbolic variables
q_l = sp.sympify(data[7][0])
t_l = sp.sympify(data[7][1])
T_l = sp.sympify(data[7][2])
U_l = sp.sympify(data[7][3])
D_l = sp.sympify(data[7][4])

x1t = q_l[0][0]
x1dt = q_l[0][1]
x1ddt = q_l[0][2]
x2t = q_l[1][0]
x2dt = q_l[1][1]
x2ddt = q_l[1][2]
x3t = q_l[2][0]
x3dt = q_l[2][1]
x3ddt = q_l[2][2]

# construct symbolic equation of motion with loaded data
L1 = lagrange.Lagrange(q_l, t_l, T_l, U_l, D_l)
L_eq_l = L1.lagrangian()
# pprint(L_eq_l)

# plot equation
xdd_expr = L_eq_l[q_l[0][-1]]
phidd_expr = L_eq_l[q_l[1][-1]]
x1, x2, x3, x1d, x2d, x3d, x1dd, x2dd, x3dd = sp.symbols("x1, x2, x3, x1d, x2d, x3d, x1dd, x2dd, x3dd")

rplmts = [(x1ddt, x1dd), (x2ddt, x2dd), (x3ddt, x3dd), (x1dt, x1d), (x2dt, x2d), (x3dt, x3d),
          (x1t, x1), (x2t, x2), (x3t, x3)]
Eq1a = sp.Eq(x1dd, xdd_expr.subs(rplmts))
Eq2a = sp.Eq(x2dd, phidd_expr.subs(rplmts))
Eq3a = sp.Eq(x3dd, phidd_expr.subs(rplmts))
# provide LaTeX notation for the symbols
# provide LaTeX notation for the symbols
sn_dict = {x1dd: r"\ddot{x1}", x2dd: r"\ddot{x2}", x3dd: r"\ddot{x3}"}

preview(Eq1a, symbol_names=sn_dict)
preview(Eq2a, symbol_names=sn_dict)
preview(Eq3a, symbol_names=sn_dict)

# plot
plt.figure(figsize=(20, 12))
plt.subplot(3, 1, 1)
plt.plot(time, position1)
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position m1")
plt.grid()
plt.subplot(3, 1, 2)
plt.plot(time, position2)
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position m2")
plt.grid()
plt.subplot(3, 1, 3)
plt.plot(time, position3)
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position m3")
plt.grid()
plt.show()