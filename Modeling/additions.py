import matplotlib.pyplot as plt
from sympy import Eq, latex, Function, symbols, Derivative


def eq_to_latex(system):
    """
    Method for transform equations of motion to LaTeX notation

    :param system: system for which the equations of motion should be converted
    :type system: newton.Mechanics class
    :return: latex notation of equations
    :rtype: string
    """

    # dictionary for derivative terms
    derivative_dict = {}
    t = symbols("t")
    for i in range(len(system.coordinates)):
        i = i + 1
        x = Function(f'x{i}')(t)
        y = Function(f'y{i}')(t)
        derivative_dict[x] = symbols(f'x_{{{i}}}')
        derivative_dict[Derivative(x, t)] = symbols(f'\\dot{{x}}_{{{i}}}')
        derivative_dict[Derivative(x, t, t)] = symbols(f'\\ddot{{x}}_{{{i}}}')
        derivative_dict[y] = symbols(f'y_{{{i}}}')
        derivative_dict[Derivative(y, t)] = symbols(f'\\dot{{y}}_{{{i}}}')
        derivative_dict[Derivative(y, t, t)] = symbols(f'\\ddot{{y}}_{{{i}}}')

    # get equations from the system
    equ = system.generate_equations()
    sub_eq = system.substitute_parameters(equ, system.param_values)
    expr_eq = system.rhs_of_equation(sub_eq)

    # construct expression: a=F/m
    dd = [system.accelerations[m][c] for m in list(system.parameters.keys()) for c in ['x', 'y']]
    dd_expr = [Eq(dd[i], expr_eq[i]) for i in range(len(dd))]

    # substitute to get rid of the explicit time dependency
    dd_expr_subs = [expr.subs(derivative_dict) for expr in dd_expr]

    # create the LaTeX string
    latex_str = ""
    for expr in dd_expr_subs:
        expr_latex = latex(expr)
        latex_str = latex_str + f"${expr_latex}$\n"

    latex_str = latex_str.replace("operatorname", "mathrm")

    return latex_str


def show_equations_of_motion(latex_str, window_size=(1, 1), font_size=30):
    """
    Method for display of expressions in LaTeX

    :param latex_str: String that should be displayed (should be already in LaTeX notation)
    :type latex_str: newton.Mechanics class
    :param window_size: Multiplier for window size in 16x9 format --> (width, height): width*16, hight*9
    :type window_size: tuple
    :param font_size: size of the displayed text
    :type font_size: int
    """

    # plot for LaTeX display
    plt.figure(figsize=(16 * window_size[0], 9 * window_size[0]))  # 16x9 format

    # show the LaTex expression
    plt.text(0.5, 0.5, latex_str, fontsize=font_size, horizontalalignment="center", verticalalignment="center",
             multialignment="center", wrap=True)
    plt.axis("off")
    plt.show()
