/**
* Quick and dirty solution to speed up Python calculations (at least 100x times performance increase).
**/

#include <vector>
#include <chrono>
#include <memory>
#include <random>
#include <utility>
#include <iostream>
#include <exception>
#include <sstream>
#include <fstream>
#include <string>
#include <cassert>

class TupleGenerator {
    typedef unsigned long T;
    std::default_random_engine generator;
    std::uniform_int_distribution<T> distribution;
    std::vector<T> tuple;
    T total_sum;


    TupleGenerator(const Tree&);
    TupleGenerator(Tree&&);
    TupleGenerator& operator=(const TupleGenerator&);
public:
    TupleGenerator() : generator(std::chrono::system_clock::now().time_since_epoch().count()), distribution(), tuple(), total_sum() {
    }

    /**
    * Generate a tuple with specified number of new children and number of iterations.
    */
    std::size_t generate(const std::size_t new_children_num, const std::size_t num_iterations) {
        tuple.resize(0);
        total_sum = 1;
        tuple.push_back(1);

        for (std::size_t i = 0; i < num_iterations; ++i) {
            step(new_children_num);
        }
        return tuple.size();
    }

    /**
    * Generate a tuple with specified number of iterations and the number of children uniformly random from
    * [new_children_num_min, new_children_num_max).
    */
    std::size_t generate(const std::size_t new_children_num_min, const std::size_t new_children_num_max,
            const std::size_t num_iterations) {
        tuple.resize(0);
        total_sum = 1;
        tuple.push_back(1);

        const auto diff = new_children_num_max - new_children_num_min;
        assert (diff > 0);
        for (std::size_t i = 0; i < num_iterations; ++i) {
            const std::size_t new_children_num = new_children_num_min + distribution(generator) % diff;
            step(new_children_num);
        }
        return tuple.size();
    }

private:
    void step(const std::size_t new_children_num) {
        const auto rnd = distribution(generator) % total_sum;
        T cum_sum = 0;
        for (std::size_t i = 0; i < tuple.size(); ++i) {
            cum_sum += tuple[i];
            if (cum_sum > rnd) {
                ++tuple[i];
                if (i < tuple.size() - 1) {
                    tuple[i + 1] += new_children_num;
                } else {
                    tuple.push_back(new_children_num);
                }
                total_sum += 1 + new_children_num;
                return;
            }
        }
        throw std::exception();
    }
};


int main(int argc, char** argv) {
    if (argc != 5) {
        std::cout << "params: [new_children_num_min] [new_children_num_max] [max_scale] [iterations_num]" << std::endl;
        return 1;
    }
    TupleGenerator gen;
    std::size_t size = 1;
    const std::size_t new_children_num_min = std::stoi(std::string(argv[1]));
    const std::size_t new_children_num_max = std::stoi(std::string(argv[2]));
    const std::size_t max_scale = std::stoi(std::string(argv[3]));
    const std::size_t iterations_num = std::stoi(std::string(argv[4]));
    if (new_children_num_min == new_children_num_max) {
        const std::size_t new_children_num = new_children_num_min;
        std::stringstream filename;
        filename << "tuple_4x_" << new_children_num << "_" << max_scale << "_" << iterations_num;
        std::ofstream out(filename.str(), std::ofstream::out);
        std::cout << "Starting with max_scale=" << max_scale << " and iterations=" << iterations_num << std::endl;
        for (std::size_t scale = 0; scale < max_scale; ++scale) {
            long sum = 0;
            for (std::size_t i = 0; i < iterations_num; ++i) {
                const auto v = gen.generate(new_children_num, size);
                sum += v;
                out << v;
                if (i != iterations_num - 1)
                    out << " ";
            }
            out << std::endl;
            std::cout << "size=" << size << " mean=" << static_cast<double>(sum) / iterations_num << std::endl;
            size *= 4;
        }
    } else {
        if (new_children_num_min > new_children_num_max) {
            std::cout << "new_children_num_min must be not greater than new_children_num_max" << std::endl;
            return 1;
        }
        std::stringstream filename;
        filename << "tuple_4x_" << new_children_num_min << "-" << new_children_num_max << "_" << max_scale << "_" << iterations_num;
        std::ofstream out(filename.str(), std::ofstream::out);
        std::cout << "Starting with max_scale=" << max_scale << " and iterations=" << iterations_num << std::endl;
        for (std::size_t scale = 0; scale < max_scale; ++scale) {
            long sum = 0;
            for (std::size_t i = 0; i < iterations_num; ++i) {
                const auto v = gen.generate(new_children_num_min, new_children_num_max, size);
                sum += v;
                out << v;
                if (i != iterations_num - 1)
                    out << " ";
            }
            out << std::endl;
            std::cout << "size=" << size << " mean=" << static_cast<double>(sum) / iterations_num << std::endl;
            size *= 4;
        }
    }


}