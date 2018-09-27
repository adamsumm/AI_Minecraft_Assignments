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


def expect_model(m1, m2, fraction, explanation):
    print(explanation)
    register_point()
    good = True
    for k2, v2 in m2.items():
        assert k2 in m1
        v1 = m1[k2]
        if abs(v1 - v2) > fraction * v2:
            print("Got", m1, "=", v1, "Expected", v2, "Acceptable delta:", fraction * v2)
            good = False
            break
    if good:
        earn_point("Values equal, +1")
    else:
        miss_point("Values not equal, +0")


print("Solve castle_1 with varying parameters")

print("5,7256")
opt, model = solve_castle_1(5, 7256)
expect_exactly(opt, 14540, "Optimal cost")
# expect_model(model, {
#     "a": 10940,
#     "b": 10800,
#     "c": 14540
# }, 0.01, "Decision variable values")

print("10,7256")
opt, model = solve_castle_1(10, 7256)
expect_exactly(opt, 32680, "Optimal cost")
# expect_model(model, {
#     "a": 29080,
#     "b": 10800,
#     "c": 32680
# }, 0.01, "Decision variable values")

# TODO fixme wrong, plan must take at least three hours to make sense
# print("1,20000")
# opt, model = solve_castle_1(1, 20000)
# expect_nearly(opt, 7866.667, 0.01, "Optimal cost")
# expect_model(model, {
# "a": 4266.6,
# "b": 7866.6,
# "c": 7866.6
# }, 0.01, "Decision variable values")

print("Solve castle_2 with varying parameters")
opt, model = solve_castle_2(4000, 256, 3000)
expect_nearly(opt, 1014.8, 0.01, "Optimal duration")
# expect_model(model, {'a_dig': 709.93333, 'a_pane': 0.0, 'a_plank': 0.0, 'a_sand': 0.0, 'a': 1014.8, 'a_wood': 304.86667, 'b_dig': 1014.8, 'b_pane': 0.0, 'b_plank': 0.0, 'b_sand': 0.0, 'b': 1014.8, 'b_wood': 0.0, 'c_dig': 0.0, 'c_pane': 16.0, 'c_plank': 750.0, 'c_sand': 38.4, 'c': 1014.8, 'c_wood': 210.4, 'duration': 1014.8}, 0.1, "Optimal allocation")

opt, model = solve_castle_2(4000, 256, 1500)
expect_nearly(opt, 960, 0.01, "Optimal duration")
# expect_model(model, {'a_dig': 920.0, 'a_pane': 16.0, 'a_plank': 6.6428571, 'a_sand': 17.357143, 'a_t': 960.0, 'a_wood': 0.0, 'b_dig': 960.0, 'b_pane': 0.0, 'b_plank': 0.0, 'b_sand': 0.0, 'b_t': 960.0, 'b_wood': 0.0, 'c_dig': 0.0, 'c_pane': 0.0, 'c_plank': 368.35714, 'c_sand': 29.142857, 'c_t': 960.0, 'c_wood': 562.5, 'duration': 960.0}, 0.1, "Optimal allocation")


opt, model = solve_castle_2(4000, 128, 1500)
expect_nearly(opt, 952.6, 0.01, "Optimal duration")
# expect_model(model, {'a_dig': 948.51505, 'a_pane': 0.0, 'a_plank': 0.0, 'a_sand': 0.0, 'a_t': 952.56129, 'a_wood': 4.0462366, 'b_dig': 952.56129, 'b_pane': 0.0, 'b_plank': 0.0, 'b_sand': 0.0, 'b_t': 952.56129, 'b_wood': 0.0, 'c_dig': 0.0, 'c_pane': 8.0, 'c_plank': 375.0, 'c_sand': 19.2, 'c_t': 952.56129, 'c_wood': 550.36129, 'duration': 952.56129}, 0.1, "Optimal allocation")
