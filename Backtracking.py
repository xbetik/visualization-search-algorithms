def satisfies(domain_dict, constraints):
    for constraint in constraints:
        unsigned_key = False
        for key in domain_dict.keys():
            if key in constraint:
                unsigned_key = True
        if not unsigned_key:
            if not eval(constraint):
                return False
    return True

def select_value(domain, domain_name, constraints, domain_dict):
    while domain != []:
        value = domain.pop(0)
        domain_dict[domain_name] = value
        
        print(domain_dict)
        
        assigned_constraints = []
        for constraint in constraints:
            for key in domain_dict.keys():
                if domain_dict.get(key) != None:
                    constraint = constraint.replace(str(key), str(domain_dict[key]))
            assigned_constraints.append(constraint)
        if satisfies(domain_dict, assigned_constraints):
            return value
    return None
        
def backtracking_algorithm(domains, constraints):
    solution = []
    domain_dict = {d[1] : None for d in domains}
    domain_index = 0
    domain_names = [d[1] for d in domains]
    domain_values = [d[0] for d in domains]
    domain_values_old = [d[0] for d in domains]
    current_domain = domain_values[domain_index][:]
    
    while 0 <= domain_index <= len(domains)-1:
        new_value = select_value(current_domain, domain_names[domain_index], constraints, domain_dict)
        if new_value is None: # backward phase
            domain_dict[domain_names[domain_index]] = None
            domain_values[domain_index] = domain_values_old[domain_index][:]
            domain_index-=1
            current_domain = domain_values[domain_index][:]
        else: # forward phase
            domain_values[domain_index] = current_domain[:]
            domain_index+=1
            if domain_index <= len(domains)-1:
                current_domain = domain_values[domain_index][:]
            else:
                vals = list(domain_dict.values())
                solution.append(vals)
                if domain_values == [ [] for _ in domain_values ]:
                    return solution
                else:
                    domain_index-=1
                    domain_dict[domain_names[domain_index]] = None
                    current_domain = domain_values[domain_index][:]
    if domain_index == -1:
        return solution

domains = [([1,2,3], "a"), ([1,2,3], "b"), ([1,2,3], "c")]
#constraints = ["a > b", "b > c"]
constraints = ["a == 3*c"]
print(backtracking_algorithm([([1,2,3], "a"), ([1,2,3], "b"), ([1,2,3], "c")], constraints))

