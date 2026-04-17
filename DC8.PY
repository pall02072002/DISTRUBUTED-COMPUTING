# Experiment 8: Task Assignment using Hungarian Algorithm

import itertools

# Input
n = int(input("Enter number of tasks/processors (square matrix): "))

print("Enter cost matrix:")
cost = []
for i in range(n):
    row = list(map(int, input().split()))
    cost.append(row)

min_cost = float('inf')
best_assignment = None

# Generate all possible assignments (permutations)
for perm in itertools.permutations(range(n)):
    current_cost = 0
    
    for i in range(n):
        current_cost += cost[i][perm[i]]
    
    # Check minimum cost
    if current_cost < min_cost:
        min_cost = current_cost
        best_assignment = perm

# Output
print("\n--- Optimal Task Assignment ---")
for i in range(n):
    print(f"Task {i+1} -> Processor {best_assignment[i]+1} (Cost: {cost[i][best_assignment[i]]})")

print(f"\nMinimum Total Cost: {min_cost}")