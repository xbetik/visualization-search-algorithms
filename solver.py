import sys, json, collections
from posix import access

def write_description(file, description_info):
    str_buff = ""
    if description_info[0] == "1":
        str_buff = "#BACKTRACKING" + "\n"
    elif description_info[0] == "2":
        str_buff = "#LOOK-AHEAD-FORWARD-CHECKING" + "\n"
    elif description_info[0] == "3":
        str_buff = "#LOOK-AHEAD-ARC-CONSISTENCY" + "\n" 
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
    str_buff+="#description_size=16,node_size=400,edge_size=1.5,variable_label_size=20,node_label_size=16\n"
    file.write(str_buff)

def create_config(solution, nodes, input_file_name, description_info):
    f = open(input_file_name, "w+")
    write_description(f, description_info)
    f.write("r0 root 1\n")
    for counter, node in enumerate(nodes, start=2):
        partial_string = "r0"
        domains = node[0]
        node_name = None
        for domain in domains:
            variable = domain[0]
            value = domain[1]
            partial_string += variable + str(value)
            node_name = value
        partial_string += " " + str(node_name) + " "
        partial_string += str(counter)
        
        if node[1] == "d":
            partial_string += " s r"
        if any(node[0] == s for s in solution):
            partial_string += " b"
        if node[2] != None:
            partial_string += " " + '"' + "l1 (c" + str(node[2]+1) + ")"
        if node[3] != None:
            partial_string += ' "l2 '
            place_separator = False
            for key in list(node[3].keys())[::-1]:
                if place_separator:
                    partial_string += ",, "
                partial_string += key + " : "
                if node[3].get(key) == []:
                    partial_string += "{}"
                else:
                    partial_string += str(set(node[3].get(key)))
                place_separator = True
        f.write(partial_string + "\n")

def satisfies(partial_solution, constraints):
    for counter, constraint in enumerate(constraints):
        try:
            if not eval(constraint, partial_solution):
                return False, counter
        except:
            pass
    return True, None
            
    unified_constraints.append(constraint)
    return unified_constraints

def backtracking(domains, constraints, partial_solution, solution, nodes):
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
            satisfy, constraint_index = satisfies(partial_solution.copy(), constraints)
            if satisfy:
                nodes.append((list(partial_solution.items()), "p", constraint_index, None))
                backtracking(domains, constraints, partial_solution, solution, nodes)
            else:
                nodes.append((list(partial_solution.items()), "d", constraint_index, None))
        partial_solution.popitem()
        domains[name] = values_original

def dead_end(accessible_domains):
    return any(value==[] for value in accessible_domains.values())

def select_forward_check(partial_solution, domains, constraints):
    accessible_domains = {key : [] for key in domains.keys()}
    for variable in domains.keys():
        for value in domains.get(variable):
            partial_solution[variable] = value
            satisfy, constraint_index = satisfies(partial_solution.copy(), constraints)
            if satisfy:
                accessible_domains.get(variable).append(value)
        partial_solution.popitem()
    return accessible_domains

def forward_checking(domains, constraints, partial_solution, solution, nodes):
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
            accessible_domains = select_forward_check(partial_solution, domains, constraints)
            if dead_end(accessible_domains):
                nodes.append((list(partial_solution.items()), "d", None, accessible_domains))
            else:
                nodes.append((list(partial_solution.items()), "p", None, accessible_domains))
                forward_checking(accessible_domains, constraints, partial_solution, solution, nodes)
        partial_solution.popitem()
        domains[name] = values_original

def select_arc_consistency(partial_solution, domains, constraints, solution, additionals):
    accessible_domains = select_forward_check(partial_solution, domains, constraints)
    while not dead_end(accessible_domains) and len(accessible_domains.keys()) > 1:
        domain = accessible_domains.popitem()
        name = domain[0]
        values = domain[1]
        temp_domain = {key : domains[key][:] for key in accessible_domains.keys()}
        additionals.append(domain)
        for counter, value in enumerate(values):
            partial_solution[name] = value
            accessible_domains = select_arc_consistency(partial_solution, accessible_domains, constraints, solution, additionals)
            if dead_end(accessible_domains) and value != values[len(values)-1]:
                    accessible_domains = temp_domain
        partial_solution.popitem()
    return accessible_domains

def arc_consistency(domains, constraints, partial_solution, solution, nodes):
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
            additionals = []
            accessible_domains = select_arc_consistency(partial_solution, domains, constraints, solution, additionals)
            for additional in additionals[::-1]:
                accessible_domains[additional[0]] = additional[1]
            access_copy = {key : accessible_domains[key][:] for key in accessible_domains.keys()}
            if dead_end(accessible_domains):
                nodes.append((list(partial_solution.items()), "d", None, access_copy))
            else:
                nodes.append((list(partial_solution.items()), "p", None, access_copy))
                arc_consistency(accessible_domains, constraints, partial_solution, solution, nodes)
        partial_solution.popitem()

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
        "2" : forward_checking,
        "3" : arc_consistency
        }
    partial_solution = {}
    solution = []
    nodes = []
    domains_copy = {key : domains[key][:] for key in domains.keys()}
    ordered_domains = collections.OrderedDict(sorted(domains_copy.items())[::-1])
    options[algorithm](ordered_domains, constraint_list, partial_solution, solution, nodes)
    description_info = (algorithm, domains, constraint_list)
    create_config(solution, nodes, input_file_name, description_info)

if __name__ == "__main__":
    args = sys.argv
    algorithm = args[1] # 1-backtracking, 2-look-ahead-forward-checking, 3-look-ahead-arc-consistency
    domains = args[2]
    constraints = args[3]
    solve(algorithm, domains, constraints, "input.txt")
