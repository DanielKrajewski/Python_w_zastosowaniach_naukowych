import argparse
from rich.progress import track

import time
start_time = time.time()

import numpy as np
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description="ISING")
parser.add_argument('--net_size', '-n', type=int, default=20, help="Size of net  (default 20).", required = True)
parser.add_argument('--j_value', '-J', type=float, default=1, help="Value of J (default 1)", required = True)
parser.add_argument('--beta_value','-b', type=float, default=1, help="Value of Beta (default 1).", required = True)
parser.add_argument('--B_value','-B', type=float, default=1, help="Value of B (default 1).", required = True)
parser.add_argument('--steps','-s', type=int, default=100, help="Macro step (default 100).", required = True)
parser.add_argument('--density','-d', type=float, default=0.5, help="density (default 0.5).")
parser.add_argument('--image_prefix','-ip', type=str, default='./images/image', help="Image prefix path(default ./image).")
parser.add_argument('--animation_file','-af', type=str, default='animation.gif', help="animation name (default 'animation.gif).")
parser.add_argument('--magnetization_file','-mf', type=str, default='magnet.txt', help="magnet file(default 'magnet.txt).")


class Ising:
    def __init__(self, args):
        
        self.n = args.net_size
        self.J = args.j_value
        self.beta = args.beta_value
        self.B = args.B_value
        self.steps = args.steps
        self.spin_density = args.density
        self.image_prefix = args.image_prefix  
        self.animation_file = args.animation_file 
        self.magnetization_file = args.magnetization_file 

        self.grid = np.random.choice([-1, 1], size=(self.n, self.n), p=[1 - args.density, args.density])
        self.magnetization = []

    def delta_Eij(self, i, j):
        spin = self.grid[i, j]
        sum_neighbors = (
            self.grid[(i+1) % self.n, j] + self.grid[(i-1) % self.n, j] +
            self.grid[i, (j+1) % self.n] + self.grid[i, (j-1) % self.n]
        )
        dE = 2 * spin * (self.J * sum_neighbors + self.B)
        return dE

    def monte_carlo_step(self):
        for _ in range(self.n * self.n):
            i, j = np.random.randint(0, self.n, size=2)
            dE = self.delta_Eij(i, j)
            if dE < 0 or np.random.rand() < np.exp(-self.beta * dE):
                self.grid[i, j] *= -1

    def simulate(self):
            images = []
            for step in track(range(self.steps), description="Simulating"):
                self.monte_carlo_step()
                magnetization = np.sum(self.grid) / (self.n * self.n)
                self.magnetization.append(magnetization)

                if self.image_prefix:
                    image = Image.new('RGB', (self.n, self.n), 'red')
                    draw = ImageDraw.Draw(image)
                    for i in range(self.n):
                        for j in range(self.n):
                            color = (255, 255, 255) if self.grid[i, j] == 1 else (0, 0, 0)
                            draw.point((j, i), fill=color)
                    image = image.resize((self.n * 100, self.n * 100), Image.NEAREST)
                    image.save(f"{self.image_prefix}_{step}.png")
                    images.append(image)

            if self.animation_file:
                images[0].save(self.animation_file,save_all=True,append_images=images[1:],duration=100,loop=0)
            if self.magnetization_file:
                with open(self.magnetization_file, 'w') as f:
                    for step, m in enumerate(self.magnetization):
                        f.write(f"{step}\t{m}\n")



args = parser.parse_args()
ising = Ising(args)
ising.simulate()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Czas wykonania: {elapsed_time:.6f} sekund")


#poetry run python lab02.py -n 20 -J 2 -b 0.01 -B 1 -s 50
#poetry run python lab02.py -n 20 -J 2 -b 5 -B 1 -s 20