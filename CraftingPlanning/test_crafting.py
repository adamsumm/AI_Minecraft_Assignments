from crafting import recipes, plan_dijkstra, plan_width, State

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


def run_trial(alg, limit, start, goal):
    now = time.time()
    visited, cost, path = alg(start, goal, limit)
    done = time.time()
    print("DT:", done - now)
    return visited, cost, path, done - now


def expect_path(p1, cost, p2, explanation):
    print(explanation)
    register_point()
    if p1 == p2:
        earn_point("Paths equal, +1")
    else:
        start = p2[0]
        goal = p2[-1]
        if(p1[0] != start):
            miss_point("Wrong start state, +0")
            print("Got", p1[0], "expected", start)
            return
        if(p1[-1] != goal):
            miss_point("Wrong goal state, +0")
            print("Got", p1[-1], "expected", goal)
            return
        p1cost = 0
        p2cost = 0
        costs = {n: r.cost for n, r in recipes.items()}
        for pt in p1[1:]:
            p1cost += costs[pt]
        for pt in p2[1:]:
            p2cost += costs[pt]
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


print("Dijkstra make stone pickaxe")
visited, cost, path, dt = run_trial(plan_dijkstra, 300000, State.from_dict({}), State.from_dict({'stone_pickaxe': 1}))
expect_exactly(cost, 31, "Optimal plan cost")
expect_path(path, 31, ['punch for wood', 'craft plank', 'punch for wood', 'craft plank', 'punch for wood', 'craft plank', 'craft bench', 'craft stick', 'craft wooden_pickaxe at bench', 'wooden_pickaxe for cobble', 'wooden_pickaxe for cobble', 'wooden_pickaxe for cobble', 'craft stone_pickaxe at bench'], "Optimal path")
print("Dijkstra make ingot given bench, pickaxe")
visited, cost, path, dt = run_trial(plan_dijkstra, 100000, State.from_dict({'bench': 1, 'stone_pickaxe': 1}), State.from_dict({'ingot': 1}))
expect_exactly(cost, 28, "Optimal plan cost")
expect_path(path, 28, ['stone_pickaxe for cobble', 'stone_pickaxe for cobble', 'stone_pickaxe for cobble', 'stone_pickaxe for cobble', 'stone_pickaxe for cobble', 'stone_pickaxe for cobble', 'stone_pickaxe for cobble', 'stone_pickaxe for cobble', 'craft furnace at bench', 'stone_pickaxe for coal', 'stone_pickaxe for ore', 'smelt ore in furnace'], "Optimal path")

print("------------------------")
print("Widening make stone pickaxe")
visited, cost, path, dt = run_trial(plan_width,
                                    4,
                                    State.from_dict({}),
                                    State.from_dict({'stone_pickaxe': 1}))
expect_nearly(cost, 31, 0.1, "Path length")
print("Widening make ingot given bench")
visited, cost, path, dt = run_trial(plan_width,
                                    4,
                                    State.from_dict({'bench': 1}),
                                    State.from_dict({'ingot': 1}))

expect_exactly(cost, 55, "Path length")
print("Widening make iron pickaxe")
visited, cost, path, dt = run_trial(plan_width,
                                    4,
                                    State.from_dict({}),
                                    State.from_dict({'iron_pickaxe': 1}))
expect_nearly(cost, 89, 0.1, "Path length")
print("Widening make cart")
visited, cost, path, dt = run_trial(plan_width,
                                    4,
                                    State.from_dict({}),
                                    State.from_dict({'cart': 1}))
expect_nearly(cost, 114, 0.1, "Path length")

print("Widening make rail")
visited, cost, path, dt = run_trial(plan_width,
                                    4,
                                    State.from_dict({}),
                                    State.from_dict({'rail': 1}))
expect_nearly(cost, 128, 0.1, "Path length")
