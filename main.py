from docplex.mp.model import Model

# Define sets
conference_sessions = 40
slots = 7
length_of_paper_range = 4
NbrGrps = 20

Sessions = range(1, conference_sessions + 1)
Slots = range(1, slots + 1)
PaperRange = range(1, length_of_paper_range + 1)
Groups = range(1, NbrGrps + 1)

# Parameters
papers_range = [3, 4, 5, 6]
np = [14, 23, 12, 9, 9, 6, 10, 4, 10, 7, 6, 5, 3, 5, 6, 4, 3, 12, 7, 16, 4, 5, 14, 11, 4, 3, 10, 6, 6, 4, 13, 3, 4, 9, 5, 4, 11, 6, 6, 8]
npMax = [4, 6, 6, 4, 4, 5, 3]
max_parallel_sessions = 11
session_groups = [
    [1], [2], [3], [], [], [], [6], [7], [7, 8], [10], [8], [8, 11], [5, 8], 
    [3, 8], [7], [13], [13], [14], [], [8], [16], [16], [20], [17], [13], 
    [], [9], [11], [11, 12], [9], [6, 19], [], [], [18], [10], [5], [16], 
    [4, 5], [8, 12], [7, 15]
]

# Model
mdl = Model()

# Decision Variables
x = mdl.binary_var_dict(((s, c, l) for s in Sessions for c in Slots for l in PaperRange), name="x")
y = mdl.binary_var_dict(((s1, s2, c, g) for s1 in Sessions for s2 in Sessions if s1 < s2 for c in Slots for g in Groups), name="y")
z = mdl.binary_var_matrix(Sessions, Slots, name="z")
session_allocated = mdl.binary_var_matrix(Sessions, Slots, name="session_allocated")

# Objective Function: Minimize working-group conflicts
num_conflicts = mdl.sum(y[s1, s2, c, g] for s1 in Sessions for s2 in Sessions if s1 < s2 for c in Slots for g in Groups if g in session_groups[s1] and g in session_groups[s2])
mdl.minimize(num_conflicts)

# Constraints
# At most one amount of papers chosen for a (session, slot) pair
for s in Sessions:
    for c in Slots:
        mdl.add_constraint(mdl.sum(x[s, c, l] for l in PaperRange) <= 1)

# Subdivision of a session into slots covers all the papers in the session
for s in Sessions:
    mdl.add_constraint(mdl.sum(papers_range[l-1] * x[s, c, l] for c in Slots for l in PaperRange) == np[s-1])

# Session allocation indicator
for s in Sessions:
    for c in Slots:
        mdl.add_constraint(session_allocated[s, c] == (mdl.sum(x[s, c, l] for l in PaperRange) >= 1))

# Equivalence transformation for session-slot (z variable)
for s in Sessions:
    for c in Slots:
        mdl.add_constraint(z[s, c] == (mdl.sum(x[s, c, l] for l in PaperRange) >= 1))

# Two sessions associated with the same group and allocated to the same slot generate a conflict
for s1 in Sessions:
    for s2 in Sessions:
        if s1 < s2:
            for c in Slots:
                for g in Groups:
                    if g in session_groups[s1] and g in session_groups[s2]:
                        mdl.add_constraint(y[s1, s2, c, g] == ((session_allocated[s1, c] + session_allocated[s2, c]) == 2))

# Solve
mdl.solve()

# Print solution
print("Objective Value:", mdl.objective_value)
for v in mdl.iter_binary_vars():
    if v.solution_value > 0.5:
        print(v)
