import random

# Define the rock-paper-scissors rules
RULES = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

class Civilization:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.hexagons = set()
        self.power = 10

    def add_hexagon(self, hexagon):
        self.hexagons.add(hexagon)

    def remove_hexagon(self, hexagon):
        self.hexagons.remove(hexagon)

    def attack(self, target):
        attack_type = random.choice(list(RULES.keys()))
        if RULES[attack_type] == target.defense_type:
            target.owner.remove_hexagon(target)
            target.owner = self
            self.add_hexagon(target)
        elif RULES[attack_type] == self.defense_type:
            self.remove_hexagon(target)
            target.owner = None
        else:
            target.defend(self, attack_type)

    def defend(self, attacker, attack_type):
        if RULES[attack_type] == self.defense_type:
            self.remove_hexagon(attacker.hexagons.pop())
            attacker.power -= 1
        else:
            self.power -= 1

class Hexagon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.owner = None
        self.defense_type = None

    def set_owner(self, owner):
        self.owner = owner
        owner.add_hexagon(self)

    def set_defense_type(self, defense_type):
        self.defense_type = defense_type

    def __str__(self):
        return f"({self.x}, {self.y}): {self.owner.name if self.owner else 'unoccupied'}"

# Initialize the grid
GRID_SIZE = 10
hex_grid = [[Hexagon(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]

# Initialize the civilizations
civ_a = Civilization('Civilization A', (255, 0, 0))
civ_b = Civilization('Civilization B', (0, 255, 0))

# Place hexagons on the grid
hex_grid[0][0].set_owner(civ_a)
hex_grid[0][0].set_defense_type('rock')
hex_grid[0][1].set_owner(civ_b)
hex_grid[0][1].set_defense_type('paper')

# Print the initial state of the grid
for row in hex_grid:
    print([str(hexagon) for hexagon in row])

# Run the simulation
while True:
    # Check for a winner
    if len(civ_a.hexagons) == 0:
        print(f"{civ_b.name} wins!")
        break
    elif len(civ_b.hexagons) == 0:
        print(f"{civ_a.name} wins!")
        break

    # Civ A takes a turn
    if civ_a.power > 0:
        hexagon = random.choice(list(civ_a.hexagons))
        adjacent_hexagons = []
        if hexagon.x > 0:
            adjacent_hexagons.append(hex_grid[hexagon.x - 1][hexagon.y])
        if hexagon.x < GRID_SIZE - 1:
            adjacent_hexagons.append(hex_grid[hexagon.x + 1][hexagon.y])
        if hexagon.y > 0:
            adjacent_hexagons.append(hex_grid[hexagon.x][hexagon.y - 1])
        if hexagon.y < GRID_SIZE - 1:
                adjacent_hexagons.append(hex_grid[hexagon.x][hexagon.y + 1])
        target_hexagon = random.choice([hexagon for hexagon in adjacent_hexagons if hexagon.owner is not None and hexagon.owner != civ_a])
        if target_hexagon:
            civ_a.attack(target_hexagon.owner)

    # Civ B takes a turn
    if civ_b.power > 0:
        hexagon = random.choice(list(civ_b.hexagons))
        adjacent_hexagons = []
        if hexagon.x > 0:
            adjacent_hexagons.append(hex_grid[hexagon.x - 1][hexagon.y])
        if hexagon.x < GRID_SIZE - 1:
            adjacent_hexagons.append(hex_grid[hexagon.x + 1][hexagon.y])
        if hexagon.y > 0:
            adjacent_hexagons.append(hex_grid[hexagon.x][hexagon.y - 1])
        if hexagon.y < GRID_SIZE - 1:
            adjacent_hexagons.append(hex_grid[hexagon.x][hexagon.y + 1])
        target_hexagon = random.choice([hexagon for hexagon in adjacent_hexagons if hexagon.owner is not None and hexagon.owner != civ_b])
        if target_hexagon:
            civ_b.attack(target_hexagon.owner, )

    # Print the current state of the grid
    print("")
    for row in hex_grid:
        print([str(hexagon) for hexagon in row])
    
    # Reduce power of each civilization by 1
    civ_a.power -= 1
    civ_b.power -= 1