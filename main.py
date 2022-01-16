import pygame
import numpy as np

# colours of the different types of cells
col_background = (10, 10, 40)
col_grid = (30, 30, 60)
col_about_to_die = (200, 200, 225)
col_alive = (255, 255, 215)

class Rules:
    def DieRule(self, current_cell, num_alive):
        return current_cell == 1 and num_alive < 2 or num_alive > 3
    def BirthRule(self, current_cell, num_alive):
        return (current_cell == 1 and 2 <= num_alive <= 3) or (current_cell == 0 and num_alive == 3)

    def addGosperGliderGun(self, i, j, cells):
        """adds a Gosper Glider Gun with top left
           cell at (i, j)"""
        gun = np.zeros(11 * 38).reshape(11, 38)

        gun[5][1] = gun[5][2] = 1
        gun[6][1] = gun[6][2] = 1

        gun[3][13] = gun[3][14] = 1
        gun[4][12] = gun[4][16] = 1
        gun[5][11] = gun[5][17] = 1
        gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 1
        gun[7][11] = gun[7][17] = 1
        gun[8][12] = gun[8][16] = 1
        gun[9][13] = gun[9][14] = 1

        gun[1][25] = 1
        gun[2][23] = gun[2][25] = 1
        gun[3][21] = gun[3][22] = 1
        gun[4][21] = gun[4][22] = 1
        gun[5][21] = gun[5][22] = 1
        gun[6][23] = gun[6][25] = 1
        gun[7][25] = 1

        gun[3][35] = gun[3][36] = 1
        gun[4][35] = gun[4][36] = 1

        cells[i:i + 11, j:j + 38] = gun

    def addGlider(self, i, j, cells):
        """adds a glider with top left cell at (i, j)"""
        glider = np.array([[0, 0, 1],
                           [1, 0, 1],
                           [0, 1, 1]])
        cells[i:i + 3, j:j + 3] = glider


class GameOfLife:
    def __init__(self, dimx, dimy, cellsize, random = True):
        self.dimx = dimx
        self.dimy = dimy
        self.cellsize = cellsize
        self.rules = Rules()

        # Cells are implemented as Numpy Array, because it's faster than a class and i don't need
        # anything so much special for them
        cells = np.zeros((dimy, dimx))

        if random:
            cells = self.randomGrid(dimx, dimy)
        else:
            self.rules.addGosperGliderGun(5,5, cells)
            self.rules.addGlider(20, 50, cells)

        self.cells = cells
    def randomGrid(self, dimx, dimy):
        """returns a grid of X by Y random values"""
        return np.random.choice([1, 0], dimx * dimy, p=[0.2, 0.8]).reshape(dimx, dimy)

    def start(self):
        pygame.init()
        surface = pygame.display.set_mode((self.dimx * self.cellsize, self.dimy * self.cellsize))
        pygame.display.set_caption("John Conway's Game of Life")

        cells = self.cells

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            surface.fill(col_grid)
            cells = self.update(surface, cells, self.cellsize)
            pygame.display.update()

    def update(self, surface, cur, sz):
        nxt = np.zeros((cur.shape[0], cur.shape[1]))

        for r, c in np.ndindex(cur.shape):
            num_alive = np.sum(cur[r - 1:r + 2, c - 1:c + 2]) - cur[r, c]

            if self.rules.DieRule(cur[r, c], num_alive):
                col = col_about_to_die
            elif self.rules.BirthRule(cur[r, c], num_alive):
                nxt[r, c] = 1
                col = col_alive
            col = col if cur[r, c] == 1 else col_background
            pygame.draw.rect(surface, col, (c * sz, r * sz, sz - 1, sz - 1))

        return nxt


if __name__ == "__main__":
    game = GameOfLife(120, 90, 8, random=True)
    game.start()