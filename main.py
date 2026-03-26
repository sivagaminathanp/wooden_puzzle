from itertools import permutations

cube_colours = ['Green', 'Blue', 'Yellow', 'Red']

class Puzzle:
    cubes_data = []
    constraints = {}

    def __init__(self, cube_colours):
        print("Generating all possible combinations of cube colors")
        print("---------------------------------------")
        for perm in permutations(cube_colours):
            self.cubes_data.append(list(perm))
        
        self.define_constraints()

    def define_constraints(self):
        """ 
            Creating a constraint mapping of cube positions as a rule set for the solution
            Corners: 0=Top-Left, 1=Top-Right, 2=Bottom-Right, 3=Bottom-Left
            Mapping is created for all cube positions (0-7) and the required corner matches
            0 and 1 are skipped as they are the first two cubes and have no prior constraints 
            Also we check backwards to ensure we only compare against already placed cubes, reducing the search space significantly.

            Format: cube_id: [(neighbor_cube_id, neighbor_corner, my_corner), ...]
            Example: 2: [(0, 3, 0), (0, 2, 1), (1, 0, 1), (1, 3, 2)] means:
            - For cube at position 2 (Center-1):
                - BL(3) of Cube 0 must match TL(0) of Cube 2
                - BR(2) of Cube 0 must match TR(1) of Cube 2
                - TL(0) of Cube 1 must match TR(1) of Cube 2
                - BL(3) of Cube 1 must match BR(2) of Cube 2
        """
        self.constraints = {
            2: [(0, 3, 0), (0, 2, 1), (1, 0, 1), (1, 3, 2)], # Cube 2 Constraints: BL(3) of Cube 0 matches TL(0) of Cube 2; BR(2) of Cube 0 matches TR(1) of Cube 2; TL(0) of Cube 1 matches TR(1) of Cube 2; BL(3) of Cube 1 matches BR(2) of Cube 2 
            3: [(2, 0, 1), (2, 3, 2)],            # Cube 3 Constraints: TL(0) of Cube 2 matches TR(1) of Cube 3; BL(3) of Cube 2 matches BR(2) of Cube 3
            4: [(2, 2, 1), (2, 3, 0)],            # Cube 4 Constraints: BR(2) of Cube 2 matches TR(1) of Cube 4; BL(3) of Cube 2 matches TL(0) of Cube 4
            5: [(3, 3, 0), (3, 2, 1), (4, 3, 2)], # Cube 5 Constraints: BL(3) of Cube 3 matches TL(0) of Cube 5; BR(2) of Cube 3 matches TR(1) of Cube 5; BL(3) of Cube 4 matches BR(2) of Cube 5
            6: [(5, 0, 1), (5, 3, 2)],            # Cube 6 Constraints: TL(0) of Cube 5 matches TR(1) of Cube 6; BL(3) of Cube 5 matches BR(2) of Cube 6
            7: [(5, 3, 0), (5, 2, 1)]             # Cube 7 Constraints: BL(3) of Cube 5 matches TL(0) of Cube 7; BR(2) of Cube 5 matches TR(1) of Cube 7
        }

    def rotate(self, cube, steps):
        return cube[steps:] + cube[:steps]

    def is_valid(self, grid, cube, pos):
        if pos not in self.constraints:
            return True
        
        for neighbor_idx, neighbor_corner, my_corner in self.constraints[pos]:
            if cube[my_corner] != grid[neighbor_idx][neighbor_corner]:
                return False
        return True

    def solve(self, grid, available_indices):
        # print(f"Current Grid: {grid}, Available Cubes: {available_indices}")
        if not available_indices:
            return grid

        pos = len(grid)
        for i in range(len(available_indices)):
            cube_index = available_indices[i]
            cube = self.cubes_data[cube_index]
            remaining = available_indices[:i] + available_indices[i+1:]
            
            for step in range(4):
                rotated_cube = self.rotate(cube, step)
                if self.is_valid(grid, rotated_cube, pos):
                    response = self.solve(grid + [rotated_cube], remaining)
                    if response: return response
        return None

def solve_puzzle():
    puzzle = Puzzle(cube_colours)
    solution = puzzle.solve([], list(range(8)))

    if solution:
        print("Solution Found and Puzzle Resolved! Adjacent corners match the constraint set")
        layout = ["Top-Left", "Top-Right", "Center-1", "Mid-Left", "Mid-Right", "Center-2", "Bottom-Left", "Bottom-Right"]
        for i, cube in enumerate(solution):
            print(f"{layout[i]}: {cube}")
    else:
        print("No solution found. Check if cube colors were recorded in a clockwise manner and that the constraints are correctly defined.")

if __name__ == "__main__":
    solve_puzzle()