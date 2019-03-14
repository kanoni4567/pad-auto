from lib.classifier import classify_orbs, get_canvas_position
from lib.screen import get_screenshot
from lib.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from heuristics.pruned_bfs import PrunedBfs
from heuristics.greedy_dfs import GreedyDfs
from lib.scriptwriter import write_path_script
import subprocess
import time


def solve_board(depth=25):
    screen = get_screenshot()
    board = classify_orbs(screen)
    print(board)

    weights = {Fire.symbol: 1.0,
               Wood.symbol: 1.0,
               Water.symbol: 1.0,
               Dark.symbol: 1.0,
               Light.symbol: 1.0,
               Heart.symbol: 1.0,
               Poison.symbol: 0.5,
               Jammer.symbol: 0.5,
               Unknown.symbol: 0.0}

    # try PrunedBfs heuristic
    solver = PrunedBfs(weights)
    solution = solver.solve(board, depth)

    return solution


if __name__ == "__main__":
    try:
        subprocess.call("adb connect 127.0.0.1:62001", shell=True)
    except:
        pass

    while True:
        try:
            solution = solve_board(40)
            print(solution[1])
            print(solution[2])
            write_path_script(solution[1])
            command = r"monkeyrunner C:\Users\cuish\Documents\PersonalProjects\pad-auto\script\script.py"
            subprocess.call(command, shell=True)
            time.sleep(5)
        except:
            pass
