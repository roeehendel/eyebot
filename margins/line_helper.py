""" A mini-library for helping line-processing.
The assumed format of lines in this library, is as given by the
cv2.HoughLinesP function."""
import math
import numpy as np

def get_Xs_and_Ys(line):  # return x and y vals
    x1 = line[0][0]
    x2 = line[0][2]
    y1 = line[0][1]
    y2 = line[0][3]
    return x1, y1, x2, y2


def get_r_and_theta(line):
    a, b = get_A_and_B(line)
    theta = math.atan(a)
    r = abs(b) * math.cos(theta)

    return r, theta


def get_low_point_and_high_point(line):
    x1, y1, x2, y2 = get_Xs_and_Ys(line)

    if y2 > y1:
        return [x1, y1], [x2, y2]
    else:
        return [x2, y2], [x1, y1]


def get_A_and_B(line):  # return slope (a) and added constant (b)
    x1, y1, x2, y2 = get_Xs_and_Ys(line)
    if x2 - x1 == 0:
        x2 += 10 ** -8
    a = (float)(y2 - y1) / (float)(x2 - x1)
    b = y2 - a * x2
    return a, b


def points_on_line(line):
    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]

    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    line_equation = lambda x: np.array([x, a * x + b])

    return line_equation(np.arange(min(x1, x2) + 1, max(x1, x2)))


def A_B_from_r_theta(r, theta, sign):
    """
    doing what you think it does: moving from polar presentation of line,
    to cartesian representation.
    we're saved by the fact that python's math.cos and math.tan
     *cannot* return 0 or inf only very small/very large numbers
    :param r:
    :param theta:
    :return:
    """

    a = math.tan(theta)

    # todo: maybe it CAN crash??
    b = sign * r / math.cos(theta)

    return a, b


def get_line_center(line):
    x1, y1, x2, y2 = get_Xs_and_Ys(line)
    Xc = (x1 + x2) / 2
    Yc = (y1 + y2) / 2
    return (Xc, Yc)


def get_line_length(line):
    x1, y1, x2, y2 = get_Xs_and_Ys(line)
    return math.hypot(x1 - x2, y1 - y2)


def distance_between_line_centers(line1, line2):
    x1, y1 = get_line_center(line1)
    x2, y2 = get_line_center(line2)
    return math.hypot(x1 - x2, y1 - y2)


def distance_by_a_and_b(line1, line2):
    a1, b1 = get_A_and_B(line1)
    a2, b2 = get_A_and_B(line2)
    return math.hypot(a1 - a2, b1 - b2)


# given a rectangle and a line (a,b), return the two intersection points
# todo :maybe this causes problems due to roundings? can numbers get out of index?
def part_blocked_in_rect(a, b, x_min, y_min, x_max, y_max):
    y1, y2 = a * x_min + b, a * x_max + b

    # the list of all possible Ys. we nead only the middle 2
    Y = [y1, y2, y_max, y_min]

    Y.remove(max(Y))
    Y.remove(min(Y))

    # corresponding x values
    x0 = (Y[0] - b) / a
    x1 = (Y[1] - b) / a

    return [int(x0), int(Y[0]), int(x1), int(Y[1])]
