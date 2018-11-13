from intprog_crafting import solve_intprog, solve_intprog_compact

import time

score = [0, 0]
point_status = False


class bcolors:
    # Thanks to https://stackoverflow.com/a/287944
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


print("Solve planning with intprog")

print("{bench}->{stone_pickaxe}")
opt, model = solve_intprog({'bench': 1}, {'stone_pickaxe': 1}, 10)
expect_exactly(opt, 25, "Optimal cost...?")

print("{bench}->{stone_pickaxe}")
opt, model = solve_intprog({'bench': 1}, {'stone_pickaxe': 1}, 15)
expect_exactly(opt, 31, "Optimal cost...?")

print("{}->{stone_pickaxe}, t=13")
opt, model = solve_intprog({}, {'stone_pickaxe': 1}, 13)
expect_exactly(opt, 31, "Optimal cost...?")


print("{}->{stone_pickaxe}, t=15")
opt, model = solve_intprog({}, {'stone_pickaxe': 1}, 15)
expect_exactly(opt, 34, "Optimal cost...?")


print("Solve planning with intprog (compact encoding)")

print("{}->{stone_pickaxe}")
opt, model = solve_intprog_compact({}, {'stone_pickaxe': 1}, 10)
expect_exactly(opt, 31, "Optimal cost")


opt, model = solve_intprog_compact({}, {'stone_pickaxe': 100}, 10)
expect_exactly(opt, 837, "Optimal cost")


opt, model = solve_intprog_compact({}, {'rail': 1, 'cart': 1}, 10)
expect_exactly(opt, 172, "Optimal cost")

print("Total score:", score[0], "/", score[1], "==", score[0] / score[1])
