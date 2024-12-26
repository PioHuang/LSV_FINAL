# Puzzle Solving Using Modern Sat Solvers

This project initially focuses on solving simpler combinatorial problems, such as the Bridges Puzzle (Hashiwokakero), as a foundation for developing encoding techniques and understanding the application of SAT solvers. Building on this groundwork, the project will then tackle the more complex sequential problem Sokoban Puzzle, a challenging single-agent strategy game that demands exponential backtracking if solved through brute force.
The Sokoban puzzle can be encoded and represented as a Bounded Model Checking (BMC) problem and solved using an SAT solver. By adopting BMC, we can determine the shortest sequence of movements required to complete the game.

## Installation

To compile the project, you will need a C++ compiler and the ABC framework.

1. Clone the repository:

   ```sh
   git clone https://github.com/PioHuang/LSV_FINAL
   cd LSV_FINAL
   ```

2. Make the project:
   ```sh
   make
   ```

### Usage
### Hashiwokakero Solver
1. Navigate to the **Hashiwokakero** directory.  
2. Modify the `p.py` file to define the following:
   - Island positions `(x, y)`.
   - The number of required bridges for each island.
3. Run the program to generate the solution, ensuring all constraints are satisfied.

### Sokoban Solver
The sokoban solver is integrated into the Berkeley ABC framework.
The sokoban solver codes are within src/ext-lsv
First execute abc:

```sh
./abc
```

then run the sokoban solver with the following command:

```sh
sokoban <map_file_path> <run_type>
```

for example:

```sh
sokoban maps/map1.txt 1
```

(1 for BMC, 2 for BMC with binary search)
