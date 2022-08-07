#!/usr/bin/python
##
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <alex.rom23@mail.ru> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.       Alex Romanov
# ----------------------------------------------------------------------------
##
from cgi import test
import random
import sys
import getopt
import os

from numpy import unsignedinteger

usage_string = "gentest.py -n <num> -o output"


MAX_REQUEST_VALUE = 5
MAX_CACHE_SIZE = 3
MAX_REQUESTS_NUMBER = 10



def generate_random_test(test_number):
    cache_size = random.randint(2, MAX_CACHE_SIZE)
    requests_number = random.randint(cache_size, MAX_REQUESTS_NUMBER)

    test_str = []
    test_str.append(str(cache_size))
    test_str.append(str(requests_number))

    for request in range(requests_number):
        test_str.append(str(random.randint(1, MAX_REQUEST_VALUE)))
    return test_str


def find (list_:list, elem:int):
    for i in range(0, len(list_)):
        if (list_[i] == elem):
            return i
    return -1

class ideal_t:
    capacity_ = 0
    size_ = 0
    clist_ = []
    def __init__(self, n:int):
        self.capacity_ = n
        self.clist_ = [-1]*n
    


    def erase (self, test_list:list):
        assert self.capacity_ == len(self.clist_)

        far = -1
        far_i = self.size_
        for ind in range (0, self.capacity_):
            soon = find (test_list, self.clist_[ind])
            if (soon == -1):
                self.size_ -= 1
                return ind
            if (far < soon ):
                far = soon
                far_i = ind
        self.size_ -= 1
        return far_i
                
    def get_best_hits_count (self, test_list:list):
        assert len(self.clist_) == self.capacity_

        hits = 0
        for request in test_list:
            assert self.capacity_ == len(self.clist_)
            ins_ind = self.size_
            if (find(self.clist_, request) == -1): # cache miss
                if (len(self.clist_) == self.size_):
                    ins_ind = self.erase (test_list)
                self.clist_[ins_ind] = request
                self.size_ += 1
            else:
                hits += 1 # cache hit
            test_list = test_list[1:]
        return hits
                

                



def generate_answer (test):
    cache_size = int(test[0])
    test_list = [int(request) for request in test[2:]]
    cache = ideal_t (cache_size)
    hits = cache.get_best_hits_count (test_list)
    return hits
    
            


class CmdArgs:
    number_of_tests = 0
    output_path = "./resources"
    
    def __init__(self):
        pass


def generate_n_random_tests(cmd: CmdArgs):
    for test_number in range(cmd.number_of_tests):
        test_str = generate_random_test(test_number)
        with open (os.path.join(cmd.output_path, "test{}.dat".format(test_number)), 'w+') as test_file:
            test_file.write("{}".format(" ".join(test_str)) + "\n")
        answ = generate_answer(test_str)
        with open (os.path.join(cmd.output_path, "answ{}.dat".format(test_number)), "w+") as answer_file:
            answer_file.write("{}\n".format(answ))



def main (argv):
    cmd = CmdArgs ()
    try :
        opts, args = getopt.getopt(argv, "hn:o:")
    except getopt.GetoptError:
        print (usage_string)
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print (usage_string)
            sys.exit()
        if opt in ("-o", "--output"):
            cmd.output_path = str(arg)
        if opt in ("-n", "--number"):
            cmd.number_of_tests = int(arg)
    generate_n_random_tests (cmd)


main (sys.argv[1:])