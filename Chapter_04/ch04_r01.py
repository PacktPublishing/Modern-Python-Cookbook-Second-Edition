"""Python Cookbook 2nd ed.

Chapter 4, recipe 1, Choosing a data structure
"""

def confirm() -> bool:
    yes = {"yes", "y"}
    no = {"no", "n"}
    while (answer := input("Confirm: ")).lower() not in (yes | no):
        print("Please respond with yes or no")
    return answer in yes


test_confirm = """
>>> from unittest.mock import Mock, patch
>>> mock_input = Mock(side_effect=["what", "yes"])
>>> __builtins__['input'] = mock_input  # Patch
>>> answer = confirm()
Please respond with yes or no
>>> answer
True
"""

test_examples = """
>>> yes = {"yes", "y"}
>>> no = {"no", "n"}
>>> valid_inputs = yes | no
>>> valid_inputs.add("y")
>>> valid_inputs == {'yes', 'no', 'n', 'y'}
True

>>> month_name_list = ["Jan", "Feb", "Mar", "Apr",
...    "May", "Jun", "Jul", "Aug",
...    "Sep", "Oct", "Nov", "Dec"]
>>> month_name_list[8]
'Sep'
>>> month_name_list.index("Feb")
1

>>> scheme = {"Crimson": (220, 14, 60),
... "DarkCyan": (0, 139, 139),
... "Yellow": (255, 255, 00)}
>>> scheme['Crimson']
(220, 14, 60)
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
