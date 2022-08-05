#include <cassert>
#include <iostream>
#include <vector>

#include "belady.hpp"

int main ()
{
    size_t n {}, m {};

    std::cin >> m >> n;
    assert (std::cin.good ());

    std::vector<int> vec {};
    vec.reserve (n);

    for ( int i = 0; i < n; i++ )
    {
        int temp {};
        std::cin >> temp;

        assert (std::cin.good ());

        vec.push_back (temp);
    }

    auto hits = cache::get_best_hits_count<int> (m, vec.begin (), vec.end ());
    std::cout << hits << std::endl;
}