from pazudorasolver.board import Board
from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudorasolver.heuristics.greedy_dfs import GreedyDfs
from pazudorasolver.heuristics.pruned_bfs import PrunedBfs

weights = {Fire.symbol: 1.0,
           Wood.symbol: 1.0,
           Water.symbol: 1.0,
           Dark.symbol: 1.0,
           Light.symbol: 1.0,
           Heart.symbol: 1.0,
           Poison.symbol: 0.5,
           Jammer.symbol: 0.5,
           Unknown.symbol: 0.0}

board = Board.create_randomized_board(5, 6)
matches = board.get_matches()

print(board)
print(matches)

# try GreedyDfs heuristic
solver1 = GreedyDfs(weights)
solution = solver1.solve(board, 50)

print(solution)

# try PrunedBfs heuristic
solver2 = PrunedBfs(weights)
solution = solver2.solve(board, 50)

print(solution)