import matplotlib.pyplot as plt
from sympy import Eq, latex, Function, symbols, Derivative


def eq_to_latex(system):
    """
    Method for transform equations of motion to LaTeX notation.
    With the given input the method extracts the equations of motion of the system. To do that it replaces
    the used variables(i.e. x1(t),x2(t),y1(t),y2(t)) with variables that don't depend on the time (i.e. x1,x2,y1,y2)
    for a better readability.
    It also generates the derivatives to display the equation accordingly.
    Using the latex() function of sympy the LaTeX notation of the equations of motion is generated.

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
    expr_eq = system.rhs_of_equation(equ)

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


def show_equations_of_motion(latex_str, font_size=16):
    """
    Method to display expressions in LaTeX.
    The method generates a simple figure based on matplotlib in 16x9 format. It uses the text() function of matplotlib
    to show expressions.

    :param latex_str: String that should be displayed (should be already in LaTeX notation)
    :type latex_str: string
    :param font_size: size of the displayed text
    :type font_size: int
    """

    # base 16:9 aspect ratio
    base_width = 16
    base_height = 9
    # split the string into lines and find the length of the longest line
    lines = latex_str.split('\n')
    longest_line_length = max(len(l) for l in lines)
    # adjust width proportionally to the length of the string
    correction_term = longest_line_length / 140

    # compute the width based on the longest line length
    width = base_width * correction_term
    # compute the height based on the width to maintain a 16:9 aspect ratio
    height = (width / base_width) * base_height

    # plot for LaTeX display
    plt.figure(figsize=(width, height))  # adjusted 16x9 format based on string length

    # show the LaTex expression
    plt.text(0.5, 0.5, latex_str, fontsize=font_size, horizontalalignment="center", verticalalignment="center",
             multialignment="center", wrap=True)
    plt.axis("off")
    plt.show(block=False)


class LoadedSystem:
    """
    A class to represent a loaded system with associated time, output data, and system parameters.

    :param t: time values of the simulated and loaded system
    :type t: float
    :param y: results of the simulated and loaded system
    :type y: Numpy.array
    :param loaded_system: Loaded system regarding the Newton class
    :type loaded_system: Newton class
    """
    def __init__(self, t, y, loaded_system):
        self.t = t
        self.y = y
        self.loaded_system = loaded_system