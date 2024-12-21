def bfs(get_neighbours, start, goal):
    to_visit = set()
    visited = []
    to_visit.add(start)
    visited.append(start)
    while to_visit:
        current = to_visit.pop()
        if current == goal:
            return current

        for neighbour in get_neighbours(current):
            if neighbour not in visited:
                visited.append(neighbour)
                to_visit.add(neighbour)


