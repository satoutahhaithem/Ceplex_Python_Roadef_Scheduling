from docplex.mp.model import Model

# Define sets
# conference_sessions = 40
# slots = 7
# length_of_paper_range = 4
# NbrGrps = 20

# Sessions = range(1, conference_sessions + 1)
# Slots = range(1, slots + 1)
# PaperRangeIndex = range(1, length_of_paper_range + 1)
# Groups = range(1, NbrGrps + 1)

# # Parameters
# papers_range = [3, 4, 5, 6]
# np = [14, 23, 12, 9, 9, 6, 10, 4, 10, 7, 6, 5, 3, 5, 6, 4, 3, 12, 7, 16, 4, 5, 14, 11, 4, 3, 10, 6, 6, 4, 13, 3, 4, 9, 5, 4, 11, 6, 6, 8]
# npMax = [4, 6, 6, 4, 4, 5, 3]
# max_parallel_sessions = 11
# session_groups = [
#     [1], [2], [3], [], [], [], [6], [7], [7, 8], [10], [8], [8, 11], [5, 8], 
#     [3, 8], [7], [13], [13], [14], [], [8], [16], [16], [20], [17], [13], 
#     [], [9], [11], [11, 12], [9], [6, 19], [], [], [18], [10], [5], [16], 
#     [4, 5], [8, 12], [7, 15]
# ]

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
max_var_x = var_x(conference_sessions, slots, length_of_paper_range)
def var_z(s, c): 
    return max_var_x + (s - 1) * slots + c
def decode_var_x(x, slots, papers_range_length):
    # Adjust for 1-indexing
    x -= 1  
    l = x % papers_range_length + 1
    x //= papers_range_length
    c = x % slots + 1
    s = x // slots + 1
    return s, c, l

# Model
mdl = Model()

# Decision Variables
# Decision Variables with custom names based on var_x(s, c, l) values
x = {(s, c, l): mdl.integer_var(name=f'x_{var_x(s, c, l)}') for s in Sessions for c in Slots for l in PaperRangeIndex}
y = mdl.binary_var_dict(((s1, s2, c, g) for s1 in Sessions for s2 in Sessions if s1 < s2 for c in Slots for g in Groups), name="y")
# z = mdl.binary_var_matrix(Sessions, Slots, name="z")
z = {(s, c): mdl.integer_var(name=f'z_{var_z(s, c)}') for s in Sessions for c in Slots }
session_allocated = mdl.binary_var_matrix(Sessions, Slots, name="session_allocated")

# Objective Function: Minimize working-group conflicts
num_conflicts = mdl.sum(y[s1, s2, c, g] for s1 in Sessions for s2 in Sessions if s1 < s2 for c in Slots for g in Groups if g in session_groups[s1-1] and g in session_groups[s2-1])
mdl.minimize(num_conflicts)




# First Constraint: At most one amount of papers chosen for a (session, slot) pair
for s in Sessions:
    for c in Slots:
        vars_for_s_c = []
        for l in PaperRangeIndex:
            vars_for_s_c.append(x[s, c, l])
            # print(x[s, c, l])
        # print(vars_for_s_c)
        mdl.add_constraint(mdl.sum(vars_for_s_c) <= 1)
####################################################################################





# Second Constraint: Subdivision of a session into slots covers all the papers in the session
for s in Sessions:
    aux_vars = []
    aux_weights = []
    for c in Slots:
        for l in PaperRangeIndex:
            aux_vars.append(x[s, c, l])
            aux_weights.append(papers_range[l-1])
    mdl.add_constraint(mdl.sum(aux_vars[i] * aux_weights[i] for i in range(len(aux_vars))) == np[s-1])
####################################################################################




# Third Constraint : The subdivision respects the maximum length of each slot
for s in Sessions:
    for c in Slots:
        for l in PaperRangeIndex:
            if papers_range[l-1] > npMax[c-1]:
                # print (x[s, c, l])
                mdl.add_constraint(x[s, c, l] == 0)
####################################################################################



# Fourth Constraint: Number of parallel sessions is not exceeded for each slot
for c in Slots:
    for s in Sessions:
        mdl.add_constraint(z[s, c] <= session_allocated[s, c])
        # print(z[s, c])
    mdl.add_constraint(mdl.sum(session_allocated[s, c] for s in Sessions) <= max_parallel_sessions)



# Implementing 
for s in Sessions:
    for c in Slots:
        z_var = z[s, c]
        x_vars = [x[s, c, l] for l in PaperRangeIndex]
        
        # Add an OR clause for each x_var along with z_var
        or_clause = x_vars + [z_var]
        mdl.add_constraints(x_var <= z_var for x_var in x_vars)  # Logical implication: if x_var is selected, then z_var must be selected
# solution = mdl.solve()

# # Check and print the solution values for the variables constrained to 0
# if solution:
#     for s in Sessions:
#         for c in Slots:
#             for l in PaperRangeIndex:
#                 value = x[s, c, l].solution_value
#                 print(f"x[{s}, {c}, {l}] = {value}")
# else:
#     print("No solution found")