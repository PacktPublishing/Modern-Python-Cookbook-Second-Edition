"""Python Cookbook 2nd ed.

Chapter 7, recipe 2, timing comparison
"""

import timeit

if __name__ == "__main__":

    m1 = timeit.timeit(
        """repr(card)""",
        setup="""
from ch07_r02 import make_card
card = make_card(10,'S')
    """,
    )

    m2 = timeit.timeit(
        """str(card)""",
        setup="""
from ch07_r02 import make_card
card = make_card(10,'S')
    """,
    )

    print(f"Card.__repr__ make time {m1:.4f}")
    print(f"object.__str__ make time {m2:.4f}")
    print(f"{abs(m1-m2)/m1:.1%} difference")
