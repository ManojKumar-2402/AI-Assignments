from collections import deque

def is_goal(state):
    return state == "EEE_WWW"

def generate_moves(state):
    next_states = []
    tiles = list(state)
    empty_idx = state.index('_')

    # Slide East to the left
    if empty_idx < 6 and tiles[empty_idx + 1] == 'E':
        new_tiles = tiles[:]
        new_tiles[empty_idx], new_tiles[empty_idx + 1] = new_tiles[empty_idx + 1], new_tiles[empty_idx]
        next_states.append("".join(new_tiles))

    # Jump East over West
    if empty_idx < 5 and tiles[empty_idx + 2] == 'E' and tiles[empty_idx + 1] == 'W':
        new_tiles = tiles[:]
        new_tiles[empty_idx], new_tiles[empty_idx + 2] = new_tiles[empty_idx + 2], new_tiles[empty_idx]
        next_states.append("".join(new_tiles))

    # Slide West to the right
    if empty_idx > 0 and tiles[empty_idx - 1] == 'W':
        new_tiles = tiles[:]
        new_tiles[empty_idx], new_tiles[empty_idx - 1] = new_tiles[empty_idx - 1], new_tiles[empty_idx]
        next_states.append("".join(new_tiles))

    # Jump West over East
    if empty_idx > 1 and tiles[empty_idx - 2] == 'W' and tiles[empty_idx - 1] == 'E':
        new_tiles = tiles[:]
        new_tiles[empty_idx], new_tiles[empty_idx - 2] = new_tiles[empty_idx - 2], new_tiles[empty_idx]
        next_states.append("".join(new_tiles))

    return next_states


def solve_with_bfs(initial_state):
    visited = set()
    queue = deque([[initial_state]])

    while queue:
        path = queue.popleft()
        current = path[-1]

        if is_goal(current):
            return path

        for neighbor in generate_moves(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return []


def solve_with_dfs(initial_state):
    visited = set()
    stack = [[initial_state]]

    while stack:
        path = stack.pop()
        current = path[-1]

        if is_goal(current):
            return path

        for neighbor in generate_moves(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(path + [neighbor])

    return []


def main():
    initial = "WWW_EEE"
    print("BFS Path:")
    bfs_result = solve_with_bfs(initial)
    if bfs_result:
        for step in bfs_result:
            print(step)
    else:
        print("No BFS solution")

    print("\nDFS Path:")
    dfs_result = solve_with_dfs(initial)
    if dfs_result:
        for step in dfs_result:
            print(step)
    else:
        print("No DFS solution")


if __name__ == "__main__":
    main()
