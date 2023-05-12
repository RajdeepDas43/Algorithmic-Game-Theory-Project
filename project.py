from numpy.random import choice
import math
import numpy as np
from copy import deepcopy
from collections import deque
import datetime
debug = 0

class CsvWriter:
    def __init__(self, delta, k, rounds, lower, upper):
        self.file = f"d={delta};k={k};lower={lower};upper={upper};date={datetime.datetime.now()}"

    def write(self, n, ratio):
        ratio = "0," + str(ratio)[2:]
        with open(self.file, "a") as f:
            f.write(f"{n};{ratio}\n")

def get_preferences(n: int, k: int, delta=2):

    start = -delta
    end = delta

    xs = np.linspace(start, end, n)

    nums = np.exp(-xs)
    probabilities = nums / nums.sum()

    p = {i: prob for i, prob in enumerate(probabilities)}

    preferences = []
    choices = [i for i in range(n)]
    p = list(p.values())
    for _ in range(n):
        preferences.append(list(choice(choices, replace=False, p=p, size=k)))
    prefs1 = preferences

    all_choices = []
    for recipient in range(n):
        choices = set()
        for proposer, prefs in enumerate(preferences):
            if recipient in prefs:
                choices.add(proposer)
        all_choices.append(choices)
    new_preferences = []
    for recipient, choices in enumerate(all_choices):
        prob = np.array([p[choice] for choice in choices])
        prob = prob / prob.sum()
        if len(choices) > 0:
            new_preferences.append(
                list(choice(list(choices), replace=False, p=prob, size=len(choices)))
            )
        else:
            new_preferences.append([])
    prefs2 = new_preferences

    pref_dict1 = {agent: list(prefs) for agent, prefs in enumerate(prefs1)}
    pref_dict2 = {agent: list(prefs) for agent, prefs in enumerate(prefs2)}

    return pref_dict1, pref_dict2

def deferred_acceptance(male_prefs, female_prefs):
    """
    Simple python implementation of Gale-Shapley (1962) algorithm

    This algorithm allows for agents to have variable length in
    their preference orderings and also does not require a match
    between agents' preferences on either side of the market
    """

    # copy to avoid destrcuction
    male_prefs_copy = deepcopy(male_prefs)

    # Use deque instead of list for male_prefs_copy for faster pop
    # but keep list for female_prefs since we perfoem lookups
    for k, v in male_prefs_copy.items():
        male_prefs_copy[k] = deque(v)

    # Initialize all male and female to free
    male_matches, female_matches = {}, {}

    # while ∃ unmatched male who still has a female to propose to
    while True:
        unmatched_males = [
            male for male in male_prefs_copy.keys() if male not in male_matches
        ]

        if debug == 1:
            print("Unmatched_males: ", unmatched_males)

        if unmatched_males == []:
            break
        
        for male in unmatched_males:
            if not male_prefs_copy[male]:
                male_matches[male] = "NA"
                break
            female = male_prefs_copy[male].popleft()

            prev_male = female_matches.get(female, None)
            prev_male_index = (
                female_prefs[female].index(prev_male) if prev_male else None
            )
            this_male_index = (
                female_prefs[female].index(male)
                if male in female_prefs[female]
                else None
            )

            if this_male_index == None:
                if debug == 1:
                    print("rejected. reciepient prefer unmatched")
            elif prev_male_index == None:
                male_matches[male] = female
                female_matches[female] = male

                if debug == 1:
                    print("new match")
            elif prev_male_index > this_male_index:
                male_matches[male] = female
                female_matches[female] = male
                del male_matches[prev_male]

                if debug == 1:
                    print("updated match")
            else:
                if debug == 1:
                    print("rejected. reciepient prefer current")

    for female in female_prefs.keys():
        if female not in female_matches:
            female_matches[female] = "NA"

    return male_matches, female_matches

def count_useful_deviatiors(male_prefs, female_prefs):
    _, truthful_match = deferred_acceptance(male_prefs, female_prefs)
    dev_female_prefs = deepcopy(female_prefs)
    count = 0
    for female in female_prefs.keys():
        while len(dev_female_prefs[female]) > 1:
            dev_female_prefs[female] = dev_female_prefs[female][:-1]
            _, matching_d = deferred_acceptance(male_prefs, dev_female_prefs)

            preference_order = female_prefs[female]

            if useful_deviation(truthful_match, matching_d, female, female_prefs):
                count += 1
                break
        dev_female_prefs[female] = female_prefs[female]
    return count



def useful_deviation(truthful_match, deviated_match, deviator, proposed_prefs):
    preference_order = proposed_prefs[deviator]

    # TODO deal with "NA"
    if deviated_match[deviator] == "NA":
        # if deviation gives no match, it is never useful
        return False
    elif truthful_match[deviator] == "NA":
        # if truthful gives no match and deviation gives a match, it is a useful deviation
        return True
    else:
        return preference_order.index(
            truthful_match[deviator]
        ) > preference_order.index(deviated_match[deviator])


def simulation(rounds, lower, upper, step, debug, logging, k, delta):

    # Run the simulation for all correlation coefficients supplied
    for d in delta:

        # Run the simulation for all preference ordering lengths supplied
        for pref_length in k:
            writer = CsvWriter(d, pref_length, rounds, lower, upper)

            # Initialize while loop that runs the simulation for the specified amount of rounds
            current_round = 0
            while rounds == -1 or rounds > current_round:

                # Run the simulation for ρ and k decided by outer loop, for all n
                for n in range(max(lower, pref_length), upper, step):

                    # Create the preferences for all agents
                    male_prefs, female_prefs = get_preferences(n, pref_length, d)

                    # Run deferred acceptance and look for deviations
                    useful_deviators_cnt = count_useful_deviatiors(male_prefs, female_prefs)

                    # Calculate ratio of agents with useful deviations
                    ratio = useful_deviators_cnt / float(n)

                    if debug == 1 or debug == 0:
                        print(f"d={d} k={pref_length}: result n={n}: ", ratio)

                    if logging:
                        writer.write(n, ratio)

                current_round += 1

if __name__ == "__main__":
    simulation(
            rounds=1,
            lower=10,
            upper=100,
            step=10,
            debug=False,
            logging=True,
            k=[10],
            delta=[1],
        )