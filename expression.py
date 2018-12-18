"""
Provides three classes to represent variables, constants, and expressions.
Variable and Constant names start with lower and upper case letters, respectively.
Expressions are trees with Variables and/or Constants as leaves.
Each internal node includes an operator and an argument (i.e., child) list.
"""


class Variable:
    def __init__(self, variable_name):
        """
        Initialize a variable with the given name.
        The name should start with a lower-case letter.
        """
        if variable_name[0].isupper(): raise (Exception("Variable name starting with upper-case!"))
        self.variable_name = variable_name

    def __eq__(self, other):
        """
        Checks whether self and other represent the same variable.
        Two variables are the same if they have the same name.
        """
        return isinstance(other, Variable) and self.variable_name == other.variable_name

    def __ne__(self, other):
        """
        Checks whether self and other represent different variables.
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        Returns a string representation of the variable.
        """
        return self.variable_name

    def __repr__(self):
        """
        Returns a string representation of the variable.
        """
        return str(self)

    def __hash__(self):
        """
        Produces a hash of the variable so it can be stored in a dictionary.
        """
        return str(self).__hash__()

    def occurs_in(self, other):
        """
        Recursively performs the "occurs check" during unification.
        If self represents the same variable as other, returns True.
        Else if other is an instance of Expression,
        and self occurs in one or more of other's arguments, returns True.
        Otherwise, returns False.
        """
        if isinstance(other, Variable) and self.__eq__(other):
            return True
        if isinstance(other, Expression) and self.__str__() in other.__str__():
            return True
        return False


class Constant:
    def __init__(self, constant_name):
        """
        Initialize a constant with the given name.
        The name should start with an upper-case letter.
        """
        if constant_name[0].islower(): raise (Exception("Constant name starting with lower-case!"))
        self.constant_name = constant_name

    def __eq__(self, other):
        """
        Checks whether self and other represent the same constant.
        Two constants are the same if they have the same name.
        """
        return isinstance(other, Constant) and self.constant_name == other.constant_name

    def __ne__(self, other):
        """
        Checks whether self and other represent different constants.
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        Returns a string representation of the constant.
        """
        return self.constant_name

    def __repr__(self):
        """
        Returns a string representation of the constant.
        """
        return str(self)

    def __hash__(self):
        """
        Produces a hash of the constant so it can be stored in a dictionary.
        """
        return str(self).__hash__()


class Expression:
    """
    Represents a compound FOL expression with a top-level function or predicate symbol.
    The "operator" field is the top-level function or predicate symbol.
    The "arguments" field is a list of Constants, Variables, and/or Expression objects.
    """

    def __init__(self, operator, arguments):
        """
        operator: a function or predicate symbol (a string)
        arguments: a list of Constants, Variables, and/or Expression objects.
        """
        self.operator = operator
        self.arguments = arguments

    def __str__(self):
        """
        Returns a string representation of the expression.
        """
        return "%s(%s)" % (
            self.operator,
            ", ".join(map(str, self.arguments)))

    def __repr__(self):
        """
        Returns a string representation of the expression.
        """
        return str(self)

    def __hash__(self):
        """
        Produces a hash of the expression so it can be stored in a dictionary.
        """
        return str(self).__hash__()

    def __eq__(self, other):
        """
        Checks whether self and other represent the same expression.
        Two expressions are the same if they have the same operator
        and each of their respective arguments are the same.
        """
        if not isinstance(other, Expression): return False
        if self.operator != other.operator: return False
        if len(self.arguments) != len(other.arguments): return False
        return all([a1 == a2 for a1, a2 in zip(self.arguments, other.arguments)])

    def __ne__(self, other):
        """
        Checks whether self and other represent different expressions.
        """
        return not self.__eq__(other)


def parse_expression(s):
    """
    Parses a string s and returns a corresponding expression object.
    Assumes arguments are separated by commas and zero or more whitespace.
    """
    l, d, i = [], 0, 0
    op, args = None, []
    for j, c in enumerate(s):
        if c == "(":
            if op is None:
                op = s[:j]
                i = j + 1
            d += 1
        if c == ")":
            if d == 1:
                if j > i: args.append(s[i:j])
                i = j + 1
            d -= 1
        if c == "," and d == 1:
            args.append(s[i:j])
            i = j + 1
        if c == " " and i == j: i += 1

    if op is None:
        if s[0].islower():
            return Variable(s)
        else:
            return Constant(s)

    return Expression(op, list(map(parse_expression, args)))


if __name__ == "__main__":
    """
    Some examples of parsing and using expressions.
    Feel free to edit the following code.
    """

    strs = [
        "x",
        "y",
        "P()",
        "P(A, Q())",
        "P(A, B, B)",
        "Q(y, G(A, B))",
        "Older(Father(y), y)",
        "Knows(y, Father(y))",
        "P(Q(x, y), Q(R(z, y), R(x)), a)",
    ]

    exps = [parse_expression(s) for s in strs]
    print(exps[-1].operator)
    print(exps[-1].arguments)

    print(exps[0] == exps[-1])
    print(exps[-2] == exps[-1])
    print(parse_expression(strs[-1]) == exps[-1])

    for e in exps:
        print(e)
        print(e == e)
        print("y occurs: %s"%Variable("y").occurs_in(e))
