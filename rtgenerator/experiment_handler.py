__author__ = 'Pavel Morar <pvmorar@gmail.com>'

import numpy as np
import pickle
from matplotlib import pyplot as plt
import math
import scipy.optimize

from rtgenerator.tuple_generator import generate_random_state_size
from rtgenerator.tree_generator import generate_random_tree_height


def run_experiment(func, children_num_generator, step_nums, iterations_num=10000):
    print 'iterations=', iterations_num, 'steps num=', step_nums
    results = []
    for n in step_nums:
        print 'step_num=', n
        samples = [func(children_num_generator, n) for i in xrange(iterations_num)]
        results.append(samples)
    return results


def save_to(filename, step_nums, results):
    with open(filename + '_steps.pickle', "w") as f_pickle:
        pickle.dump(step_nums, f_pickle)
    with open(filename + '_res.pickle', "w") as f_pickle:
        pickle.dump(results, f_pickle)
    with open(filename + '.txt', "w") as f:
        f.write("Generator: 1\n")
        f.write("Steps: %s\n" % step_nums.__str__())
        for n, r in enumerate(results):
            f.write("for step %d results: %s\n" % (step_nums[n], r))


def load_from(filename):
    with open(filename + '_steps.pickle', "r") as f_pickle:
        step_nums = pickle.load(f_pickle)
    with open(filename + '_res.pickle', "r") as f_pickle:
        results = pickle.load(f_pickle)
    return step_nums, results


def statistics(ys):
    stats = {'mean': [], 'min': [], 'max': [], 'quantile 0.999': [], 'mean of upper 5%': []}
    for r in ys:
        stats['mean'].append(np.mean(r))
        stats['min'].append(np.min(r))
        stats['max'].append(np.max(r))
        stats['quantile 0.999'].append(np.percentile(r, 99.9))
        upper10perc = sorted(r)[len(r)*19 / 20:]
        stats['mean of upper 5%'].append(np.mean(upper10perc))
    for n, s in stats.iteritems():
        stats[n] = np.array(s, dtype=np.float)
    return stats


def plt_results(xs, ys, filename=None, xlabel='Steps num', ylabel='Tree height'):
    plt.figure(figsize=(10, 7))
    stats = statistics(ys)

    for name, stat in stats.iteritems():
        plt.semilogx(xs, stat, label=name)

    plt.legend(loc='best')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    if filename is not None:
        plt.savefig(filename + '.jpg')


def slopes_with_mapped_x(xs, ys, x_func=np.log, slopes_aggregation=None):
    mapped_xs = x_func(xs)
    x_increment = mapped_xs[1:] - mapped_xs[:-1]
    stats = statistics(ys)
    out = {}
    for name, stat in stats.iteritems():
        slopes = (stat[1:] - stat[:-1]) / x_increment
        if slopes_aggregation is None:
            out[name] = slopes
        else:
            out[name] = slopes_aggregation(slopes)
    return out


def theoretical_slope(expectation):
    alpha = expectation + 1
    eq_func = lambda x: expectation*x*math.exp(x+1) - 1.0
    gamma = scipy.optimize.brentq(eq_func, 0, 100)
    return alpha, gamma, 1.0 / (alpha * gamma)


def run(name, step_nums, generator, children_num_callback, iterations):
    results = run_experiment(generator, children_num_callback, step_nums, iterations)
    save_to(name, step_nums, results)
    plt_results(step_nums, results, name)
    return results


def load_cpp_output(filename):
    with open(filename) as in_file:
        v = []
        i = 0
        for line in in_file:
            if (len(line) > 0):
            # if i == 12:
            #         v.append([int(e) for e in line[:-1].split(' ')])
            #         break
                i += 1
                v.append([int(e) for e in line.split(' ')])
        return np.array(v)


if __name__ == '__main__':
    run('test', [2 ** x for x in xrange(3)], generate_random_state_size, lambda: 1, 10)