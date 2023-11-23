from operator import lt, ne, eq, gt, ge
from Variable import Variable
from Constraint import Constraint
from CSP import CSP
from Con_solver import Con_solver
from SearchTree import SearchTree


def ne_(val):
    """not equal value"""

    # nev = lambda x: x != val # alternative definition
    # nev = partial(neq,val) # another alternative definition
    def nev(x):
        return val != x

    nev.__name__ = f"{val} != "  # name of the function
    return nev


def nep1(val1, val2):
    return val1 != val2 + 1


def is_(val):
    """is a value"""

    # isv = lambda x: x == val # alternative definition
    # isv = partial(eq,val) # another alternative definition
    def isv(x):
        return val == x

    isv.__name__ = f"{val} == "
    return isv


domain = {1, 2, 3, 4}

A = Variable('A', domain, position=(0.1, 0.1))
B = Variable('B', domain, position=(0.9, 0.9))
C = Variable('C', domain, position=(0.1, 0.9))
D = Variable('D', domain, position=(0.9, 0.1))
E = Variable('E', domain, position=(0.5, 0.5))
C0 = Constraint([A, D], gt, "A > D")
C1 = Constraint([D, E], gt, "D > E")
C2 = Constraint([C, A], ne, "C != A")
C3 = Constraint([C, E], gt, "C > E")
C4 = Constraint([C, D], ne, "C != D", position=(0.5, 0.25))
C5 = Constraint([B, A], ge, "B >= A", position=(0.65, 0.75))
C6 = Constraint([B, C], ne, "B != C")
C7 = Constraint([C, D], nep1, "C != D+1", position=(0.9, 0.5))
variables = {A, B, C, D, E}
cons = {C0, C1, C2, C3, C4, C5, C6, C7}
tree = SearchTree(variables, cons)
tree.print_tree()  # generate the solutions with the backtrack algorithm

csp = CSP("csp", variables, cons)
domain_dic = {}
todo_set = set({})

# printing domain for each variable
print("\n")
for v in csp.variables:
    print(f'{v.name} -> {v.domain}')
    domain_dic.update({v: v.domain})

csp.show(showDomains=True)

# Domain pruning
print("\n")
for c in csp.constraints:
    todo_set.add((c.scope[0], c))
    todo_set.add((c.scope[1], c))

for a in Con_solver(csp).generate_sols():
    print(a)
    pass

csp.show(showDomains=True)

