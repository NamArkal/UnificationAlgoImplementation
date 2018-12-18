"""
Provides two functions for performing unification.
"""
from expression import *
from substitution import *

def mismatch(e1, e2):
    """
    Finds the first sub-expressions (if any) where e1 and e2 do not match.
    If there are no mismatches, returns (None, None). 
    Else, returns (m1, m2), where m1 and m2 are the mismatched sub-expressions.
    e1 and e2 should be Variables, Constants, or Expression objects.
    m1 and m2 should either be both None, or else both
    Variables, Constants, or Expression objects.
    If either e1 or e2 is not an Expression object, and e1 does not equal e2,
    then m1 is e1 and m2 is e2.
    If e1 and e2 are both expressions with different operators,
    or different number of arguments, then m1 is e1 and m2 is e2.
    Else, if ... a1_i ... are the arguments of e1 and ... a2_i ... are the arguments of e2,
    then m1 and m2 should be the first arguments where a1_i does not match a2_i.
    """
    if isinstance(e1, Expression) and isinstance(e2, Expression):
        if e1.__eq__(e2):
            return (None, None)
        else:
            for i, j in zip(e1.arguments, e2.arguments):
                (m1, m2) = mismatch(i, j)
                if m1 != m2:
                    return (m1, m2)

    elif e1.__ne__(e2):
        return (e1, e2)

    elif not isinstance(e1, Expression) or not isinstance(e2, Expression):
        if e1.__ne__(e2):
            return (e1, e2)
        else:
            return (None, None)

def unify(e1, e2):
    """
    Runs the unification algorithm on e1 and e2.
    e1 and e2 should be Variables, Constants, and/or Expression objects.
    You can assume e1 and e2 are already standardized apart.
    If e1 and e2 do not unify, returns False
    Else, returns a substitution s that unifies e1 with e2.
    s is represented as a dictionary.
    The mapping s[v] = t indicates a substitution in which
    every occurrence of v is to be replaced by t.
    """
    u = {}

    if mismatch(e1, e2) == (None, None):
        return u

    if isinstance(e1, Constant) and isinstance(e2, Constant):
        return False

    if isinstance(e1, Variable):
        (m1, m2) = mismatch(e1, e2)
        u[m1] = m2
        return u

    if isinstance(e2, Variable):
        (m1, m2) = mismatch(e2, e1)
        u[m1] = m2
        return u

    if isinstance(e1, Expression) and isinstance(e2, Expression):
        if e1.operator == e2.operator:
            for i in e1.arguments:
                for j in e2.arguments:
                    if isinstance(i, Variable) and isinstance(j, Variable):
                        if i == j:
                            return False

            for args1, args2 in zip(e1.arguments, e2.arguments):
                if isinstance(args1, Expression) and isinstance(args2, Expression):
                    u.update(unify(args1, args2))
                    res = substitute(u, e1)
                    if isinstance(res, Expression):
                        e1.arguments[:] = res.arguments
                    res2 = substitute(u, e2)
                    if isinstance(res2, Expression):
                        e2.arguments[:] = res2.arguments
                else:
                    (m3, m4) = mismatch(args1, args2)
                    if isinstance(m3, Variable):
                        u[m3] = m4
                        for a, b in enumerate(e1.arguments):
                            if Variable.occurs_in(m3, b):
                                res3 = substitute(u, b)
                                e1.arguments[a] = res3
                    else:
                        u[m4] = m3
                        for a, b in enumerate(e2.arguments):
                            if Variable.occurs_in(m4, b):
                                res4 = substitute(u, b)
                                e2.arguments[a] = res4
            return u
        else:
            return False

if __name__ == "__main__":

    """
    Some examples from the AIMA unification exercises.
    Feel free to edit the following code.
    """
    ep = [
        ("P(A,B,B)", "P(x,y,z)"),
        ("Q(y,G(A,B))", "Q(G(x,x),z)"),
        ("O(F(y),y)", "O(F(x),J)"),
        ("K(F(y),y)", "K(x,x)"),
    ]

    for e1,e2 in ep:
        print(parse_expression(e1), parse_expression(e2))
        print(mismatch(parse_expression(e1), parse_expression(e2)))
        print(unify(parse_expression(e1), parse_expression(e2)))
