import unittest as ut
from expression import *
from substitution import *
from unification import *

class OccursInTestCase(ut.TestCase):

    def do_test(self, v, e, tf):
        v = parse_expression(v)
        e = parse_expression(e)
        if tf: self.assertTrue(v.occurs_in(e))
        else: self.assertFalse(v.occurs_in(e))

    def test_0(self): self.do_test("y", "y", True)
    def test_1(self): self.do_test("y", "x", False)
    def test_2(self): self.do_test("y", "A", False)
    def test_3(self): self.do_test("y", "P(A, B, B)", False)
    def test_4(self): self.do_test("y", "Q(y, G(A, B))", True)
    def test_5(self): self.do_test("y", "Older(Father(y), y)", True)
    def test_6(self): self.do_test("y", "Knows(y, Father(y))", True)

class SubstituteTestCase(ut.TestCase):

    def do_test(self, s, e, se):
        s = {
            parse_expression(v): parse_expression(t)
            for v, t in s.items()}
        e = parse_expression(e)
        se = parse_expression(se)
        self.assertTrue(substitute(s, e) == se)

    def test_0(self): self.do_test({"x": "A"}, "x", "A")
    def test_1(self): self.do_test({"x": "A", "y": "B"}, "P(x,y)", "P(A,B)")
    def test_2(self): self.do_test({"x": "y", "y": "B"}, "P(x,y)", "P(y,B)")
    def test_3(self): self.do_test({"x": "Q(A)", "y": "x"}, "P(x,y)", "P(Q(A),x)")

class ComposeTestCase(ut.TestCase):

    def do_test(self, s2, s1, s):
        s2 = {
            parse_expression(v): parse_expression(t)
            for v, t in s2.items()}
        s1 = {
            parse_expression(v): parse_expression(t)
            for v, t in s1.items()}
        s = {
            parse_expression(v): parse_expression(t)
            for v, t in s.items()}

        self.assertTrue(compose(s2, s1) == s)

    def test_0(self): self.do_test({"x":"y"}, {"y":"z"}, {"x":"y", "y":"z"})
    def test_1(self): self.do_test({"y":"z"}, {"x":"y"}, {"x":"z", "y":"z"})
    def test_2(self): self.do_test({"y":"z"}, {"x":"P(y)"}, {"x":"P(z)", "y":"z"})

class MismatchTestCase(ut.TestCase):

    def do_test(self, e1, e2, m1, m2):
        e1 = parse_expression(e1)
        e2 = parse_expression(e2)
        if m1 is not None: m1 = parse_expression(m1)
        if m2 is not None: m2 = parse_expression(m2)
        self.assertTrue(mismatch(e1,e2) == (m1,m2))

    def test_0(self): self.do_test("x", "x", None, None)
    def test_1(self): self.do_test("P(A,B,B)", "P(x,y,z)", "A", "x")
    def test_2(self): self.do_test("Q(y,G(A,B))", "Q(G(x,x),z)", "y", "G(x,x)")
    def test_3(self): self.do_test("O(F(y),y)", "O(F(x),J)", "y", "x")
    def test_4(self): self.do_test("K(F(y),y)", "K(x,x)", "F(y)", "x")

class UnifyTestCase(ut.TestCase):

    def do_test(self, e1, e2, s):
        e1 = parse_expression(e1)
        e2 = parse_expression(e2)
        if s is not False: s = {
            parse_expression(v): parse_expression(t)
            for v, t in s.items()}

        self.assertTrue(unify(e1,e2) == s)

    def test_0(self): self.do_test("x", "x", {})
    def test_1(self): self.do_test("A", "A", {})
    def test_2(self): self.do_test("A", "B", False)
    def test_3(self): self.do_test("x", "y", {"x":"y"})
    def test_4(self): self.do_test("x", "A", {"x":"A"})
    def test_5(self): self.do_test("P(A,B,B)", "P(x,y,z)", {"x":"A", "y":"B", "z":"B"})
    def test_6(self): self.do_test("Q(y,G(A,B))", "Q(G(x,x),z)", {"y":"G(x,x)", "z":"G(A,B)"})
    def test_7(self): self.do_test("Q(y,G(A,B))", "Q(G(x,x),y)", False)

if __name__ == "__main__":
    
    test_suite = ut.TestLoader().loadTestsFromTestCase(OccursInTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

    test_suite = ut.TestLoader().loadTestsFromTestCase(SubstituteTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

    test_suite = ut.TestLoader().loadTestsFromTestCase(ComposeTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

    test_suite = ut.TestLoader().loadTestsFromTestCase(MismatchTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

    test_suite = ut.TestLoader().loadTestsFromTestCase(UnifyTestCase)
    ut.TextTestRunner(verbosity=2).run(test_suite)

