from sympy import Function, pprint, solve
import sympy as sp
import lagrange

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

params = sp.symbols("m, g, k")
m, g, k = params

# task 2
t = sp.Symbol("t")  # create the symbol for the time
xt = Function("x")(t)  # x(t)

xdt = xt.diff(t)
xddt = xt.diff(t, 2)

T = 1/2 * m * xdt**2
U = 1/2 * k * xt**2 + m * g * xt

L1 = lagrange.Lagrange(xt, t, T, U,0)

L_eq = L1.lagrange_equation()
Eq = L1.equation_of_motion()

res = solve(Eq, xddt)
xdd_expr = res[0]
x, xd, xdd = sp.symbols("x, xd, xdd")
rplmts = [(xddt, xdd), (xdt, xd), (xt, x)]
Eq1a = sp.Eq(xdd, xdd_expr.subs(rplmts))

# provide LaTeX notation for the symbols
sn_dict = {xd: r"\dot{x}", xdd: r"\ddot{x}"}

preview(Eq1a, symbol_names=sn_dict)
