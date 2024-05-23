from docplex.mp.model import Model

# Define sets
conference_sessions = 3
slots = 2
length_of_paper_range = 2
NbrGrps = 2

Sessions = range(1, conference_sessions + 1)
Slots = range(1, slots + 1)
PaperRangeIndex = range(1, length_of_paper_range + 1)
Groups = range(1, NbrGrps + 1)

# Parameters
papers_range = [2, 3]  # Adjusted to have at least one paper per session
np = [3, 3, 3]  # Adjusted to ensure enough papers for each session
npMax = [2, 3]  # Adjusted to ensure slots can accommodate the papers
max_parallel_sessions = 2
session_groups = [
    [1], [2], [3]
]

def var_x(s, c, l):
    return (s-1)*slots *length_of_paper_range  + (c-1)*length_of_paper_range + l

# Define variables and model
mdl = Model()

# Decision Variables
x = {(s, c, l): mdl.integer_var(name=f'x_{s}_{c}_{l}') for s in Sessions for c in Slots for l in PaperRangeIndex}

# Constraints
for s in Sessions:
    for c in Slots:
        vars_for_s_c = [x[s, c, l] for l in PaperRangeIndex]
        mdl.add_constraint(mdl.sum(vars_for_s_c) <= 1)

for s in Sessions:
    aux_vars = []
    aux_weights = []
    for c in Slots:
        for l in PaperRangeIndex:
            aux_vars.append(x[s, c, l])
            aux_weights.append(papers_range[l-1])
    mdl.add_constraint(mdl.sum(aux_vars[i] * aux_weights[i] for i in range(len(aux_vars))) == np[s-1])

for s in Sessions:
    for c in Slots:
        for l in PaperRangeIndex:
            if papers_range[l-1] > npMax[c-1]:
                mdl.add_constraint(x[s, c, l] == 0)

# Solve the model
solution = mdl.solve()

# Check and print the solution values for the variables
if solution:
    for s in Sessions:
        for c in Slots:
            for l in PaperRangeIndex:
                value = x[s, c, l].solution_value
                print(f"x[{s}, {c}, {l}] = {value}")
else:
    print("No solution found")
