import sys, json, collections

def write_description(description_info):
    str_buff = ""
    if description_info[0] == "1":
        str_buff = "#BACKTRACKING\n"
    elif description_info[0] == "2":
        str_buff = "#FORWARD-CHECKING\n"
    elif description_info[0] == "3":
        str_buff = "#FULL LOOK-AHEAD\n" 
    elif description_info[0] == "4":
        str_buff = "#GASCHNIG-BACKJUMPING\n"
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
    str_buff+="#description_size=16,node_size=400,edge_size=1.5,variable_label_size=20,node_label_size=16,show_frame=false,colored_limit=none,animation_speed=500\n"
    return str_buff

def create_config(solution, nodes, description_info, jumps):
    ret_string = write_description(description_info)
    ret_string += "path:=R0;name:=none;order:=1\n"
    for i, node in enumerate(nodes, start=2):
        partial_string = "path:=R0"
        domains = node[0]
        node_name = None
        for domain in domains:
            variable = domain[0]
            value = domain[1]
            partial_string += variable + str(value)
            node_name = value
        partial_string += ";name:=" + str(node_name)
        partial_string += ";order:=" +str(i)
        
        if node[1] == "d":
            partial_string += ";shape:=square;color:=red"
        if any(node[0] == s for s in solution):
            partial_string += ";color:=blank"
        if any(node[0] == j for j in jumps):
            partial_string += ";jump:=yes"
        if node[2]:
            partial_string += ";bottom_label:="
            for l in node[2]:
                if l != node[2][0]:
                    partial_string += ","
                partial_string += "(c" + str(l+1) + ")"
        if node[3]:
            partial_string += ";side_label:="
            for l in node[3]:
                if l!=node[3][0]:
                    partial_string += "&&"
                for c in l[2]:
                    if c != l[2][0]:
                        partial_string += ","
                    partial_string += "c" + str(c+1)
                if l[1]:
                    partial_string += "->" + l[0] + ":" + str(set(l[1]))
                else:
                    partial_string += "->" + l[0] + ":{}"
        ret_string += partial_string
        if node != nodes[len(nodes)-1]:
            ret_string += "\n"
    return ret_string

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

def dead_end(accessible_domains):
    return any(value==[] for value in accessible_domains.values())

def select_forward_check(partial_solution, domains, constraints, d_behavior):
    accessible_domains = {key : [] for key in domains.keys()}
    constraints_applied = {key : [] for key in domains.keys()}
    for variable in domains.keys():
        inconsistent_constraints = []
        for value in domains.get(variable):
            partial_solution[variable] = value
            is_consistent = consistent(partial_solution.copy(), constraints, inconsistent_constraints)
            if is_consistent:
                accessible_domains.get(variable).append(value)
        if accessible_domains.get(variable) != domains.get(variable):
            d_behavior.append((variable, accessible_domains.get(variable)[:], inconsistent_constraints))
        partial_solution.popitem()
    return accessible_domains

def forward_checking(domains, constraints, partial_solution, solution, nodes, _):
    if not domains:
        if consistent(partial_solution.copy(), constraints, []):
            solution.append(list(partial_solution.items()))
        else:
            nodes.pop()
            nodes.append((list(partial_solution.items()), "d", None, None))
    else:
        domain = domains.popitem()
        name = domain[0]
        values = domain[1]
        values_original = domain[1][:]
        while values:
            value = values.pop(0)
            partial_solution[name] = value
            d_behavior = []
            accessible_domains = select_forward_check(partial_solution, domains, constraints, d_behavior)
            if dead_end(accessible_domains):
                nodes.append((list(partial_solution.items()), "d", None, d_behavior))
            else:
                nodes.append((list(partial_solution.items()), "p", None, d_behavior))
                forward_checking(accessible_domains, constraints, partial_solution, solution, nodes, _)
        partial_solution.popitem()
        domains[name] = values_original

def revise(constraints, dom_name1, values1, dom_name2, values2, inconsistent_constraints):
    changed_domain = []
    for value1 in values1:
        consistent_value_found = False
        for value2 in values2:
            is_consistent = consistent({dom_name1 : value1, dom_name2 : value2}, constraints, inconsistent_constraints)
            if is_consistent:
                consistent_value_found = True
        if consistent_value_found:
            changed_domain.append(value1)
    return changed_domain

def reviseAll(domains, constraints, name, value, d_behavior):
    domain_queue = [(name, [value])]
    for d in domains.items():
        domain_queue.append((d[0], d[1]))
    while domain_queue:
        name, values = domain_queue.pop(0)
        for d in list(domains.items()):
            if d[0] != name:
                inconsistent_constraints = []
                changed_domain = revise(constraints, d[0], d[1], name, values, inconsistent_constraints)
                if changed_domain != d[1]:
                    domains[d[0]] = changed_domain 
                    changed = True
                    domain_queue.append((d[0], changed_domain))
                    if inconsistent_constraints:
                        d_behavior.append((d[0], changed_domain[:], inconsistent_constraints))
    return domains

def full_look_ahead(domains, constraints, partial_solution, solution, nodes, _):    
    if not domains:
        if consistent(partial_solution.copy(), constraints, []):
            solution.append(list(partial_solution.items()))
        else:
            nodes.pop()
            nodes.append((list(partial_solution.items()), "d", None, None))
    else:
        domain = domains.popitem()
        name = domain[0]
        values = domain[1]
        while values:
            value = values.pop(0)
            partial_solution[name] = value
            domains_copy = {key : domains[key][:] for key in domains.keys()}
            d_behavior = []
            changed_domains = reviseAll(domains_copy, constraints, name, value, d_behavior)
            if any(value == [] for value in changed_domains.values()):
                nodes.append((list(partial_solution.items()), "d", None, d_behavior))
            else:
                nodes.append((list(partial_solution.items()), "p", None, d_behavior))
                full_look_ahead(changed_domains, constraints, partial_solution, solution, nodes, _)
            partial_solution.popitem()

def satisfies_backjumping(partial_solution, constraints, variables, latest):
    for i in range(len(variables)-1, -1, -1):
        for counter, constraint in enumerate(constraints):
            if variables[i] in constraint:
                if variables[i] != list(partial_solution.keys())[-1]:
                    latest = i
                    try:
                        if not eval(constraint, partial_solution):
                            return False, counter, latest
                    except:
                        pass
    return True, None, latest

def select_value(domains, i, constraints, partial_solution, nodes, latest):
    variables = list(domains.keys())[::-1]
    variable = variables[i]
    values = domains[variable]
    while values:
        value = values.pop(0)
        partial_solution[variable] = value
        satisfy, constraint_index, latest = satisfies_backjumping(partial_solution.copy(), constraints, variables, latest)
        if satisfy:
            nodes.append((list(partial_solution.items()), "p", constraint_index, None))
            return value, latest
        else:
            nodes.append((list(partial_solution.items()), "d", constraint_index, None))
    return None, latest

def reset_values(i, domains, domains_copy, partial_solution):
    if partial_solution:
        for j in range(i, len(list(domains.keys()))):
            domains[list(domains.keys())[::-1][j]] = domains_copy[list(domains.keys())[::-1][j]][:]
            partial_solution.popitem()

def gaschnig_backjumping(domains, constraints, partial_solution, solution, nodes, jumps):
    i = 0
    latest = 0
    domains_copy = {key : domains[key][:] for key in domains.keys()}
    while i >= 0:
        value, latest = select_value(domains, i, constraints, partial_solution, nodes, latest)        
        if not value:
            if latest != i-1:
                jumps.append(list(partial_solution.items()))
            i = latest
            reset_values(i+1, domains, domains_copy, partial_solution)
        else:
            if i+1 < len(domains.keys()):
                i += 1
            else:
                solution.append(list(partial_solution.items()))
                if all(val == [] for val in list(domains.values())):
                    return None
                reset_values(i, domains, domains_copy, partial_solution)
                i-=1

def parse(dom, constraints):
    dom_temp = dom[1:len(dom)-1]
    dom_temp = dom_temp.replace("{", "[")
    dom_temp = dom_temp.replace("}", "]")
    dom_temp = "{" + dom_temp + "}"
    return json.loads(dom_temp), constraints.split(",")

def test(algorithm, domains, constraints):
    domains, constraint_list = parse(domains, constraints)
    options = { 
        "1" : backtracking,
        "2" : forward_checking,
        "3" : full_look_ahead,
        "4" : gaschnig_backjumping
        }
    partial_solution = {}
    solution = []
    nodes = []
    jumps = []
    domains_copy = {key : domains[key][:] for key in domains.keys()}
    ordered_domains = collections.OrderedDict(sorted(domains_copy.items())[::-1])
    options[algorithm](ordered_domains, constraint_list, partial_solution, solution, nodes, jumps)
    return solution

def solve(algorithm, domains, constraints):
    domains, constraint_list = parse(domains, constraints)
    options = { 
        "1" : backtracking,
        "2" : forward_checking,
        "3" : full_look_ahead,
        "4" : gaschnig_backjumping
        }
    partial_solution = {}
    solution = []
    nodes = []
    jumps = []
    domains_copy = {key : domains[key][:] for key in domains.keys()}
    ordered_domains = collections.OrderedDict(sorted(domains_copy.items())[::-1])
    options[algorithm](ordered_domains, constraint_list, partial_solution, solution, nodes, jumps)
    description_info = (algorithm, domains, constraint_list)
    config_str = create_config(solution, nodes, description_info, jumps)
    return config_str

if __name__ == "__main__":
    args = sys.argv
    algorithm = args[1]
    domains = args[2]
    constraints = args[3]
    solve(algorithm, domains, constraints)
