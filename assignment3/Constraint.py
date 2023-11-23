class Constraint(object):
    """A Constraint consists of
    * scope: a tuple of variables
    * condition: a Boolean function that can applied to a tuple of values
    variables in scope
    * string: a string for printing the constraints. All of the strings
    t be unique.
    for the variables
    """
    def __init__(self, scope, condition, string=None, position=None):
        self.scope = scope
        self.condition = condition
        if string is None:
            self.string = f"{self.condition.__name__}({self.scope})"
        else:
            self.string = string
            self.position = position

    def __repr__(self):
        return self.string

    def can_evaluate(self, assignment):
        """
        assignment is a variable:value dictionary
        returns True if the constraint can be evaluated given assignment
        """
        return all(v in assignment for v in self.scope)

    def holds(self,assignment):
        """returns the value of Constraint con evaluated in assignment.
        precondition: all variables are assigned in assignment, ie
        f.can_evaluate(assignment) is true
        """
        return self.condition(*tuple(assignment[v] for v in self.scope))
