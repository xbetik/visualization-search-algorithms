import cgi, sys, json

def write_description(file, description_info):
    str_buff = ""
    if description_info[0] == "1":
        str_buff = "#" + "BACKTRACKING" + "\n"
    elif description_info[0] == "2":
        str_buff = "#" + "LOOK-AHEAD" + "\n"
    str_buff += "#"
    for key in list(description_info[1].keys()):
        if not str_buff.endswith("#"):
            str_buff += ","
        str_buff += key
        for value in description_info[1][key]:
            str_buff += " " + str(value)
    str_buff += "\n"
    str_buff += "#"
    for counter, constraint in enumerate(description_info[2], start=1):
        if not str_buff.endswith("#"):
            str_buff += ","
        str_buff += "c" + str(counter) + " : " + constraint
    str_buff+="\n"
    file.write(str_buff)

def create_config(solutions, partial_solutions, d_names, input_file_name, description_info):
    f = open(input_file_name, "w+")
    write_description(f, description_info)
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
        if sol[3] != None:
            partial_string += ' "l2 '
            for dom_index, domain in enumerate(sol[3]):
                if dom_index != 0:
                    partial_string += ",, "
                partial_string += d_names[dom_index] + " : "
                if domain == []:
                    partial_string += "{}"
                else:
                    partial_string += str(set(domain))
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
        satisfy, const_index = satisfies(domain_dict, assigned_constraints)
        if satisfy:
            partial_solutions.append((list(domain_dict.values()), "p", const_index, None))
            return value
        partial_solutions.append((list(domain_dict.values()), "d", const_index, None))
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

def unificate(value, dict, constraints, domain_key):
    dict[domain_key] = value
    unified_constraints = []
    for constraint in constraints:
        for key in dict.keys():
            if dict.get(key) != None:
                constraint = constraint.replace(str(key), str(dict[key]))
        unified_constraints.append(constraint)
    return unified_constraints

def dead_end_occurs(i, values):
    return any(val==[] for val in values[i:])

def reset(index_from, values, values_original):
    for i in range(index_from, len(values)):
        values[i] = values_original[i][:]
    return values

def select_value_forward_checking(values, names, index, constraints, dict, values_original, partial_solutions):
    current_values = values[index]
    while current_values != []:
        current_value = current_values.pop(0)
        dict[names[index]] = current_value
        for i in range(index+1,len(values)):
            for value in values[i][:]:
                unified_constraints = unificate(value, dict, constraints, names[i])
                satisfy, const_index = satisfies(dict, unified_constraints)
                if not satisfy:
                    values[i].remove(value)
            dict[names[i]] = None
        if not dead_end_occurs(index+1, values):
            partial_solutions.append((list(dict.values()), "p", None, [x[:] for x in values]))
            return current_value
        partial_solutions.append((list(dict.values()), "d", None, [x[:] for x in values]))
        values = reset(index+1, values, values_original)
    return None

def look_ahead(domains, constraints):
    solution, domain_dict, domain_names, domain_values, domain_values_old = init(domains)
    values_original = [value[:] for value in domain_values]
    domain_index = 0
    partial_solutions = []
    while 0 <= domain_index < len(domains):
        new_value = select_value_forward_checking(domain_values, domain_names, domain_index, constraints, domain_dict, values_original, partial_solutions)
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
        return solution, partial_solutions

def parse(dom, constraints):
    dom_temp = dom[1:len(dom)-1]
    dom_temp = dom_temp.replace("{", "[")
    dom_temp = dom_temp.replace("}", "]")
    dom_temp = "{" + dom_temp + "}"
    return json.loads(dom_temp), constraints.split(",")
    
def solve(algorithm, domains, constraints, input_file_name):
    domains, constraint_list = parse(domains, constraints)
    options = { 
        "1" : backtracking,
        "2" : look_ahead,
        }
    solutions, partial_solutions = options[algorithm](domains, constraint_list)
    description_info = (algorithm, domains, constraint_list)
    create_config(solutions, partial_solutions, list(domains.keys()), input_file_name, description_info)

if __name__ == "__main__":
    args = sys.argv
    algorithm = args[1] # 1-backtracking, 2-look-ahead
    domains = args[2]
    constraints = args[3]
    solve(algorithm, domains, constraints, "input.txt")


