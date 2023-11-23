class SearchTree(object):
    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints
        self.sorted_vars = sorted(self.variables, key=lambda x: x.name)

    def valid(self, assignment):
        return all(con.holds(assignment) for con in self.constraints if con.can_evaluate(assignment))

    def valid_with(self, assignment, var, value):
        """returns True if assignment + {var:value} is valid
        """
        return self.valid(assignment | {var: value})

    def next_unassigned_variable(self, assignment):
        # we assume that not all variables are assigned
        return next(v for v in self.sorted_vars if v not in assignment)

    def backtrack(self, assignment, depth, solutions=[]):
        if len(assignment) == len(self.variables):
            last = self.sorted_vars[-1]
            value = assignment[last]
            if self.valid(assignment):
                print(pad_of_length("    ", depth - 1) + (last.name + "=" + str(value)) + " (success)")
                solutions.append(assignment)
                return  # even if we found a solution, we continue to find all solutions
            else:
                # unreachable because else it would be valid
                print(pad_of_length("    ", depth - 1) + (last.name + "=" + str(value)) + " (failure)")
                return

        var = self.next_unassigned_variable(assignment)

        for value in var.domain:
            assignment[var] = value
            print(pad_of_length("    ", depth) + (var.name + "=" + str(value)), end="")
            # Check if current partial assignment violates any constraint
            if self.valid_with(assignment, var, value):
                print(" valid")
                self.backtrack(assignment.copy(), depth + 1, solutions)
            else:
                print(" invalid")

        del assignment[var]  # backtrack
        return  # No valid assignment found

    def print_tree(self):
        """
            prints the tree of the search like:
        """
        sols = []
        self.backtrack({}, 0, sols)
        print(f"Found {len(sols)} solutions: {str(sols)}")


def pad_of_length(s, length):
    if length <= 0:
        return ""
    return s * length


def branch(depth):
    if (depth <= 0):
        return "   "
    return "|__" + "___" * (depth - 1)


def assignment_to_string(assignment):
    items = sorted(assignment.items(), key=lambda x: x[0].name)
    return " ".join(f"{var}={value}" for var, value in items)


def last_n_assignments_to_string(assignments, n):
    # prints the last n assignments (inclusive)
    items = sorted(assignments.items(), key=lambda x: x[0].name)
    if len(items) <= n:
        return " ".join(f"{var}={value}" for var, value in items)
    return " ".join(f"{var}={value}" for var, value in items[-n:])
