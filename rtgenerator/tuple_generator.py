__author__ = 'pmorar'
"""
To study random tree heights we just need to generate random tuples. This file contains methods to do that.
"""

import numpy as np
import numpy.random as random
import math


def weighted_level_generator(state, cum_sum=None, size=None):
    """Picks a random level of state with respect to its contents.

    Generates a random level of state. The probability of the level is proportional to the corresponding weight.
    Args:
        state (array): array of weights with possible trailing zeros.
        cum_sum (array): cumulative sum of state (defaults to None).
        size: size of state not including trailing zeros (ignored for now).

    Returns:
        a random level.
    """
    # if size is not None:
    #     if cum_sum is None:
    #         cum_sum = np.cumsum(state[:size])
    #     n = random.randint(0, cum_sum[size-1])
    #     return np.searchsorted(cum_sum[:size], n)
    if cum_sum is None:
        cum_sum = np.cumsum(state)
    n = 1 + random.randint(0, cum_sum[-1])
    return np.searchsorted(cum_sum, n)


def generate_random_state(children_num_generator, level_generator, num_steps=1, initial_state=None, copy=False):
    """Generates a random state by iteratively attaching a random number of children to a random level.

    Generates a random index of an array state. The probability of the index is proportional to the corresponding value.
    Args:
        children_num_generator (callback): on call generates a number of children.
        level_generator (callback(state)): on call generate a level of state to add children.
        num_steps (int): the number of steps to perform.
        initial_state (array): the initial state (defaults to [1] with possible trailing zeros for performance reasons).
        copy (boolean): whether or not to copy the initial state (defaults to False).

    Returns:
        a random state.
    """
    default_size_bound = 10
    if initial_state is None:
        if num_steps < default_size_bound:
            initial_len = 1 + num_steps
        else:
            initial_len = 1 + default_size_bound + int(math.log(num_steps))
        state = np.zeros(initial_len, dtype=int)
        state[0] = 1
    else:
        if copy:
            state = initial_state.copy()
        else:
            state = initial_state

    for i in xrange(num_steps):
        # using cum_sum and size does not help to speed up
        level = level_generator(state)
        state[level] += 1
        n = children_num_generator()
        if level == len(state) - 1:
            state.resize((len(state) + default_size_bound,))
        state[level + 1] += n

    return state

def generate_random_state_size(children_num_generator, num_steps):
    return np.argmin(generate_random_state(children_num_generator, weighted_level_generator,
                                           num_steps))