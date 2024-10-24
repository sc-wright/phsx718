#############################################
#### Work for problem set 3 due on 10/24 ####
####             Simon Wright            ####
#############################################


from numpy import random
import numpy as np


def stat_unc(N, var):
    # Uncertainty simplifies to sqrt(variance/N)
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

        # Calculate the distance between the two points using the distance formula
        d = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        # Keep track of all the distances
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

        # Reject the selection if it is outside the circle.
        # This isn't very optimized but it works and does not bias the sample.
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
    # f is the function to be estimated with the MC method. In this problem, it is the function I() defined above.
    # t1 and t2 are the x-bounds.
    tries = int(tries)
    under_curve = 0
    i = 0

    y1 = f(t1)
    y2 = f(t2)

    while i < tries:
        # Generate values within the box with corners xmin, xmax, ymin, ymax.
        x = random.uniform(t1, t2)
        y = random.uniform(y1, y2)
        # If the point is under curve, increase counter. Otherwise do nothing.
        if y < f(x):
            under_curve += 1
        i += 1

    # Caclulate the total area of the box
    area = abs((t2 - t1) * (y2 - y1))
    # Multiply the area by the fraction of points that was under the curve
    area_under_curve = area * (under_curve / tries)

    # The uncertainty simplifies to the value divided by sqrt(N)
    unc = area_under_curve / np.sqrt(tries)

    print(f"Integral: {area_under_curve} +/- {unc}")


def conditions():
    # This function generates all 128 possible combinations of outcomes
    out = []
    electoral = np.array([15, 10, 6, 19, 16, 16, 11])

    # Generate all possible boolean arrays where 1 is a d win and 0 is an r win
    for i in range(1 << 7):
        s = bin(i)[2:]
        s = '0' * (7 - len(s)) + s
        out.append(list(map(int, list(s))))

    d_win = 0
    r_win = 0
    t_win = 0
    for i in out:
        # Just multiply each boolean array by the array of electoral college votes then add them up
        d = 226 + sum(electoral * np.array(i))
        if d > 269:
            d_win += 1
        elif d == 269:
            t_win += 1
        else:
            r_win +=1

    print(d_win, r_win, t_win)


def vote(n, offset=0, new_odds=None):
    # This function generates n possible election results using a defined set of odds for the swing states.
    # The offset can be optionally added to swing the distribution toward D (positive offset) or R (negative offset)
    # The new odds can define an entirely new array of initial odds to replace the one in the problem
    n = int(n)

    # Define a few useful arrays and variables
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
        # For each simulated election
        for state, odd, std, elec in zip(states, odds, stdev, electoral):
            # In each state, generate a random outcome based on the previously defined parameters for the gaussians
            # centered on zero to make it easier to tell the outcome - positive for d win, negative for r win.
            state_vote = random.normal(odd+offset, std)
            # Multiply the electoral votes by +1 or -1 depending on who won
            # This could be skipped and added to the balance right away,
            # this step simply retains the individual state results in case we want to look at them later
            vote_outcomes[i] += int(np.sign(state_vote) * elec)

    d_win = 0
    r_win = 0
    t_win = 0
    for i in range(n):
        # The dems are currently ahead by 7 votes, so balance starts at +7
        balance = 7
        # Then add the electoral votes from each mock election and add one to the d win or r win tally
        # based on whether the outcome was above or below zero respectively.
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
    conditions()
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

