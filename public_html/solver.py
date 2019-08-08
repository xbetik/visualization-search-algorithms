import cgi, sys, json

def create_config(solutions, partial_solutions, d_names):
    f = open("/home/xbetik/public_html/input.txt", "w+")
    f.write("r0 0 1\n")
    for counter, sol in enumerate(partial_solutions, start=2):
        partial_string = "r0"
        node_name = None
        for i in range(len(sol[0])):
            if sol[0][i] != None:
                partial_string += d_names[i] + str(sol[0][i])
                node_name = sol[0][i]
        partial_string += " " + str(node_name) + " "
        partial_string += str(counter)
        if sol[1] == "d":
            partial_string += " s r"
        if any(sol[0] == s for s in solutions):
            partial_string += " b"
        if sol[2] != None:
            partial_string += " " + '"' + "l1 (c" + str(sol[2]+1) + ")"   
        f.write(partial_string + "\n")

def satisfies(domain_dict, constraints):
    for counter, constraint in enumerate(constraints):
        unsigned_key = False
        for key in domain_dict.keys():
            if key in constraint:
                unsigned_key = True
        if not unsigned_key:
            if not eval(constraint):
                return False, counter
    return True, None

def select_value(domain, domain_name, constraints, domain_dict, partial_solutions):
    while domain != []:
        value = domain.pop(0)
        domain_dict[domain_name] = value        
        assigned_constraints = []
        for constraint in constraints:
            for key in domain_dict.keys():
                if domain_dict.get(key) != None:
                    constraint = constraint.replace(str(key), str(domain_dict[key]))
            assigned_constraints.append(constraint)
        satify, const_index = satisfies(domain_dict, assigned_constraints)
        if satify:
            partial_solutions.append((list(domain_dict.values()), "p", const_index))
            return value
        partial_solutions.append((list(domain_dict.values()), "d", const_index))
    return None

def init(domains):
    solution = []
    domain_dict = {key : None for key in list(domains.keys())}
    domain_names = list(domains.keys())
    domain_values = [list(value) for value in list(domains.values())]
    domain_values_original = [list(value)[:] for value in list(domains.values())]
    return solution, domain_dict, domain_names, domain_values, domain_values_original

def backtracking(domains, constraints):
    solution, domain_dict, domain_names, domain_values, domain_values_original = init(domains)
    domain_index = 0
    partial_solutions = []
    while 0 <= domain_index < len(domains):
        current_domain = domain_values[domain_index][:]
        new_value = select_value(current_domain, domain_names[domain_index], constraints, domain_dict, partial_solutions)
        if new_value is None: # backward phase
            domain_dict[domain_names[domain_index]] = None
            domain_values[domain_index] = domain_values_original[domain_index][:]
            domain_index-=1
        else: # forward phase
            domain_values[domain_index] = current_domain[:]
            domain_index+=1
            if domain_index == len(domains):
                vals = list(domain_dict.values())
                solution.append(vals)
                domain_index-=1
                domain_dict[domain_names[domain_index]] = None
    if domain_index == -1:
        return solution, partial_solutions

def select_value_forward_checking(values, names, index, constraints, dict, values_old):
    current_values = values[index]
    dead_end_detected = False
    while current_values != []:
        current_value = current_values.pop(0)
        dict[names[index]] = current_value
        
        print(dict)
        
        for i in range(index+1,len(values)):
            dead_end_detected = False
            for value in values[i][:]:
                dict[names[i]] = value
                assigned_constraints = []
                for constraint in constraints:
                    for key in dict.keys():
                        if dict.get(key) != None:
                            constraint = constraint.replace(str(key), str(dict[key]))
                    assigned_constraints.append(constraint)
                if not satisfies(dict, assigned_constraints):
                    values[i].remove(value)
            print(names[i], " has domain : ", values[i])
            if not values[i]:
                for j in range(index+1, i+1):
                    values[j] = values_old[j][:]
                dead_end_detected = True
                dict[names[i]] = None
                break
            dict[names[i]] = None
        if not dead_end_detected:
            return current_value
    return None

def look_ahead(domains, constraints):
    solution, domain_dict, domain_names, domain_values, domain_values_old = init(domains)
    values_original = [value[:] for value in domain_values]
    domain_index = 0
    while 0 <= domain_index < len(domains):
        new_value = select_value_forward_checking(domain_values, domain_names, domain_index, constraints, domain_dict, values_original)
        if new_value is None: # backward phase
            domain_dict[domain_names[domain_index]] = None
            domain_values[domain_index] = values_original[domain_index][:]
            domain_index-=1
        else:
            domain_index+=1
            if domain_index == len(domains):
                solution.append(list(domain_dict.values()))
                domain_index-=1
                domain_dict[domain_names[domain_index]] = None
    if domain_index == -1:
        return solution

def parse(dom, constraints):
    dom_temp = dom[1:len(dom)-1]
    dom_temp = dom_temp.replace("{", "[")
    dom_temp = dom_temp.replace("}", "]")
    dom_temp = "{" + dom_temp + "}"
    return json.loads(dom_temp), constraints.split(",")
    
def solve(algorithm, domains, constraints):
    domains, constraint_list = parse(domains, constraints)
    options = { 
        "1" : backtracking,
        "2" : look_ahead,
        }
    solutions, partial_solutions = options[algorithm](domains, constraint_list)
    create_config(solutions, partial_solutions, list(domains.keys()))

if __name__ == "__main__":
    args = sys.argv
    algorithm = args[1] # 1-backtracking, 2-look-ahead
    domains = args[2]
    constraints = args[3]
    solve(algorithm, domains, constraints)


