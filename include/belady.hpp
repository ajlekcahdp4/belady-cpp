/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <alex.rom23@mail.ru> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.       Alex Romanov
 * ----------------------------------------------------------------------------
 */

#pragma once

#include <algorithm>
#include <cassert>
#include <deque>
#include <iterator>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <utility>

namespace cache
{
template <typename T, typename iterator_t> class ideal_cache_t
{
    using occurence_map = typename std::unordered_map<T, std::deque<size_t>>;

    occurence_map occur_map_;
    std::vector<T> cvec_;
    std::unordered_set<T> inserted_set_;
    size_t capacity_;
    size_t size_ = 0;

    void fill (iterator_t begin, iterator_t end)
    {
        if ( begin == end )
            throw std::invalid_argument ("Wrong argument(s) in get_best_hits_count ()");

        size_t step {};
        for ( ; begin != end; begin++, step++ )
        {
            auto &ins_que = occur_map_.emplace (*begin, std::deque<size_t> {}).first->second;
            ins_que.push_back (step);
        }
    }

  public:
    bool full () const { return size_ == capacity_; }

    ideal_cache_t (size_t m, iterator_t begin, iterator_t end) : capacity_ (m)   // O(n)
    {
        cvec_.reserve (m);
        fill (begin, end);
    }

    bool lookup_update (const T &to_insert)
    {
        auto found = inserted_set_.find (to_insert);
        if ( found == inserted_set_.end () )
        {
            auto insert_ind = -1;
            if ( full () )
                insert_ind = erase ();
            insert (insert_ind, to_insert);
            return false;
        }
        promote (to_insert);
        return true;
    }

  private:
    size_t erase ()
    {
        std::pair<size_t, size_t> to_erase {0, 0};

        for ( auto i = 0; i < cvec_.size (); i++ )
        {
            auto found = occur_map_.find (cvec_[i]);
            if ( found == occur_map_.end () )
            {
                inserted_set_.erase (cvec_[i]);
                size_--;
                return i;
            }
            auto found_soon = found->second[0];
            if ( found_soon > to_erase.first )
            {
                to_erase.first  = found_soon;
                to_erase.second = i;
            }
        }
        assert (to_erase.second <= cvec_.size ());
        inserted_set_.erase (cvec_[to_erase.second]);
        size_--;

        return to_erase.second;
    }

    void insert (size_t ind, const T &to_insert)
    {
        if ( ind == -1 )   // to optimize
            cvec_.push_back (to_insert);
        else
            cvec_[ind] = to_insert;
        inserted_set_.insert (to_insert);
        promote (to_insert);
        size_++;
    }

    void promote (const T &to_promote)
    {
        auto found = occur_map_.find (to_promote);
        assert (found != occur_map_.end ());
        auto &que = found->second;
        que.pop_front ();
        if ( que.empty () )
            occur_map_.erase (to_promote);
    }
};

template <typename T, typename iterator_t> size_t get_best_hits_count (size_t size, iterator_t begin, iterator_t end)
{
    if ( !size || begin == end )
        throw std::invalid_argument ("Wrong argument(s) in get_best_hits_count ()");

    ideal_cache_t<T, iterator_t> cache {size, begin, end};

    size_t hits {};
    for ( ; begin != end; begin++ )
    {
        if ( cache.lookup_update (*begin) )
            hits++;
    }
    return hits;
}
}   // namespace cache