import argparse
import numpy as np
from PIL import Image, ImageDraw
from rich.progress import track
from numba import njit
import time

parser = argparse.ArgumentParser(description="ISING")
parser.add_argument('--net_size', '-n', type=int, default=20, help="Size of net (default 20).", required=True)
parser.add_argument('--j_value', '-J', type=float, default=1, help="Value of J (default 1)", required=True)
parser.add_argument('--beta_value', '-b', type=float, default=1, help="Value of Beta (default 1).", required=True)
parser.add_argument('--B_value', '-B', type=float, default=1, help="Value of B (default 1).", required=True)
parser.add_argument('--steps', '-s', type=int, default=100, help="Macro step (default 100).", required=True)
parser.add_argument('--density', '-d', type=float, default=0.5, help="Density (default 0.5).")
parser.add_argument('--image_prefix', '-ip', type=str, default='./images/image', help="Image prefix path (default ./image).")
parser.add_argument('--animation_file', '-af', type=str, default='animation.gif', help="Animation name (default 'animation.gif').")
parser.add_argument('--magnetization_file', '-mf', type=str, default='magnet.txt', help="Magnet file (default 'magnet.txt').")


@njit
def delta_Eij(grid, i, j, J, B, n):
    spin = grid[i, j]
    sum_neighbors = (
        grid[(i + 1) % n, j] + grid[(i - 1) % n, j] +
        grid[i, (j + 1) % n] + grid[i, (j - 1) % n]
    )
    dE = 2 * spin * (J * sum_neighbors + B)
    return dE

@njit
def monte_carlo_step(grid, beta, J, B, n):
    for _ in range(n * n):
        i, j = np.random.randint(0, n), np.random.randint(0, n)
        dE = delta_Eij(grid, i, j, J, B, n)
        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            grid[i, j] *= -1

@njit(parallel=True)
def calculate_magnetization(grid):
    return np.sum(grid) / grid.size

def simulate(args):
    n = args.net_size
    J = args.j_value
    beta = args.beta_value
    B = args.B_value
    steps = args.steps
    density = args.density

    grid = np.random.choice([-1, 1], size=(n, n), p=[1 - density, density])
    magnetization = []

    images = []
    for step in track(range(steps), description="Simulating"):
        monte_carlo_step(grid, beta, J, B, n)

        m = calculate_magnetization(grid)
        magnetization.append(m)

        if args.image_prefix:
            image = Image.new('RGB', (n, n), 'red')
            draw = ImageDraw.Draw(image)
            for i in range(n):
                for j in range(n):
                    color = (255, 255, 255) if grid[i, j] == 1 else (0, 0, 0)
                    draw.point((j, i), fill=color)
            image = image.resize((n * 100, n * 100), Image.NEAREST)
            image.save(f"{args.image_prefix}_{step}.png")
            images.append(image)

    #if args.animation_file and images:
        #images[0].save(args.animation_file,save_all=True,append_images=images[1:],duration=100,loop=0)

    if args.magnetization_file:
        with open(args.magnetization_file, 'w') as f:
            for step, m in enumerate(magnetization):
                f.write(f"{step}\t{m}\n")

args = parser.parse_args()
start_time = time.time()

simulate(args)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Czas wykonania: {elapsed_time:.6f} sekund")


#bez numby poetry run python lab02.py -n 100 -J 2 -b 0.01 -B 1 -s 100 trwało 170 sekund
#teraz z numbą trwa 134 sekundy

#poetry run python lab02.py -n 20 -J 2 -b 0.01 -B 1 -s 100 trwało 7.66 sekund
#z 7.7 sekundy