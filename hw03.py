#############################################
#### Work for problem set 3 due on 10/24 ####
####             Simon Wright            ####
#############################################

from numpy import random
import numpy as np


def stat_unc(N, var):
    o = np.sqrt(var)
    return o/np.sqrt(N)


def mc1_square(tries):
    tries = int(tries)

    i = 0
    radius = 1
    dl = []

    while i < tries:
        # Choose random X and Y centered around 0,0
        x1 = random.uniform(0, radius)
        y1 = random.uniform(0, radius)
        x2 = random.uniform(0, radius)
        y2 = random.uniform(0, radius)

        d = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        dl.append(d)
        i += 1

    dl = np.array(dl)

    mean = sum(dl)/tries                       # Expected value
    #variance = sum((dl - mean)**2)/tries       # Variance
    variance = sum(dl**2)/tries - mean**2       # Variance
    unc = stat_unc(tries, variance)

    print("Square:")
    print(f"Expected Value: {mean} +/- {unc}")
    print(f"Variance: {variance}")

def mc1_cube(tries):
    tries = int(tries)

    i = 0
    radius = 1
    dl = []

    while i < tries:
        # Choose random X and Y centered around 0,0
        x1 = random.uniform(0, radius)
        y1 = random.uniform(0, radius)
        z1 = random.uniform(0, radius)
        x2 = random.uniform(0, radius)
        y2 = random.uniform(0, radius)
        z2 = random.uniform(0, radius)

        d = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

        dl.append(d)

        i += 1

    dl = np.array(dl)

    mean = sum(dl)/tries                       # Expected value
    variance = sum((dl - mean)**2)/tries       # Variance
    unc = stat_unc(tries, variance)

    print("Cube:")
    print(f"Expected Value: {mean} +/- {unc}")
    print(f"Variance: {variance}")


def mc1_circle(tries):
    tries = int(tries)

    i = 0
    radius = 1
    dl = []

    while i < tries:
        # Choose random X and Y centered around 0,0
        x1 = random.uniform(-radius, radius)
        y1 = random.uniform(-radius, radius)
        x2 = random.uniform(-radius, radius)
        y2 = random.uniform(-radius, radius)

        if (np.sqrt(x1**2 + y1**2) < radius and np.sqrt(x2**2 + y2**2) < radius):
            d = np.sqrt((x1-x2)**2 + (y1-y2)**2)
            dl.append(d)
            i += 1

    dl = np.array(dl)

    mean = sum(dl)/tries                       # Expected value
    variance = sum((dl - mean)**2)/tries       # Variance
    unc = stat_unc(tries, variance)

    print("Circle:")
    print(f"Expected Value: {mean} +/- {unc}")
    print(f"Variance: {variance}")


def mc1_sphere(tries):
    tries = int(tries)

    i = 0
    radius = 1
    dl = []

    while i < tries:
        # Choose random X and Y centered around 0,0
        x1 = random.uniform(-radius, radius)
        y1 = random.uniform(-radius, radius)
        z1 = random.uniform(-radius, radius)
        x2 = random.uniform(-radius, radius)
        y2 = random.uniform(-radius, radius)
        z2 = random.uniform(-radius, radius)

        if (np.sqrt(x1**2 + y1**2 + z1**2) < radius and np.sqrt(x2**2 + y2**2 + z2**2) < radius):
            d = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
            dl.append(d)
            i += 1

    dl = np.array(dl)

    mean = sum(dl)/tries                       # Expected value
    variance = sum((dl - mean)**2)/tries       # Variance
    unc = stat_unc(tries, variance)

    print("Sphere:")
    print(f"Expected Value: {mean} +/- {unc}")
    print(f"Variance: {variance}")


def I(x):
    return np.sqrt(1-x**2)


def mc2(tries, f, t1, t2):
    tries = int(tries)
    under_curve = 0
    i = 0

    y1 = f(t1)
    y2 = f(t2)

    while i < tries:
        x = random.uniform(t1, t2)
        y = random.uniform(f(t1), f(t2))
        # If the point is inside circle, increase variable
        if y < f(x):
            under_curve += 1
        i += 1

    # Calculate area and print; should be closer to Pi with increasing number of throws
    area = abs((t2 - t1) * (y2 - y1))
    area_under_curve = area * (under_curve / tries)

    unc = area_under_curve / np.sqrt(tries)

    print(f"Integral: {area_under_curve} +/- {unc}")


def conditions():

    out = []
    electoral = np.array([15, 10, 6, 19, 16, 16, 11])

    for i in range(1 << 7):
        s = bin(i)[2:]
        s = '0' * (7 - len(s)) + s
        out.append(list(map(int, list(s))))

    d_win = 0
    r_win = 0
    t_win = 0
    for i in out:
        d = 226 + sum(electoral * np.array(i))
        if d > 269:
            d_win += 1
        elif d == 269:
            t_win += 1
        else:
            r_win +=1

    print(d_win, r_win, t_win)


def vote(n, offset=0, new_odds=None):

    n = int(n)
    MI = WI = NV = PA = NC = GA = AZ = np.zeros(n)
    states = [MI, WI, NV, PA, NC, GA, AZ]
    if new_odds is None:
        odds = [3, 2, 1, 0, -1, -2, -3]
    else:
        odds = new_odds
    stdev = [2, 2, 2, 2, 2, 2, 2]
    electoral = [15, 10, 6, 19, 16, 16, 11]
    vote_outcomes = np.zeros(n)

    for i in range(n):
        for state, odd, std, elec in zip(states, odds, stdev, electoral):
            state_vote = random.normal(odd+offset, std)
            vote_outcomes[i] += int(np.sign(state_vote) * elec)

    d_win = 0
    r_win = 0
    t_win = 0
    for i in range(n):
        balance = 7
        balance += vote_outcomes[i]
        if balance > 0:
            d_win += 1
        elif balance < 0:
            r_win += 1
        else:
            t_win += 1

    print('D Win: {0:.2f}'.format(d_win/n*100) + '%, R Win: {0:.2f}'.format(r_win/n*100) + '%, Tie: {0:.2f}'.format(t_win/n*100) + "%")


def problem_1():
    mc1_square(1000000)
    mc1_circle(1000000)
    mc1_cube(1000000)
    mc1_sphere(1000000)


def problem_2():
    mc2(1e6, I, 0, 1)


def problem_5():
    print("With current odds:")
    vote(1e6)
    print("With D +2:")
    vote(1e6, offset=2)
    print("With R +2:")
    vote(1e6, offset=-2)
    print("With all states as tossup:")
    vote(1e6, new_odds=[0, 0, 0, 0, 0, 0, 0])


def main():
    problem_1()
    problem_2()
    problem_5()


if __name__ == '__main__':
    main()

