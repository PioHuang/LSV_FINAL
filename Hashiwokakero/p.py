from z3 import *
import matplotlib.pyplot as plt




island_numbers = [4, 3, 1, 4, 4, 3, 4, 2, 1, 4, 6]
P_x = [0, 0, 3, 4, 1, 1, 2, 3, 1, 4, 2]
P_y = [0, 4, 4, 0, 3, 4, 2, 2, 1, 3, 0]
n = len(island_numbers)



island_numbers = [3, 3, 2, 1, 2, 1, 3, 2, 3, 3, 8, 4, 1, 1, 3, 5, 3, 2, 2, 4, 1, 2, 3, 2]
P_x = [0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6]
P_y = [0, 2, 3, 4, 6, 4, 6, 1, 2, 0, 3, 6, 0, 4, 1, 3, 4, 6, 0, 1, 2, 3, 4, 5]
n = len(island_numbers)


island_numbers = [1, 5, 4, 1, 2, 2, 1, 6, 4, 4, 3, 2, 8, 3, 1, 2, 3, 8, 2, 2, 5, 2, 3, 3, 2, 1, 3, 6, 5, 2]
P_x = [0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 9, 9, 9, 9]
P_y = [0, 2, 4, 6, 8, 9, 0, 2, 4, 8, 9, 0, 2, 5, 7, 9, 0, 2, 4, 6, 8, 3, 5 ,7, 9, 8 ,0 ,2 ,7 ,9]
n = len(island_numbers)
'''
island_numbers = [4, 6, 3, 5, 7, 8, 2, 5, 7, 1, 3, 2, 2, 6, 7, 2, 6, 2, 1, 3, 2, 5, 5, 4, 7, 7, 4, 7, 6]
P_x = [4, 5, 5, 6, 9, 1, 0, 8, 5, 5, 4, 7, 9, 8, 5, 6, 4, 2, 3, 6, 1, 9, 0, 2, 1, 8, 5, 8, 0]
P_y = [1, 6, 8, 3, 6, 0, 7, 1, 2, 5, 7, 2, 5, 3, 9, 4, 2, 7, 2, 2, 6, 9, 0, 0, 9, 2, 0, 5, 9]
n = len(island_numbers)
'''

'''
island_numbers = [3, 4, 1, 4, 1, 2, 3, 4, 4, 3, 3, 6, 5, 3, 6, 5, 5, 6, 2, 4]
P_x = [7, 0, 6, 4, 9, 4, 3, 8, 0, 9, 3, 8, 8, 0, 0, 5, 5, 6, 6, 7]
P_y = [4, 2, 9, 5, 5, 8, 3, 6, 1, 6, 4, 4, 5, 0, 5, 5, 4, 8, 2, 3]
'''
solver = Solver()

# Bi,j
B = [[Int(f'B_{i}_{j}') for j in range(n)] for i in range(n)]

# Constraint 1: at most 2 bridges between each pair of islands
for i in range(n):
    for j in range(i + 1, n):
        solver.add(And(B[i][j] >= 0, B[i][j] <= 2))
        solver.add(B[i][j] == B[j][i])

# Constraint 2: every island has the correct number of bridges
for i in range(n):
    solver.add(Sum([B[i][j] for j in range(n) if i != j]) == island_numbers[i])
    
# Constraint 3: if there is a bridge between two islands, they must share a side.
for i in range(n):
    for j in range(i + 1, n):
        solver.add(Implies(B[i][j] >= 1, Or(P_x[i] == P_x[j], P_y[i] == P_y[j])))

def cross_product(x1, y1, x2, y2, x3, y3):
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

def check_crossing_and_block(model):
    # check if bridges cross each other or cross an island
    for i in range(n):
        for j in range(i + 1, n):
            if model.evaluate(B[i][j]).as_long() > 0:
                for k in range(n):
                    for l in range(k + 1, n):
                        if (i != k and j != l) and model.evaluate(B[k][l]).as_long() > 0:
                            cp1 = cross_product(P_x[i], P_y[i], P_x[j], P_y[j], P_x[k], P_y[k])
                            cp2 = cross_product(P_x[i], P_y[i], P_x[j], P_y[j], P_x[l], P_y[l])
                            cp3 = cross_product(P_x[k], P_y[k], P_x[l], P_y[l], P_x[i], P_y[i])
                            cp4 = cross_product(P_x[k], P_y[k], P_x[l], P_y[l], P_x[j], P_y[j])
                            if cp1 * cp2 < 0 and cp3 * cp4 < 0:
                                # if two bridges cross each other, block the crossing
                                print(f"Blocking crossing between bridge ({i}, {j}) and ({k}, {l})")
                                return Or(B[i][j] == 0, B[k][l] == 0)
                #  check if a bridge crosses an island
                for k in range(n):
                    if k != i and k != j and (min(P_x[i], P_x[j]) <= P_x[k] <= max(P_x[i], P_x[j]) and
                                              min(P_y[i], P_y[j]) <= P_y[k] <= max(P_y[i], P_y[j])):
                        print(f"Blocking island crossing for bridge ({i}, {j}) over island {k}")
                        return B[i][j] == 0
    return None

def draw_islands(ax, bridges, title):
    ax.set_title(title)
    ax.scatter(P_x, P_y, c='blue', s=100, zorder=2)
    for i in range(n):
        ax.text(P_x[i], P_y[i], str(island_numbers[i]), fontsize=12, ha='right', color='black')

    for bridge in bridges:
        i, j, count = bridge
        if count > 0:
            ax.plot([P_x[i], P_x[j]], [P_y[i], P_y[j]], color='green' if count == 1 else 'red', lw=2*count, zorder=1)

# the initial graph
fig, ax = plt.subplots(figsize=(6, 6))
draw_islands(ax, [], "Before Solving")
plt.tight_layout()
plt.show()

while True:
    if solver.check() == sat:
        model = solver.model()
        
        # store the bridges
        bridges = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    bridge_value = model.evaluate(B[i][j]).as_long()
                    if bridge_value > 0:
                        bridges.append((i, j, bridge_value))
        
        # check if bridges cross each other or cross an island
        blocking_clause = check_crossing_and_block(model)
        if blocking_clause is None:
            print("Found valid solution:")
            break
        else:
            solver.add(blocking_clause)
    else:
        print("No solution found.")
        break

if solver.check() == sat:
    for i in range(n):
        print(f"Island {i} at ({P_x[i]}, {P_y[i]})")
        total_bridges = 0
        for j in range(n):
            if i != j:
                bridge_value = model.evaluate(B[i][j], model_completion=True)
                if bridge_value.as_long() > 0:
                    total_bridges += bridge_value.as_long()
                    print(f"  Bridge to island {j}: {bridge_value} bridge(s)")
        print(f"Total bridges for island {i}: {total_bridges}\n")

    # the final graph
    fig, ax = plt.subplots(figsize=(6, 6))
    draw_islands(ax, bridges, "After Solving")
    plt.tight_layout()
    plt.show()
