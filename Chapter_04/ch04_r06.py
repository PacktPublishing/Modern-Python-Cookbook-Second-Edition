"""Python Cookbook 2nd ed.

Chapter 4, recipe 6, Reversing a copy of a list
"""

test_construct = """
>>> week = 13
>>> day = 2
>>> hour = 7
>>> minute = 53
>>> second = 19
>>> t_s = (((week*7+day)*24+hour)*60+minute)*60+second
>>> t_s
8063599
"""

test_destruct = """
>>> t_s = 8063599
>>> fields = []
>>> for b in 60, 60, 24, 7:
...    t_s, f = divmod(t_s, b)
...    fields.append(f)
>>> fields.append(t_s)
>>> fields
[19, 53, 7, 2, 13]

One reversal.

>>> fields_copy1 = fields.copy()
>>> fields_copy1.reverse()
>>> fields_copy1
[13, 2, 7, 53, 19]

Another reversal.

>>> fields_copy2 = fields[::-1]
>>> fields_copy2
[13, 2, 7, 53, 19]

A third.

>>> fields_copy3 = list(reversed(fields))
>>> fields_copy3
[13, 2, 7, 53, 19]
"""

test_walrus = """
>>> t_s = (8063599, 0)
>>> fields = [(t_s := divmod(t_s[0], b))[1] for b in (60, 60, 24, 7)]
>>> list(reversed(fields + [t_s[0]]))
[13, 2, 7, 53, 19]
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
