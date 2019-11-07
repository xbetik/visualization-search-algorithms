import solver
import unittest
from constraint import *

def general_solver(params):
    domain, constraint, _ = params[0], params[1], params[2] 
    con_lambda = constraint[0]
    con_var = constraint[1]
    problem = Problem()
    for var_name, values in enumerate(domain, start=97):
        problem.addVariable(chr(var_name), values)
    problem.addConstraint(con_lambda, con_var)
    solution = problem.getSolutions()
    solution = [sorted(list(s.items())) for s in solution]
    return sorted(solution)

'''
def general_solver(params):
    domain, constraint, _ = params[0], params[1], params[2] 
    problem = Problem()
    for var_name, values in enumerate(domain, start=97):
        problem.addVariable(chr(var_name), values)
    problem.addConstraint(constraint)
    solution = problem.getSolutions()
    solution = [sorted(list(s.items())) for s in solution]
    return sorted(solution)
'''
def my_solver(params, algorithm):
    domain, _, constraint = params[0], params[1], params[2] 
    domain_string = "{"
    for var_name, values in enumerate(domain, start=97):
        if var_name != 97:
            domain_string += ', '
        domain_string += '"' + chr(var_name) + '" : ' + str(set(values))
    domain_string += "}"
    solution = solver.test(algorithm, domain_string, constraint)
    solution = [sorted(s) for s in solution]
    return sorted(solution)

class UnaryConstraints(unittest.TestCase):
    def test_one_variable_one_constraint(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[9]), my_solver(data[9], str(i)))            
    def test_more_variables_one_constraints(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[10]), my_solver(data[10], str(i)))            
            self.assertEqual(general_solver(data[11]), my_solver(data[11], str(i)))            

class BinaryConstraints(unittest.TestCase):
    def test_sample1(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[0]), my_solver(data[0], str(i)), "D: a,b,c={1,2,3} C: a>b,b>c")
    def test_sample2(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[1]), my_solver(data[1], str(i)), "D: a,b,c={0,1,2,4} C: a==b*2,b>c")
    def test_sample5(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[2]), my_solver(data[2], str(i)), "D: a={2,3} b={1,2,3}, c={1,2,3}, d={1,2} C: a!=b,b==c,b!=d,c!=d")
    def test_sample8(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[3]), my_solver(data[3], str(i)), "D: a={1,2,3} b={2,3}, c={1,2,3,4}, d={2,3,4} C: a==b,c>=b,d<b")
    def test_sample9(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[4]), my_solver(data[4], str(i)), "D: a={0,1,2,3,4,5} b={0,1,2,3,4,5}, c={0,1,2,3,4,5}, d={0,1,2,3,4,5} C: a>2*b,b>=c,c==d+1")
    def test_custom(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[5]), my_solver(data[5], str(i)))
    def test_advanced(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[6]), my_solver(data[6], str(i)))
    def test_noSolution(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[7]), my_solver(data[7], str(i)))
    def my_test(self):
        for i in range(1,4):
            self.assertEqual(general_solver(data[8]), my_solver(data[8], str(i)))

data = [
    (
        [[1,2,3], [1,2,3], [1,2,3]],    
        (lambda a,b,c : a>b and b>c, ("a","b","c")),
        'a>b,b>c'
        ),
    (
        [[0,1,2,4], [0,1,2,4], [0,1,2,4]],
        (lambda a,b,c : a==b*2 and b>c, ("a","b","c")),
        'a==b*2,b>c'
        ),
    (
        [[2,3],[1,2,3],[1,2,3],[1,2]],
        (lambda a,b,c,d : a!=b and b==c and b!=d and c!=d, ("a","b","c","d")),
        'a!=b,b==c,b!=d,c!=d'
        ),
    (
        [[1,2,3],[2,3],[1,2,3,4],[2,3,4]],
        (lambda a,b,c,d : a==b and c>=b and d<b, ("a","b","c","d")),
        'a==b,c>=b,d<b'
        ),
    (
        [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5]],
        (lambda a,b,c,d : a>2*b and b>=c and c==d+1, ("a","b","c","d")),
        'a>2*b,b>=c,c==d+1'
        ),
    (
        [[1,2,3], [1,2,3], [1,2,3]],
        (lambda a,b,c : a==3*c, ("a","b","c")),
        'a==3*c'
        ),
    (
        [[1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10]],
        (lambda a,b,c,d : a+8<c and b==5*d, ("a","b","c","d")),
        'a+8<c,b==5*d'
        ),
    (
        [[1,2,3],[1,2,3],[1,2,3]],
        (lambda a : a<1, ("a")),
        'a<1'
        ),
    (   
        [[1,2,3,4],[1,2,3],[1,2,3]],
        (lambda a,b,c : a>c and b==3*c,("a","b","c")),
        'a>c,b==3*c'
        ),
    (   
        [[1,2,3,4]],
        (lambda a : a>2,("a")),
        'a>2'
        ),
    (
        [[1,2,3,4], [1,2,3,4], [1,2,3], [9,10]],
        (lambda a : a<4,("a")),
        'a<4'
        ),
    (
        [[1,2,3,4], [1,2,3,4], [1,2,3], [9,10]],
        (lambda b : b<4,("b")),
        'b<4'
        )
    ]

if __name__ == '__main__':
    unittest.main()
