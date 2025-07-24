class BridgeState:
    def __init__(self, side_status, crossing_times, total_time, lamp_position):
        self.side_status = side_status          # [0,0,0,0] means all people are on the left
        self.crossing_times = crossing_times    # Time taken by each person to cross
        self.total_time = total_time            # Time elapsed so far
        self.lamp_position = lamp_position      # 0 = left, 1 = right

    def is_goal_state(self):
        return self.side_status == [1, 1, 1, 1] and self.total_time <= 60

    def generate_successors(self):
        possible_moves = []
        for i in range(len(self.side_status)):
            for j in range(i, len(self.side_status)):
                if self.side_status[i] == self.side_status[j] == self.lamp_position:
                    new_state = self.side_status.copy()
                    if i == j:
                        new_state[i] = 1 - self.side_status[i]
                        new_time = self.total_time + self.crossing_times[i]
                    else:
                        new_state[i] = 1 - self.side_status[i]
                        new_state[j] = 1 - self.side_status[j]
                        new_time = self.total_time + max(self.crossing_times[i], self.crossing_times[j])

                    if new_time <= 60:
                        possible_moves.append(
                            BridgeState(new_state, self.crossing_times, new_time, 1 - self.lamp_position)
                        )
        return possible_moves

    def __eq__(self, other):
        return (
            isinstance(other, BridgeState)
            and self.side_status == other.side_status
            and self.lamp_position == other.lamp_position
            and self.total_time == other.total_time
        )

    def __hash__(self):
        return hash((tuple(self.side_status), self.lamp_position, self.total_time))

    def __repr__(self):
        position_str = ''.join(map(str, self.side_status))
        return f"BridgeState[{position_str}] | Time = {self.total_time}"


def reconstruct_path(explored_list, goal_node):
    path = []
    parent_map = {node: parent for node, parent in explored_list}
    while goal_node:
        path.append(goal_node)
        goal_node = parent_map.get(goal_node)
    return list(reversed(path))


def get_unvisited_nodes(expanded_nodes, frontier, visited):
    frontier_states = [node for node, _ in frontier]
    visited_states = [node for node, _ in visited]
    return [node for node in expanded_nodes if node not in frontier_states and node not in visited_states]


def breadth_first_search(start_node):
    frontier = [(start_node, None)]
    visited = []

    while frontier:
        current, parent = frontier.pop(0)
        visited.append((current, parent))

        if current.is_goal_state():
            print("BFS found a solution:")
            for step in reconstruct_path(visited, current):
                print(step)
            return

        next_states = get_unvisited_nodes(current.generate_successors(), frontier, visited)
        frontier.extend((state, current) for state in next_states)

    print("No BFS solution found within the time limit.")


def depth_first_search(start_node):
    frontier = [(start_node, None)]
    visited = []

    while frontier:
        current, parent = frontier.pop()
        visited.append((current, parent))

        if current.is_goal_state():
            print("DFS found a solution:")
            for step in reconstruct_path(visited, current):
                print(step)
            return

        next_states = get_unvisited_nodes(current.generate_successors(), frontier, visited)
        frontier.extend((state, current) for state in next_states)

    print("No DFS solution found within the time limit.")


def main():
    start_state = BridgeState([0, 0, 0, 0], [5, 10, 20, 25], 0, 0)
    print("Running BFS...")
    breadth_first_search(start_state)
    print("\nRunning DFS...")
    depth_first_search(start_state)


if __name__ == "__main__":
    main()
