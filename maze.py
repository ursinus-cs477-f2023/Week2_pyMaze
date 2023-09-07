import numpy as np
import matplotlib.pyplot as plt

class Maze:
    def __init__(self, path):
        """
        Initialize the maze

        Parameters
        ----------
        path: string
            Path to file containing maze.  Should be an RGB image
            with black indicating blocked off, white indicating open,
            blue indicating start, and red indicating goal
        """
        img = plt.imread(path)
        maze = np.zeros((img.shape[0], img.shape[1]))
        maze[np.sum(img, axis=2) > 0] = 1
        self.maze = maze
        start = np.where(img[:, :, 2]*(img[:, :, 1]==0))
        self.start = (start[0][0], start[1][0])
        end = np.where(img[:, :, 0]*(img[:, :, 2]==0))
        self.end = (end[0][0], end[1][0])

    def plot(self):
        plt.imshow(self.maze, cmap='gray')
        plt.scatter(self.start[1], self.start[0], c='C0')
        plt.scatter(self.end[1], self.end[0], c='C3')

    def solve(self):
        # Tuples of (location on frontier, location that we expanded to get this)
        frontier = [{"state":self.start, "came_from":None}]
        
        # Keep an additional set for the state tuples on the frontier so that we
        # can quickly look up what's on the frontier
        frontier_set = set([self.start])

        finished = False
        M = self.maze.shape[0] # Number of rows
        N = self.maze.shape[1] # Number of cols
        visited = set([]) # Set of visited nodes
        while not finished and len(frontier) > 0:
            # Breadth-first search
            # Remove what's at the front of my frontier list
            state_info = frontier.pop(0) # Take out first element
            state = state_info["state"]
            # Also remove from fast frontier lookup structure
            frontier_set.remove(state) 
            visited.add(state)
            if state == self.end:
                finished = True
            else:
                # Expand node; look at neighbors
                (i, j) = state
                for (di, dj) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    # For each neighbor
                    i2 = i + di
                    j2 = j + dj
                    if i2 >= 0 and i2 < M and j2 >= 0 and j2 < N:
                        if self.maze[i2, j2] > 0: # White cell (open)
                            # If it exists in the maze
                            if not (i2, j2) in visited and not (i2, j2) in frontier_set:
                                frontier.append({"state":(i2, j2), "came_from":state_info})
                                frontier_set.add((i2, j2))

        ## Backtrace solution
        solution = [self.end]
        node = state_info
        while node: # As long as we actually came from somewhere
            solution.append(node["state"])
            node = node["came_from"]
        solution.reverse()
        return solution
            