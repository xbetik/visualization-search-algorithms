import sys, json, collections

def consistent(partial_solution, constraints):
    for counter, constraint in enumerate(constraints):
        try:
            if not eval(constraint, partial_solution):
                return False, counter
        except:
            pass
    return True, None

def revise(constraints, dom_name1, values1, dom_name2, values2):
    changed_domain = []
    for value1 in values1:
        consistent_value_found = False
        for value2 in values2:
            is_consistent, index = consistent({dom_name1 : value1, dom_name2 : value2}, constraints)
            if is_consistent:
                consistent_value_found = True
        if consistent_value_found:
            changed_domain.append(value1)
    return changed_domain

def reviseAll(domains, constraints, name, value):
    domain_queue = [(name, [value])]
    while domain_queue:
        name, values = domain_queue.pop(0)
        for d in list(domains.items()):
            if d[0] != name:
                changed_domain = revise(constraints, d[0], d[1], name, values)
                if changed_domain != d[1]:
                    domains[d[0]] = changed_domain 
                    changed = True
                    domain_queue.append((d[0], changed_domain))
    return domains

def full_look_ahead(domains, constraints, partial_solution, solution, nodes, _):
    if not domains:
        solution.append(list(partial_solution.items()))
    else:
        domain = domains.popitem()
        name = domain[0]
        values = domain[1]
        while values:
            value = values.pop(0)
            partial_solution[name] = value
            domains_copy = {key : domains[key][:] for key in domains.keys()}
            changed_domains = reviseAll(domains_copy, constraints, name, value)
            if any(value == [] for value in changed_domains.values()):
                nodes.append((list(partial_solution.items()), "d", [], []))
            else:
                nodes.append((list(partial_solution.items()), "p", [], []))
                full_look_ahead(changed_domains, constraints, partial_solution, solution, nodes, _)
            partial_solution.popitem()
            
def consistent(partial_solution, constraints, inconsistent_constraints):
    for i, constraint in enumerate(constraints):
        try:
            if not eval(constraint, partial_solution):
                if i not in inconsistent_constraints:
                    inconsistent_constraints.append(i)
                return False
        except:
            pass
    return True

def backtracking(domains, constraints, partial_solution, solution, nodes, jumps):
    if not domains:
        solution.append(list(partial_solution.items()))
    else:
        domain = domains.popitem()
        name = domain[0]
        values = domain[1]
        values_original = domain[1][:]
        while values:
            value = values.pop(0)
            partial_solution[name] = value
            inconsistent_constraints = []
            is_consistent = consistent(partial_solution.copy(), constraints, inconsistent_constraints)
            if is_consistent:
                nodes.append((list(partial_solution.items()), "p", inconsistent_constraints, None))
                backtracking(domains, constraints, partial_solution, solution, nodes, jumps)
            else:
                nodes.append((list(partial_solution.items()), "d", inconsistent_constraints, None))
        partial_solution.popitem()
        domains[name] = values_original
            
def test(algorithm, domains, constraints):
    domains = [('a',[2,3]),('b',[1,2,3]),('c',[1,2,3]),('d',[1,2])]
    constraints = constraints.split(",")
    partial_solution = {}
    solution = []
    nodes = []
    jumps = []
    full_look_ahead(domains, constraints, partial_solution, solution, nodes, jumps)
    print(solution)
    return solution

def parse(dom, constraints):
    dom_temp = dom[1:len(dom)-1]
    dom_temp = dom_temp.replace("{", "[")
    dom_temp = dom_temp.replace("}", "]")
    dom_temp = "{" + dom_temp + "}"
    return json.loads(dom_temp), constraints.split(",")

if __name__ == '__main__':
    domains = '{"a" : {2,3}, "b" : {1,2,3}, "c" : {1,2,3}, "d" : {1,2}}'
    constraints = 'a!=b,b==c,b!=d,c!=d'
    domains, constraints = parse(domains,constraints)
    partial_solution = {}
    solution = []
    nodes = []
    jumps = []
    domains = collections.OrderedDict(sorted(domains.items())[::-1])
    full_look_ahead(domains, constraints, partial_solution, solution, nodes, jumps)
    print(solution)
