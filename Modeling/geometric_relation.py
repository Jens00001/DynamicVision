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
        # construct 2-dimensional translation matrix
        # (T[0,2]: translation in x-direction, T[1,2]: translation in y-direction)
        T = MatrixSymbol('T', 3, 3)
        T = Matrix(T)
        T = T.subs([(T[0, 0], 1), (T[0, 1], 0), (T[1, 0], 0), (T[1, 1], 1), (T[2, 0], 0), (T[2, 1], 0), (T[2, 2], 1)])

        # substitute x and y translation
        T = T.subs([(T[0, 2], self.d[0]), (T[1, 2], self.d[1])])
        # pprint(T)

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
        # get geometric relation
        coords = self.compute_relation()
        # create the symbol for the time
        t = Symbol("t")
        # compute derivative of component coordinates
        dgc = [gc.diff(t) for gc in self.c]
        # compute derivative of component coordinates depending on generalized coordinates
        dcoord = [co.diff(t) for co in coords]

        # potential energy depends always on q only
        energy_pot = self.E[0].subs([(self.c[0], coords[0]), (self.c[1], coords[1])])

        # kinetic energy can depend on dq and q
        energy_kin = self.E[1].subs([(dgc[0], dcoord[0]), (dgc[1], dcoord[1]),
                                     (self.c[0], coords[0]), (self.c[1], coords[1])])

        # generalized force (external force can be an integer or can depend on q and/or dq)
        if isinstance(self.E[2], int) or isinstance(self.E[2], float):
            ex_force = self.E[2]
        else:
            ex_force = self.E[2].subs([(self.c[0], coords[0]), (self.c[1], coords[1]),
                                   (dgc[0], dcoord[0]), (dgc[1], dcoord[1])])

        return [energy_pot, energy_kin, ex_force]

