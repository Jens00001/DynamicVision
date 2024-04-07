from sympy import Function, pprint
import sympy as sp
import lagrange
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

params = sp.symbols("m, g, k, d")
m, g, k, d = params

t = sp.Symbol("t")  # create the symbol for the time
xt = Function("x")(t)  # x(t)
xdt = xt.diff(t)
xddt = xt.diff(t, 2)
q = [xt, xdt]

T = 1/2 * m * xdt**2
U = 1/2 * k * xt**2 + m * g * xt

x = sp.Symbol("x")  # create the symbol for the time
T = T.subs([(m, 20), (g, 9.81), (k, 10)])
U = U.subs([(m, 20), (g, 9.81), (k, 10)])

L1 = lagrange.Lagrange(q, t, T, U, 0, 0)

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

# simulation and plot result
x0 = [0, 0]
t_span = (0, 100)
sol = L1.simulate(x0, t_span)

plt.plot(sol.t, sol.y[0])
plt.show()

