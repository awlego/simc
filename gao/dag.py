import time
from collections import defaultdict
from tqdm import tqdm

# Define the complete skill tree as a directed acyclic graph with section point requirements
skill_tree = {
    'A1': {'children': ['B1', 'B2', 'B3'], 'points': 1, 'section': 1},
    'B1': {'children': ['C1'], 'points': 1, 'section': 1},
    'B2': {'children': ['C2'], 'points': 1, 'section': 1},
    'B3': {'children': ['C3'], 'points': 1, 'section': 1},
    'C1': {'children': ['D1', 'E2'], 'points': 1, 'section': 1},
    'C2': {'children': ['D2'], 'points': 1, 'section': 1},
    'C3': {'children': ['D3'], 'points': 1, 'section': 1},
    'D1': {'children': ['E1'], 'points': 1, 'section': 1},
    'D2': {'children': ['E3', 'E4', 'E5'], 'points': 1, 'section': 1},
    'D3': {'children': ['E6'], 'points': 1, 'section': 1},
    'E1': {'children': ['F1'], 'points': 1, 'section': 2},
    'E2': {'children': ['F1', 'F2'], 'points': 1, 'section': 2},
    'E3': {'children': ['F2', 'F3'], 'points': 1, 'section': 2},
    'E4': {'children': ['F3'], 'points': 1, 'section': 2},
    'E5': {'children': ['F4', 'F5'], 'points': 1, 'section': 2},
    'E6': {'children': ['F5', 'F6'], 'points': 1, 'section': 2},
    'F1': {'children': ['G1', 'H1'], 'points': 1, 'section': 2},
    'F2': {'children': ['G2', 'H2'], 'points': 1, 'section': 2},
    'F3': {'children': ['G2', 'G3'], 'points': 1, 'section': 2},
    'F4': {'children': ['G4', 'G5'], 'points': 1, 'section': 2},
    'F5': {'children': ['G5'], 'points': 1, 'section': 2},
    'F6': {'children': ['G5', 'H5'], 'points': 1, 'section': 2},
    'G1': {'children': ['H1', 'H2'], 'points': 1, 'section': 2},
    'G2': {'children': ['H2'], 'points': 1, 'section': 2},
    'G3': {'children': ['H2', 'H3', 'H4'], 'points': 1, 'section': 2},
    'G4': {'children': ['H4'], 'points': 1, 'section': 2},
    'G5': {'children': ['H4', 'H5'], 'points': 1, 'section': 2},
    'H1': {'children': ['I1'], 'points': 1, 'section': 3},
    'H2': {'children': ['I1', 'I2'], 'points': 1, 'section': 3},
    'H3': {'children': ['I3', 'I4'], 'points': 1, 'section': 3},
    'H4': {'children': ['I4', 'I5'], 'points': 1, 'section': 3},
    'H5': {'children': ['I5', 'I6'], 'points': 1, 'section': 3},
    'I1': {'children': ['J1', 'J2'], 'points': 1, 'section': 3},
    'I2': {'children': ['J2'], 'points': 1, 'section': 3},
    'I3': {'children': ['J2', 'J3', 'J4'], 'points': 1, 'section': 3},
    'I4': {'children': ['J4'], 'points': 1, 'section': 3},
    'I5': {'children': ['J4', 'J5'], 'points': 1, 'section': 3},
    'I6': {'children': ['J5'], 'points': 1, 'section': 3},
    'J1': {'children': [], 'points': 1, 'section': 3},
    'J2': {'children': [], 'points': 1, 'section': 3},
    'J3': {'children': [], 'points': 1, 'section': 3},
    'J4': {'children': [], 'points': 1, 'section': 3},
    'J5': {'children': [], 'points': 1, 'section': 3},
}

section_requirements = {
    2: 8,  # 8 points required to unlock section 2
    3: 20  # 20 points required to unlock section 3
}

def calculate_points(activated_skills):
    return sum(skill_tree[skill]['points'] for skill in activated_skills)

def calculate_section_points(activated_skills, section):
    return sum(skill_tree[skill]['points'] for skill in activated_skills 
               if skill_tree[skill]['section'] == section)

def is_section_unlocked(activated_skills, section):
    if section == 1:
        return True
    total_points = calculate_points(activated_skills)
    return total_points >= section_requirements[section]

def get_available_skills(activated_skills):
    available = set()
    for skill in activated_skills:
        for child in skill_tree[skill]['children']:
            if child not in activated_skills and is_section_unlocked(activated_skills, skill_tree[child]['section']):
                available.add(child)
    return available

def generate_combinations(skill_tree, target_points):
    """Performs a dynamic programming search to find all valid combinations in the skill tree, 
    given the target_points and respecting the section requirements and the tree pathing.
    
    It will correctly backtrack and continue down the paths if downwards searching stopped due to 
    hitting the section point requirements"""

    valid_combinations = set()

    if target_points == 0:
        return valid_combinations
    
    if target_points == 1:
        valid_combinations.update(frozenset(['A1']))
        return valid_combinations
    
    pbar = tqdm(total=0, desc="Total combinations found", position=0)

    def search(current_node, activated_skills, valid_combinations):
        # print()
        # put a point in the current node
        activated_skills.add(current_node)
        # print("Current activated skills: ", activated_skills)

        # check if we have enough points
        talent_points_spent = calculate_points(activated_skills)

        # if we do, add the combination to the set.
        if talent_points_spent == target_points:
            # print("frozenset of activated_skills before adding to valid combos: ", frozenset(activated_skills))
            valid_combinations.add(frozenset(activated_skills))
            # print("Valid combinations: ", valid_combinations)
            activated_skills.remove(current_node)

            pbar.total = len(valid_combinations)
            pbar.desc = f"Total combinations found: {pbar.total}"
            pbar.refresh()
            
            # return early, don't bother searching children since we're already at max points.
            return valid_combinations
        
        # if we have too many points, return and don't bother searching children
        if talent_points_spent >= target_points:
            # remove the current skill so we're back at the right number.
            activated_skills.remove(current_node)
            return valid_combinations
        
        # (we don't have enough points) for child in node children, search deeper
        for node in tqdm(get_available_skills(activated_skills), desc=f"Exploring nodes from {current_node}", leave=False):
            # print("Exploring branch ", node)
            valid_combinations = search(node, activated_skills, valid_combinations)
        
        # remove the current skill so we can backtrack
        activated_skills.remove(current_node)
        return valid_combinations
    
    root_node = 'A1'
    activated_skills = set()
    search(root_node, activated_skills, valid_combinations)
    return valid_combinations
    
    


# Example usage
target_points = 43
start_time = time.time()
valid_combinations = generate_combinations(skill_tree, target_points)
end_time = time.time()
print(f"Found {len(valid_combinations)} valid combinations for {target_points} points:")
for combo in valid_combinations:
    print(combo)

print(f"Time taken: {end_time - start_time:.2f} seconds")


# # Example usage
# activated_skills = ['A1', 'B1', 'B2', 'B3']
# print("Initially available skills:", get_available_skills(activated_skills))
# print("Total points:", calculate_points(activated_skills))
# print("Points in section 1:", calculate_section_points(activated_skills, 1))
# print("Section 2 unlocked:", is_section_unlocked(activated_skills, 2))

# # Activate more skills to unlock section 2
# activated_skills.extend(['C1', 'C2', 'C3', 'D1'])
# print("\nAfter activating more skills:")
# print("Available skills:", get_available_skills(activated_skills))
# print("Total points:", calculate_points(activated_skills))
# print("Section 2 unlocked:", is_section_unlocked(activated_skills, 2))
# print("Section 3 unlocked:", is_section_unlocked(activated_skills, 3))



    





# def count_combinations(target_points):
#     """Performs a depth-first search to find the number of valid combinations in the skill tree, 
#     given the target_points and respecting the section requirements."""
    
#     def dfs(node, current_points, activated):
#         if current_points == target_points:
#             return 1
#         if current_points > target_points:
#             return 0
        
#         count = 0
#         for child in skill_tree[node]['children']:
#             if child not in activated:
#                 child_section = skill_tree[child]['section']
#                 if is_section_unlocked(activated, child_section):
#                     new_points = current_points + skill_tree[child]['points']
#                     new_activated = activated | {child}
#                     count += dfs(child, new_points, new_activated)
        
#         return count

#     return dfs('A1', skill_tree['A1']['points'], {'A1'})

# # Function to find and print example combinations
# def find_combinations(target_points):
#     def dfs(node, current_points, activated):
#         print(node, current_points, activated)
#         if current_points == target_points:
#             yield activated
#             return
#         if current_points > target_points:
#             return
        
#         for child in skill_tree[node]['children']:
#             if child not in activated:
#                 child_section = skill_tree[child]['section']
#                 if is_section_unlocked(activated, child_section):
#                     new_points = current_points + skill_tree[child]['points']
#                     new_activated = activated | {child}
#                     yield from dfs(child, new_points, new_activated)

#     return dfs('A1', skill_tree['A1']['points'], {'A1'})

# # Example usage
# start_time = time.time()
# combinations = count_combinations(31)
# end_time = time.time()

# print(f"Number of valid combinations with 31 points: {combinations}")
# print(f"Time taken: {end_time - start_time:.2f} seconds")

# # Print a few example combinations
# print("\nExample valid combinations:")
# for i, combination in enumerate(find_combinations(31)):
#     print(f"Combination {i + 1}: {sorted(combination)}")
#     if i == 4:  # Limit to 5 examples
#         break
    



# def count_combinations(target_points):
#     def dfs(node, current_points, activated):
#         if current_points == target_points:
#             print("Valid combination:", activated)
#             return 1
#         if current_points > target_points:
#             return 0
        
#         count = 0
#         for child in skill_tree[node]['children']:
#             if child not in activated:
#                 # Check if all prerequisites are met
#                 prerequisites_met = all(prereq in activated for prereq in get_prerequisites(child))
#                 if prerequisites_met:
#                     new_points = current_points + skill_tree[child]['points']
#                     activated.add(child)
#                     count += dfs(child, new_points, activated)
#                     activated.remove(child)
        
#         return count

#     def get_prerequisites(node):
#         prereqs = set()
#         for skill, data in skill_tree.items():
#             if node in data['children']:
#                 prereqs.add(skill)
#                 prereqs.update(get_prerequisites(skill))
#         return prereqs

#     total_count = dfs('A1', skill_tree['A1']['points'], {'A1'})
#     return total_count

# # Example usage
# combinations = count_combinations(31)
# print(f"Number of valid combinations with 31 points: {combinations}")

# # Function to find and print example combinations
# def find_combinations(target_points):
#     def dfs(node, current_points, activated):
#         print(node, current_points, activated)
#         if current_points == target_points:
#             yield activated.copy()
#             return
#         if current_points > target_points:
#             return
        
#         for child in skill_tree[node]['children']:
#             if child not in activated:
#                 prerequisites_met = all(prereq in activated for prereq in get_prerequisites(child))
#                 if prerequisites_met:
#                     new_points = current_points + skill_tree[child]['points']
#                     activated.add(child)
#                     yield from dfs(child, new_points, activated)
#                     activated.remove(child)

#     def get_prerequisites(node):
#         prereqs = set()
#         for skill, data in skill_tree.items():
#             if node in data['children']:
#                 prereqs.add(skill)
#                 prereqs.update(get_prerequisites(skill))
#         return prereqs

#     return dfs('A1', skill_tree['A1']['points'], {'A1'})

# # Print a few example combinations
# print("\nExample valid combinations:")
# for i, combination in enumerate(find_combinations(31)):
#     print(f"Combination {i + 1}: {sorted(combination)}")
#     if i == 4:  # Limit to 5 examples
#         break



# def count_combinations_dp(target_points):
#     # Create a reverse mapping of the skill tree
#     parents = defaultdict(list)
#     for skill, data in skill_tree.items():
#         for child in data['children']:
#             parents[child].append(skill)

#     # Initialize the DP table
#     dp = defaultdict(lambda: defaultdict(int))

#     # Start with leaf nodes
#     leaf_nodes = [skill for skill, data in skill_tree.items() if not data['children']]
#     for leaf in leaf_nodes:
#         dp[leaf][skill_tree[leaf]['points']] = 1

#     # Topological sort (simplified for this tree structure)
#     sorted_skills = leaf_nodes
#     while len(sorted_skills) < len(skill_tree):
#         for skill in skill_tree:
#             if skill not in sorted_skills and all(child in sorted_skills for child in skill_tree[skill]['children']):
#                 sorted_skills.append(skill)

#     # Bottom-up DP
#     for skill in reversed(sorted_skills):
#         skill_points = skill_tree[skill]['points']
#         for points, count in dp[skill].items():
#             for parent in parents[skill]:
#                 new_points = points + skill_tree[parent]['points']
#                 if new_points <= target_points:
#                     dp[parent][new_points] += count

#     # Sum up all combinations that reach exactly target_points
#     total_combinations = sum(dp[skill][target_points] for skill in skill_tree)

#     return total_combinations

# # Example usage
# start_time = time.time()
# combinations = count_combinations_dp(31)
# end_time = time.time()

# print(f"Number of unique combinations with 31 points: {combinations}")
# print(f"Time taken: {end_time - start_time:.2f} seconds")

# # Function to find example combinations using DP results
# def find_combinations_dp(target_points):
#     dp_results = count_combinations_dp(target_points)
    
#     def backtrack(skill, remaining_points, current_combination):
#         if remaining_points == 0:
#             yield current_combination
#             return
        
#         for child in skill_tree[skill]['children']:
#             child_points = skill_tree[child]['points']
#             if child_points <= remaining_points:
#                 yield from backtrack(child, remaining_points - child_points, current_combination + [child])

#     return backtrack('A1', target_points - skill_tree['A1']['points'], ['A1'])

# # Print a few example combinations
# print("\nExample combinations:")
# for i, combination in enumerate(find_combinations_dp(31)):
#     print(f"Combination {i + 1}: {sorted(combination)}")
#     if i == 4:  # Limit to 5 examples
#         break