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


class Tests(unittest.TestCase):
    def test_range(self):
        self.assertEqual(range(3), ll_len_3)
        self.assertEqual(range(4), ll_len_4)

    def test_occurs(self):
        self.assertEqual(occurs(ll_len_4, 1), True)
        self.assertEqual(occurs(ll_len_3, 6), False)


# Remember from Lab 1: this if statements checks
# whether this module (ghg.py) is the module
# being executed or whether it's just being
# imported from some other module.
if __name__ == "__main__":
    unittest.main()
