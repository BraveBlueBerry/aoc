from common.navigation_utils import Position, Direction


# tentative costs
def determine_tentative_cost(path_score_up_to_now, current: Position, current_direction=None, neighbour_direction=None):
    return path_score_up_to_now[current] + 1

def tentative_score_expensive_corners(path_score_up_to_now, current: Position, current_direction: Direction, neighbour_direction: Direction):
    tentative_score = path_score_up_to_now[current] + 1
    if current_direction.get_symbol() != neighbour_direction.get_symbol():
        tentative_score += 1000
    return tentative_score


# heuristics
def manhattan_heuristic(end_position: Position, current: Position):
    goal = end_position
    return abs(current.x - goal.x) + abs(current.y - goal.y)