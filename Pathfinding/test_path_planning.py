from path_planning import load_map, breadth_first, dijkstra, best_first, astar
import time

score = [0, 0]
point_status = False

# Thanks to https://stackoverflow.com/a/287944


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def register_point():
    global point_status
    if point_status:
        print(bcolors.WARNING + "Possible grader bug: No point added or missed on last question" + bcolors.ENDC)
    score[1] += 1
    point_status = True


def earn_point(explanation):
    global point_status
    if not point_status:
        print(bcolors.WARNING + "Possible grader bug: No point registered for this question" + bcolors.ENDC)
    print(bcolors.OKGREEN + explanation + bcolors.ENDC)
    score[0] += 1
    point_status = False


def miss_point(explanation):
    global point_status
    if not point_status:
        print(bcolors.WARNING + "Possible grader bug: No point registered for this question" + bcolors.ENDC)
    print(bcolors.FAIL + explanation + bcolors.ENDC)
    point_status = False


def run_trial(m, alg, start, goal):
    now = time.time()
    visited, cost, path = alg(m, start, goal)
    done = time.time()
    print("DT:", done - now)
    return visited, cost, path, done - now


def expect_path(p1, terrain, cost, start, goal, p2, explanation):
    print(explanation)
    register_point()
    if p1 == p2:
        earn_point("Paths equal, +1")
    else:
        if(p1[0] != start):
            miss_point("Wrong start point, +0")
            print("Got", p1[0], "expected", start)
            return
        if(p1[-1] != goal):
            miss_point("Wrong goal point, +0")
            print("Got", p1[-1], "expected", goal)
            return
        p1cost = 0
        p2cost = 0
        costs = {
            "🌿": 1,
            "🌉": 1,
            "🌲": 1,
            "🌼": 2,
            "🌊": 5
        }
        for pt in p1[1:]:
            p1cost += costs[terrain[pt[1]][pt[0]]]
        for pt in p2[1:]:
            p2cost += costs[terrain[pt[1]][pt[0]]]
        assert cost == p2cost
        if p1cost == cost:
            earn_point("Paths different but costs the same, +1")
            return
        miss_point("Paths different, +0:")
        print("Got", p1, "Cost", p1cost)
        print("Expected", p2, "Cost", cost)


def expect_exactly(v1, v2, explanation):
    print(explanation)
    register_point()
    if v1 == v2:
        earn_point("Values equal, +1")
    else:
        miss_point("Values different, +0")
        print("Got", v1, "Expected", v2)


def expect_nearly(v1, v2, fraction, explanation):
    print(explanation)
    register_point()
    if v1 == v2:
        earn_point("Values equal, +1")
    elif abs(v1 - v2) <= fraction * v2:
        earn_point("Values roughly equal, +1")
        print("Got", v1, "Expected", v2, "Delta:", abs(v1 - v2), "max tolerance", fraction * v2)
    else:
        miss_point("Values different, +0")
        print("Got", v1, "Expected", v2, "Acceptable delta:", fraction * v2)


t = load_map('terrain.txt')

print("BFS (0,0) -> (10,0)")
visited, cost, path, dt = run_trial(t, breadth_first, (0, 0), (10, 0))
expect_exactly(cost, 13, "Optimal path cost")
expect_path(path, t, 13, (0, 0), (10, 0), [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0)], "Optimal path")
p1_bfs_cost = cost
p1_bfs_visited = visited
print("BFS (2,3) -> (7,0)")
visited, cost, path, dt = run_trial(t, breadth_first, (2, 3), (7, 0))
expect_exactly(cost, 10, "Optimal path cost")
expect_path(path, t, 10, (2, 3), (7, 0), [(2, 3), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 1), (6, 0), (7, 0)], "Optimal path")
p2_bfs_cost = cost
p2_bfs_visited = visited
print("BFS (5,5) -> (0,1)")
visited, cost, path, dt = run_trial(t, breadth_first, (5, 5), (0, 1))
expect_exactly(cost, 17, "Optimal path cost")
expect_path(path, t, 17, (5, 5), (0, 1), [(5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 1)], "Optimal path")
p3_bfs_cost = cost
p3_bfs_visited = visited
print("BFS (0,0) -> (10,9)")
visited, cost, path, dt = run_trial(t, breadth_first, (0, 0), (10, 9))
expect_exactly(cost, 21, "Optimal path cost")
expect_path(path, t, 21, (0, 0), (10, 9), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 9), (10, 9)], "Optimal path")
p4_bfs_cost = cost
p4_bfs_visited = visited

print("BFS (0,0) -> (0,9)")
visited, cost, path, dt = run_trial(t, breadth_first, (0, 0), (0, 9))
expect_exactly(cost, 26, "Optimal path cost")
expect_path(path, t, 26, (0, 0), (0, 9), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9), (0, 9)], "Optimal path")
p5_bfs_cost = cost
p5_bfs_visited = visited

print("BFS (0,0) -> (11,10) (should find no path)")
visited, cost, path, dt = run_trial(t, breadth_first, (0, 0), (11, 10))
expect_exactly(path, None, "No path")
p6_bfs_cost = cost
p6_bfs_visited = visited

print("------------------------")

print("Dijkstra (0,0) -> (10,0)")
visited, cost, path, dt = run_trial(t, dijkstra, (0, 0), (10, 0))
expect_exactly(cost, 13, "Optimal path cost")
expect_path(path, t, 13, (0, 10), (10, 0), [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0)], "Optimal path")
p1_dijkstra_cost = cost
p1_dijkstra_visited = visited
print("Dijkstra (2,3) -> (7,0)")
visited, cost, path, dt = run_trial(t, dijkstra, (2, 3), (7, 0))
expect_exactly(cost, 10, "Optimal path cost")
expect_path(path, t, 10, (2, 3), (7, 0), [(2, 3), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], "Optimal path")
p2_dijkstra_cost = cost
p2_dijkstra_visited = visited
print("Dijkstra (5,5) -> (0,1)")
visited, cost, path, dt = run_trial(t, dijkstra, (5, 5), (0, 1))
expect_exactly(cost, 17, "Optimal path cost")
expect_path(path, t, 17, (5, 5), (0, 1), [(5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 1)], "Optimal path")
p3_dijkstra_cost = cost
p3_dijkstra_visited = visited
print("Dijkstra (0,0) -> (10,9)")
visited, cost, path, dt = run_trial(t, dijkstra, (0, 0), (10, 9))
expect_exactly(cost, 21, "Optimal path cost")
expect_path(path, t, 21, (0, 0), (10, 9), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 9), (10, 9)], "Optimal path")
p4_dijkstra_cost = cost
p4_dijkstra_visited = visited
print("Dijkstra (0,0) -> (0,9)")
visited, cost, path, dt = run_trial(t, dijkstra, (0, 0), (0, 9))
expect_exactly(cost, 26, "Optimal path cost")
expect_path(path, t, 26, (0, 0), (0, 9), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9), (0, 9)], "Optimal path")
p5_dijkstra_cost = cost
p5_dijkstra_visited = visited
print("Dijkstra (0,0) -> (11,10) (should find no path)")
visited, cost, path, dt = run_trial(t, dijkstra, (0, 0), (11, 10))
expect_exactly(path, None, "No path")
p6_dijkstra_cost = cost
p6_dijkstra_visited = visited

print("------------------------")

print("Best_First (0,0) -> (10,0)")
visited, cost, path, dt = run_trial(t, best_first, (0, 0), (10, 0))
expect_exactly(cost, 13, "Optimal path cost...?")
expect_path(path, t, 13, (0, 0), (10, 0), [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0)], "Optimal path...?")
p1_best_first_cost = cost
p1_best_first_visited = visited
print("Best_First (2,3) -> (7,0)")
visited, cost, path, dt = run_trial(t, best_first, (2, 3), (7, 0))
expect_exactly(cost, 10, "Optimal path cost...?")
expect_path(path, t, 10, (2, 3), (7, 0), [(2, 3), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], "Optimal path...?")
p2_best_first_cost = cost
p2_best_first_visited = visited
print("Best_First (5,5) -> (0,1)")
visited, cost, path, dt = run_trial(t, best_first, (5, 5), (0, 1))
expect_exactly(cost, 33, "Optimal path cost...?")
expect_path(path, t, 33, (5, 5), (0, 1), [(5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1)], "Optimal path...?")
p3_best_first_cost = cost
p3_best_first_visited = visited
print("Best_First (0,0) -> (10,9)")
visited, cost, path, dt = run_trial(t, best_first, (0, 0), (10, 9))
expect_exactly(cost, 40, "Optimal path cost...?")
expect_path(path, t, 40, (0, 0), (10, 9), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9)], "Optimal path...?")
p4_best_first_cost = cost
p4_best_first_visited = visited
print("Best_First (0,0) -> (0,9)")
visited, cost, path, dt = run_trial(t, best_first, (0, 0), (0, 9))
expect_exactly(cost, 29, "Optimal path cost...?")
expect_path(path, t, 29, (0, 0), (0, 9), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)], "Optimal path...?")
p5_best_first_cost = cost
p5_best_first_visited = visited
print("Best_First (0,0) -> (11,10) (should find no path)")
visited, cost, path, dt = run_trial(t, best_first, (0, 0), (11, 10))
expect_exactly(path, None, "No path")
p6_best_first_cost = cost
p6_best_first_visited = visited

print("------------------------")

print("Astar (0,0) -> (10,0)")
visited, cost, path, dt = run_trial(t, astar, (0, 0), (10, 0))
expect_exactly(cost, 13, "Optimal path cost")
expect_path(path, t, 13, (0, 0), (10, 0), [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0)], "Optimal path")
p1_astar_cost = cost
p1_astar_visited = visited
print("Astar (2,3) -> (7,0)")
visited, cost, path, dt = run_trial(t, astar, (2, 3), (7, 0))
expect_exactly(cost, 10, "Optimal path cost")
expect_path(path, t, 10, (2, 3), (7, 0),  [(2, 3), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], "Optimal path")
p2_astar_cost = cost
p2_astar_visited = visited
print("Astar (5,5) -> (0,1)")
visited, cost, path, dt = run_trial(t, astar, (5, 5), (0, 1))
expect_exactly(cost, 17, "Optimal path cost")
expect_path(path, t, 17, (5, 5), (0, 1), [(5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 1)], "Optimal path")
p3_astar_cost = cost
p3_astar_visited = visited
print("Astar (0,0) -> (10,9)")
visited, cost, path, dt = run_trial(t, astar, (0, 0), (10, 9))
expect_exactly(cost, 21, "Optimal path cost")
expect_path(path, t, 21, (0, 0), (10, 9), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 9), (10, 9)], "Optimal path")
p4_astar_cost = cost
p4_astar_visited = visited
print("Astar (0,0) -> (0,9)")
visited, cost, path, dt = run_trial(t, astar, (0, 0), (0, 9))
expect_exactly(cost, 26, "Optimal path cost")
expect_path(path, t, 26, (0, 0), (0, 9), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9), (0, 9)], "Optimal path")
p5_astar_cost = cost
p5_astar_visited = visited
print("Astar (0,0) -> (11,10) (should find no path)")
visited, cost, path, dt = run_trial(t, astar, (0, 0), (11, 10))
expect_exactly(path, None, "No path")
p6_astar_cost = cost
p6_astar_visited = visited

print("Total score:", score[0], "/", score[1], "==", score[0] / score[1])
