from Displayable import Displayable
class Con_solver(Displayable):
    """Solves a CSP with arc consistency and domain splitting
    """
    def __init__(self, csp):
        """a CSP solver that uses arc consistency
        * csp is the CSP to be solved
        """
        self.csp = csp
        super().__init__() # Or Displayable.__init__(self)

    def make_arc_consistent(self, domains=None, to_do=None):
        """Makes this CSP arc-consistent using generalized arc consistency
        domains is a variable:domain dictionary
        to_do is a set of (variable,constraint) pairs
        returns the reduced domains (an arc-consistent variable:domain
        tionary)
        """
        if domains is None:
            self.domains = {var:var.domain for var in self.csp.variables}
        else:
            self.domains = domains.copy() # use a copy of domains

        if to_do is None:
            to_do = {(var, const) for const in self.csp.constraints for var in const.scope}
        else:
            to_do = to_do.copy() # use a copy of to_do

        self.display(5,"Performing AC with domains", self.domains)
        while to_do:
            self.arc_selected = (var, const) = self.select_arc(to_do)
            self.display(5, "Processing arc (", var, ",", const, ")")
            other_vars = [ov for ov in const.scope if ov != var]
            new_domain = {val for val in self.domains[var] if self.any_holds(self.domains, const, {var:val}, other_vars)}

            if new_domain != self.domains[var]:
                self.add_to_do = self.new_to_do(var, const) - to_do
                self.display(3, f"Arc: ({var}, {const}) is inconsistent\n" f"Domain pruned, dom({var}) = {new_domain} due to {const}.\n {self.domains[var]-new_domain} have been removed")
                self.domains[var] = new_domain
                self.display(4, " adding", self.add_to_do if self.add_to_do else "nothing", "to to_do.")
                to_do |= self.add_to_do # set union
            self.display(5, f"Arc: ({var},{const}) now consistent")
        self.display(5, "AC done. Reduced domains", self.domains)
        return self.domains

    def new_to_do(self, var, const):
        """returns new elements to be added to to_do after assigning
        variable var in constraint const.
        """
        return {(nvar, nconst) for nconst in self.csp.var_to_const[var] if nconst != const for nvar in nconst.scope if nvar != var}

    def select_arc(self, to_do):
        """Selects the arc to be taken from to_do .
        * to_do is a set of arcs, where an arc is a (variable,constraint)
        r
        the element selected must be removed from to_do.
        """
        return to_do.pop()

    def any_holds(self, domains, const, env, other_vars, ind=0):
        """returns True if Constraint const holds for an assignment
        that extends env with the variables in other_vars[ind:]
        env is a dictionary
        """
        if ind == len(other_vars):
            return const.holds(env)
        else:
            var = other_vars[ind]
            for val in domains[var]:
                if self.any_holds(domains, const, env|{var:val}, other_vars, ind + 1):
                    return True
        return False

    def generate_sols(self, domains=None, to_do=None, context=dict()):
        """return list of all solution to the current CSP
        to_do is the list of arcs to check
        context is a dictionary of splits made (used for display)
        """
        new_domains = self.make_arc_consistent(domains, to_do)

        print("\nUpdated Domains: ")
        for v in self.csp.variables:
            v.domain = new_domains[v]
            print(f'{v.name} -> {v.domain}')
        if any(len(new_domains[var]) == 0 for var in new_domains):
            self.display(1,f"No solutions for context {context}")
            print("\n")
        elif all(len(new_domains[var]) == 1 for var in new_domains):
            self.display(1, "solution:", str({var: select(new_domains[var]) for var in new_domains}))
            print("\n")
            yield {var: select(new_domains[var]) for var in new_domains}
        else:
            var = self.select_var(x for x in self.csp.variables if (len(new_domains[x])) > 1)
            dom1, dom2 = partition_domain(new_domains[var])
            self.display(5, "...splitting", var, "into", dom1, "and", dom2)
            new_doms1 = new_domains | {var:dom1}
            new_doms2 = new_domains | {var:dom2}
            to_do = self.new_to_do(var, None)
            self.display(4, " adding", to_do if to_do else "nothing", "to to_do.")
            yield from self.generate_sols(new_doms1, to_do, context|{var:dom1})
            yield from self.generate_sols(new_doms2, to_do, context|{var:dom1})

    def solve_all(self, domains=None, to_do=None):
        return list(self.generate_sols())

    def solve_one(self, domains=None, to_do=None):
        return select(self.generate_sols())

    def select_var(self, iter_vars):
        """return the next variable to split"""
        return select(iter_vars)

def partition_domain(dom):
    """partitions domain dom into two.
    """
    split = len(dom) // 2
    dom1 = set(list(dom)[:split])
    dom2 = dom - dom1
    return dom1, dom2

def select(iterable):
    """select an element of iterable. Returns None if there is no such element.

    This implementation just picks the first element.
    For many of the uses, which element is selected does not affect correctness,
    but may affect efficiency.
    """
    for e in iterable:
        return e # returns first element found


