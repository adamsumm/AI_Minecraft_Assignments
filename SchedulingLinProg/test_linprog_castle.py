from linprog_castle import solve_castle_1, solve_castle_2

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


print("Solve castle_1 with varying parameters")

print("5,7256")
opt, model = solve_castle_1(5, 7256)
expect_exactly(opt, 14540, "Optimal cost")

print("10,7256")
opt, model = solve_castle_1(10, 7256)
expect_exactly(opt, 32680, "Optimal cost")

# TODO fixme wrong, plan must take at least three hours to make sense
print("1,20000")
opt, model = solve_castle_1(1, 20000)
expect_nearly(opt, 7866.667, 0.01, "Optimal cost")

print("Solve castle_2 with varying parameters")
opt, model = solve_castle_2(4000, 256, 3000)
expect_nearly(opt, 1014.8, 0.01, "Optimal duration")

opt, model = solve_castle_2(4000, 256, 1500)
expect_nearly(opt, 960, 0.01, "Optimal duration")


opt, model = solve_castle_2(4000, 128, 1500)
expect_nearly(opt, 952.6, 0.01, "Optimal duration")

print("Total score:", score[0], "/", score[1], "==", score[0] / score[1])
