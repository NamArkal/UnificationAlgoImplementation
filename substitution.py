"""
Provides two functions for handling variable substitution.
Substitutions are represented by dictionaries.
The keys should be Variable objects and the should be
Variables, Constants, and/or Expression objects.
Given a substitution s, the mapping s[v] = t indicates that
every occurrence of v is to be replaced by t.
"""
from expression import *
import copy

def substitute(s, e):
    """
    Applies a substitution s to e, returning the result.
    e is a Variable, Constant, or Expression object.
    s is a dictionary mapping Variable keys to
    Variable, Constant, or Expression values.
    The mapping s[v] = t indicates that every occurrence of
    v is to be replaced by t.
    
    If e is a variable and a key in s, returns s[e].
    Else if e is an expression with operator o and arguments
        ... a_i, ...,
    returns a new expression with operator o, and arguments
        ... substitute(s, a_i), ...
    Else returns e.
    """
    args = []
    if isinstance(e, Variable) and e in s:
        return s[e]
    if isinstance(e, Expression):
        for a in e.arguments:
            args.append(substitute(s, a))
        return Expression(e.operator, args)
    return e

def compose(s2, s1):
    """
    Composes two substitutions s2 and s1,
    returning a single equivalent substitution s.
    Applying s is equivalent to applying s1 followed by s2.
    """

    for key, value in s1.items():
        s1[key] = substitute(s2, value)

    temp, s = {}, {}
    temp.update(s2)
    temp.update(s1)

    s = {k: v for k, v in temp.items() if k != v}
    return s

if __name__ == "__main__":

    """
    Some examples of applying and composing substitutions.
    Feel free to edit the following code.
    """

    subs = [
        {"x": "y"},
        {"y": "z"},
        {"x": "P(y)", "y": "P(w)"}]
    subs = [{
        parse_expression(v): parse_expression(e)
        for v, e in s.items()}
        for s in subs]
    print(subs[2])

    print(substitute(subs[0], parse_expression("P(x)")))

    print(compose(subs[1],subs[0]))
    print(compose(subs[0],subs[1]))
    print(compose(subs[2],subs[0]))
