##
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <alex.rom23@mail.ru> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.       Alex Romanov
# ----------------------------------------------------------------------------
##

from functools import cache
import random
import sys
import getopt
import os

usage_string = "gentest.py -n <num> -o output"


MAX_REQUEST_VALUE = 200
MAX_CACHE_SIZE = 100
MAX_REQUESTS_NUMBER = 10000



def generate_random_test(test_number):
    cache_size = random.randint(1, MAX_CACHE_SIZE)
    requests_number = random.randint(1, MAX_REQUESTS_NUMBER)

    test_str = []
    test_str.append(str(cache_size))
    test_str.append(str(requests_number))

    for request in range(requests_number):
        test_str.append(str(random.randint(0, MAX_REQUEST_VALUE)))
    return test_str

def generate_answer (test):
    cache_size = int(test[0])
    test_list = [int(request) for request in test[2:]]
    # some code here


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
        opts = getopt.getopt(argv, "hn:o:")
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
