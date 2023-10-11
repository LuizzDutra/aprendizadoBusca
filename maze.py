import sys


class Node():
    def __init__(self, state, parent, action, dist):
        self.state = state
        self.parent = parent
        self.action = action
        self.dist = dist
    def get_dist(self, goal_state):
        return (goal_state[0] - self.state[0]) - (goal_state[1] - self.state[1])


class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node: Node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def is_empty(self):
        return len(self.frontier) == 0
    
    def remove(self) -> Node:
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self) -> Node:
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node 
        
class GreedyFrontier(StackFrontier):
    def remove(self, goal_state) -> Node:
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            min_index = 0

            for i in range(len(self.frontier)):
                if self.frontier[i].get_dist(goal_state) < self.frontier[min_index].get_dist(goal_state):
                    min_index = i

        
            #self.frontier.remove[min_index]
            node = self.frontier[min_index]
            self.frontier = self.frontier[0:min_index] + self.frontier[min_index+1:]

            return node
        
class AStarFrontier(StackFrontier):
    def remove(self, goal_state) -> Node:
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            min_index = 0

            for i in range(len(self.frontier)):
                first_node = self.frontier[i]
                second_node = self.frontier[min_index]
                if first_node.get_dist(goal_state) + first_node.dist < second_node.get_dist(goal_state) + second_node.dist:
                    min_index = i

            node = self.frontier[min_index]
            self.frontier = self.frontier[0:min_index] + self.frontier[min_index+1:]

            return node

#Souce Code from Harvard AI course
class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("â–ˆ", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    #my attempt of the solve algorithm while peeking
    def solve(self):
        
        self.num_explored = 0

        self.frontier = AStarFrontier()
        self.frontier.add(Node(self.start, None, None, 0))
        self.explored = set()

        while True:

            if self.frontier.is_empty():
                raise Exception("No solution")
            
            node = self.frontier.remove(self.goal)
            #node = self.frontier.remove()

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent != None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            #mark as explored
            self.explored.add(node.state)
            self.num_explored += 1

            for action, state in self.neighbors(node.state):
                if not self.frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, dist=node.dist+1)
                    self.frontier.add(child)

    #back to course code
    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                        ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)