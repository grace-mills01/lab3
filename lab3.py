import builtins
from typing import *
from dataclasses import dataclass
import unittest
import math
import sys

sys.setrecursionlimit(10**6)


@dataclass(frozen=True)
class LLNode:
    value: int
    rest: "LinkedList"


LinkedList: TypeAlias = Union[LLNode, None]

LL_start: LinkedList = LLNode(0, None)
LL_none: LinkedList = None


# creates a linked list from 0 to a max number -1 given in the parameter
def range(max_exclusive: int) -> LinkedList:
    if max_exclusive <= 0:
        return None

    def helper(i):
        if i == max_exclusive:
            return None
        return LLNode(i, helper(i + 1))

    return helper(0)


# finds whether an integer occurs in a linked list
def occurs(ll: LinkedList, check: int) -> bool:
    match ll:
        case None:
            return False
        case LLNode(value, rest):
            if value == check:
                return True
            else:
                return occurs(rest, check)


ll_len_4 = LLNode(0, LLNode(1, LLNode(2, LLNode(3, None))))
ll_len_3 = LLNode(0, LLNode(1, LLNode(2, None)))

# returns whether or not 'll' has any duplicate values
def has_dup(ll : LinkedList) -> bool:
    lis = []
    while ll != None:
        if ll.value in lis:
            return True
        else:
            lis.append(ll.value)
            ll = ll.rest
    
    return False

# Returns a new list in which "new_num" is inserted in the propery spot to maintain the order in a non-empty list "arr"
def insert(arr : LinkedList, new_num : int) -> LinkedList:
    match arr:
        case None:
            return LLNode(new_num, None)
        case LLNode(value, rest):
            if value > new_num:
                return LLNode(new_num, arr)
            else:
                return LLNode(value,insert(rest, new_num))

# Returns a new list which contains the same items as "ll" but sorted in ascending order
def insertion_sort(ll : LinkedList) -> LinkedList:
    answer = None
    while ll != None:
        answer = insert(answer, ll.value)
        ll = ll.rest

    return answer
    

class Tests(unittest.TestCase):
    def test_range(self):
        self.assertEqual(range(3), ll_len_3)
        self.assertEqual(range(4), ll_len_4)

    def test_occurs(self):
        self.assertEqual(occurs(ll_len_4, 1), True)
        self.assertEqual(occurs(ll_len_3, 6), False)

    def test_has_dup(self):
        ll_unique = LLNode(0, LLNode(1, LLNode(2, LLNode(3, None))))
        ll_dup_start = LLNode(1, LLNode(1, LLNode(2, LLNode(3, None))))
        ll_dup_end = LLNode(0, LLNode(1, LLNode(2, LLNode(2, None))))
        ll_all_same = LLNode(5, LLNode(5, LLNode(5, None)))
        ll_empty = None

        self.assertEqual(has_dup(ll_unique), False)     
        self.assertEqual(has_dup(ll_dup_start), True)   
        self.assertEqual(has_dup(ll_dup_end), True) 
        self.assertEqual(has_dup(ll_all_same), True)     
        self.assertEqual(has_dup(ll_empty), False)

    def test_insertion_sort(self):
        # 1. Setup: Create 3 -> 1 -> 2
        head = LLNode(3, LLNode(1, LLNode(2, None)))

        # 3. Assert: Check values in order
        self.assertEqual(insertion_sort(head), LLNode(1, LLNode(2, LLNode(3, None))))
    
# Remember from Lab 1: this if statements checks
# whether this module (ghg.py) is the module
# being executed or whether it's just being
# imported from some other module.
if __name__ == "__main__":
    unittest.main()
