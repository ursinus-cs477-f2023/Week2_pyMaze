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
        pass
        ## TODO: Fill this in in class