import random

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

def set_any_two_adjacent(switches, value):
    """
    Set any two adjacent switches to the given value (0 or 1).
    Since rotation is unknown, we'll select a random adjacent pair each time.
    """
    adjacent_pairs = [
        (0, 1),  # N & E
        (1, 2),  # E & S
        (2, 3),  # S & W
        (3, 0),  # W & N
    ]
    # Randomly select one adjacent pair
    pair = random.choice(adjacent_pairs)
    switches[pair[0]] = value
    switches[pair[1]] = value
    return switches

def visualize_pillar(switches):
    """
    Print a simple ASCII representation of the pillar's current state.
    """
    state_map = {1: 'U', 0: 'D'}
    n, e, s, w = [state_map[sw] for sw in switches]
    
    print("\n    [N]: {} ".format(n))
    print("     |")
    print("[W]: {} -- [E]: {}".format(w, e))
    print("     |")
    print("    [S]: {}".format(s))
    print()

def perform_random_rotation(switches):
    """
    Randomly rotate the pillar by 0°, 90°, 180°, or 270°.
    """
    rotation = random.randint(0, 3)  # 0 to 3 corresponding to 0°,90°,180°,270°
    return rotate_switches(switches, rotation)

def initialize_pillar():
    """
    Initialize the pillar with a random switch configuration and rotation.
    """
    # Random switch states: 0 (Down) or 1 (Up)
    switches = [random.randint(0, 1) for _ in range(4)]
    # Random initial rotation
    rotation = random.randint(0, 3)
    switches = rotate_switches(switches, rotation)
    return switches

def simulate_experiment():
    """
    Simulate one experiment of the procedure.
    """
    # Initialize pillar
    switches = initialize_pillar()
    print("=== Initial Pillar State ===")
    visualize_pillar(switches)
    
    # Define procedure steps
    steps = [
        ('Set two adjacent switches to Up', 1),
        ('Set two adjacent switches to Down', 0),
        ('Set two adjacent switches to Up', 1),
        ('Set two adjacent switches to Down', 0),
        ('Set two adjacent switches to Up', 1),
    ]
    
    for step_num, (action_desc, value) in enumerate(steps, start=1):
        print(f"--- Step {step_num}: {action_desc} ---")
        switches = set_any_two_adjacent(switches, value)
        visualize_pillar(switches)
        
        # Check for uniformity
        if all_up_or_down(switches):
            print("All switches are now uniform.")
            print(f"Procedure succeeded in {step_num} steps.")
            return
        
        # Perform random rotation
        switches = perform_random_rotation(switches)
        print("Pillar rotated randomly.")
        visualize_pillar(switches)
    
    # After five steps, check uniformity
    if all_up_or_down(switches):
        print("All switches are now uniform.")
        print("Procedure succeeded in 5 steps.")
    else:
        print("Procedure failed to set all switches uniformly within 5 steps.")

if __name__ == "__main__":
    simulate_experiment()
