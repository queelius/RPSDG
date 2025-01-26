import itertools
from collections import deque

# Define labels for clarity
LABELS = ['N', 'E', 'S', 'W']

def rotate_switches(switches, rotation):
    """
    Rotate the switches by the given rotation index.
    rotation=0: 0 degrees
    rotation=1: 90 degrees clockwise
    rotation=2: 180 degrees
    rotation=3: 270 degrees
    """
    return switches[-rotation:] + switches[:-rotation]

def all_up_or_down(switches):
    """Check if all switches are either all up or all down."""
    return all(state == 1 for state in switches) or all(state == 0 for state in switches)

def set_labels(switches, rotation, labels_to_set, value):
    """
    Set the specified labels to the given value (0 or 1).
    """
    new_switches = switches.copy()
    for label in labels_to_set:
        index = (LABELS.index(label) + rotation) % 4
        new_switches[index] = value
    return new_switches

def procedure_steps():
    """
    Define the procedure steps as a list of label pairs to set to up.
    Step 1: N & E
    Step 2: E & S
    Step 3: S & W
    Step 4: W & N
    Step 5: Any two adjacent (for testing, we'll systematically set them as N & E)
    """
    return [
        ['N', 'E'],  # Step 1
        ['E', 'S'],  # Step 2
        ['S', 'W'],  # Step 3
        ['W', 'N'],  # Step 4
        ['N', 'E'],  # Step 5 (optional)
    ]

def generate_all_initial_states():
    """Generate all possible initial switch states and rotations."""
    switch_states = list(itertools.product([0, 1], repeat=4))  # 16 states
    rotations = [0, 1, 2, 3]  # 4 possible rotations
    return list(itertools.product(switch_states, rotations))  # 64 combinations

def simulate_procedure():
    """
    Simulate the procedure for all initial states and rotations.
    Returns True if the procedure works for all cases, False otherwise.
    """
    initial_states = generate_all_initial_states()
    steps = procedure_steps()
    
    for initial_switches, initial_rotation in initial_states:
        # Use BFS to explore all possible rotation sequences
        queue = deque()
        # Each queue entry: (current_switches, current_rotation, step_number)
        queue.append((list(initial_switches), initial_rotation, 0))
        visited = set()
        
        success = False
        
        while queue:
            current_switches, current_rotation, step_number = queue.popleft()
            state_id = (tuple(current_switches), current_rotation, step_number)
            
            if state_id in visited:
                continue
            visited.add(state_id)
            
            if all_up_or_down(current_switches):
                success = True
                continue  # No need to proceed further from this state
            
            if step_number >= len(steps):
                continue  # Exceeded step limit without success
            
            # Apply the current step
            current_step = steps[step_number]
            # For step 5, you might choose any adjacent pair. For simplicity, we follow the defined sequence.
            new_switches = set_labels(current_switches, current_rotation, current_step, 1)  # Set to up
            
            if all_up_or_down(new_switches):
                success = True
                continue  # Success achieved
            
            # After setting, the pillar may rotate to any of the four orientations
            for rotation in range(4):
                rotated_switches = rotate_switches(new_switches, rotation)
                queue.append((rotated_switches, rotation, step_number + 1))
        
        if not success:
            print("Procedure FAILED for initial switches:", initial_switches, "with rotation:", initial_rotation)
            return False
    
    print("Procedure SUCCEEDS for all initial states and rotations.")
    return True

if __name__ == "__main__":
    simulate_procedure()
