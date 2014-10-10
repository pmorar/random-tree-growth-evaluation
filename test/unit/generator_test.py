__author__ = 'pmorar'

import unittest
import numpy as np
import numpy.random as random
import numpy.testing
import src.generator as generator


class TestGenerator(unittest.TestCase):

    def random_state(self):
        return random.randint(0, 10)

    def test_weighted_level_generator_picks_index_0_for_size_one_state(self):
        state = [1]
        pos = generator.weighted_level_generator(state)
        self.assertEqual(0, pos)

    def test_weighted_level_generator_never_picks_0_entry_in_end(self):
        for n in xrange(1000):
            state = random.random_integers(1, 10, 10)
            excluded_pos = random.randint(1, 10)
            state[excluded_pos:] = 0
            pos = generator.weighted_level_generator(state)
            self.assertLess(pos, excluded_pos)

    def test_weighted_level_generator_picks_within_state_size(self):
        for n in xrange(1000):
            size = random.randint(1, 100)
            state = random.random_integers(1, 10, size)
            pos = generator.weighted_level_generator(state)
            self.assertGreaterEqual(pos, 0)
            self.assertLess(pos, size)

    def test_weighted_level_generator_proportions(self):
        """It might fail with low probability."""
        state = [1000, 1]
        counts = [0, 0]
        for n in xrange(1000):
            pos = generator.weighted_level_generator(state)
            self.assertGreaterEqual(pos, 0)
            self.assertLess(pos, 2)
            counts[pos] += 1
        self.assertLessEqual(counts[1], 6)

        state = [1, 1000]
        counts = [0, 0]
        for n in xrange(1000):
            pos = generator.weighted_level_generator(state)
            self.assertGreaterEqual(pos, 0)
            self.assertLess(pos, 2)
            counts[pos] += 1
        self.assertLessEqual(counts[0], 6)

    def test_weighted_level_generator_with_cum_sum(self):
        for n in xrange(1000):
            state = random.random_integers(1, 10, 10)
            cum_sum = np.cumsum(state)
            rand_state = random.get_state()
            pos = generator.weighted_level_generator(state)
            random.set_state(rand_state)
            cs_pos = generator.weighted_level_generator(state, cum_sum)
            self.assertEqual(pos, cs_pos)

    def test_generate_random_state_with_last_position(self):
        for steps_num in xrange(5, 100, 5):
            sample = generator.generate_random_state(lambda: 1, lambda x: np.sum(x != 0) - 1, steps_num)
            self.assertEqual(np.sum(sample != 0), steps_num + 1)

    def test_generate_random_state_not_modifying_state_with_num_steps_0(self):
        state = np.ones(5)
        sample = generator.generate_random_state(lambda: 1, lambda x: 1, 0, state)
        self.assertIs(state, sample)

    def test_generate_random_state_copy_state(self):
        state = np.ones(5)
        sample = generator.generate_random_state(lambda: 1, lambda x: 1, 0, state, copy=True)
        self.assertIsNot(state, sample)
        numpy.testing.assert_equal(sample, state)

    def test_generate_random_state_default_state(self):
        sample = generator.generate_random_state(lambda: 1, lambda x: 1, 0)
        numpy.testing.assert_equal(sample[sample != 0], np.ones(1))

    def test_generate_random_state_follows_number_of_children(self):
        state = np.ones(1)
        for n in xrange(10):
            sample = generator.generate_random_state(lambda: 1, lambda x: random.randint(0, np.sum(x != 0)), 1000, state, copy=True)
            self.assertEqual(np.sum(sample), 2001)

        for n in xrange(10):
            children_nums = random.randint(0, 10, 1000)

            def gen(children_num):
                for x in children_nums:
                    yield x

            g = gen(children_nums)
            sample = generator.generate_random_state(lambda: g.next(), lambda x: random.randint(0, np.sum(x != 0)), 1000, state, copy=True)
            self.assertEqual(np.sum(sample), 1001 + np.sum(children_nums))

    def test_generate_random_state_follows_levels(self):
        state = np.ones(2)
        for n in xrange(10):
            sample = generator.generate_random_state(lambda: 1, lambda x: 0, 1000, state, copy=True)
            numpy.testing.assert_equal(sample[sample != 0], [1001, 1001])

        for n in xrange(10):
            sample = generator.generate_random_state(lambda: 1, lambda x: 1, 1000, state, copy=True)
            numpy.testing.assert_equal(sample[sample != 0], [1, 1001, 1000])


if __name__ == '__main__':
    unittest.main()
