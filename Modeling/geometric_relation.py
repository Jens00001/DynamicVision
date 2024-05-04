from sympy import MatrixSymbol, Matrix, Symbol, pprint, Derivative
import numpy


class Relation:
    """
    Class for calculating the geometric relationship between the component and the generalized coordinates

    :param x:
    :type x:

    """

    def __init__(self, E, d, c, q):
        self.E = E
        self.d = d
        self.c = c
        self.q = q

    def __repr__(self):
        return str(list(self.__dict__.items()))

    def check_attributes(self):
        """
        Method for checking the type of input variable

        :raises AssertionError: if the type of the input variable is wrong
        """
        assert isinstance(self.E, list)
        assert isinstance(self.d, (int, float))
        assert isinstance(self.c, list)
        assert isinstance(self.q, list)

    def compute_relation(self):
        """
        Method for calculating the geometric relation

        :return: x
        :rtype: x
        """
        # construct 2-dimensional translation matrix (T_0,2: translation in x-direction, T_1,2: translation in y-direction)
        T = MatrixSymbol('T', 3, 3)
        T = Matrix(T)
        T = T.subs([(T[0, 0], 1), (T[0, 1], 0), (T[1, 0], 0), (T[1, 1], 1), (T[2, 0], 0), (T[2, 1], 0), (T[2, 2], 1)])

        # substitute x and y translation
        T = T.subs([(T[0, 2], self.d[0]), (T[1, 2], self.d[1])])

        comp_coord = MatrixSymbol('comp_coord', len(self.c) + 1, 1)
        comp_coord = Matrix(comp_coord)
        comp_coord = comp_coord.subs(
            [(comp_coord[0, 0], self.c[0]), (comp_coord[1, 0], self.c[1]), (comp_coord[2, 0], 1)])

        gen_coord = MatrixSymbol('gen_coord', len(self.q) + 1, 1)
        gen_coord = Matrix(gen_coord)
        gen_coord = gen_coord.subs([(gen_coord[0, 0], self.q[0]), (gen_coord[1, 0], self.q[1]), (gen_coord[2, 0], 1)])

        comp_coord = T.multiply(gen_coord)
        return [comp_coord[0], comp_coord[1]]

    def compute_energy(self):
        """
        Method for computing the potential and kinetic energy (depending on the generalized coordinates)

        :return: x
        :rtype: x
        """
        coords = self.compute_relation()
        t = Symbol("t")  # create the symbol for the time
        dgc = [gc.diff(t) for gc in self.c]
        dcoord = [co.diff(t) for co in coords]
        energy_pot = [self.E[0].subs([(self.c[i], coords[i])]) for i in range(len(self.c))]
        energy_kin = [self.E[1].subs([(dgc[i], dcoord[i])]) for i in range(len(self.c))]
        ex_force = [self.E[2].subs([(dgc[i], dcoord[i])]) for i in range(len(self.c))]
        return [energy_pot[1], energy_kin[1], ex_force[1]]

