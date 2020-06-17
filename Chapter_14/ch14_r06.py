"""Python Cookbook

Chapter 14, recipe 6, Controlling complex sequences of steps.
"""
import argparse
import os
import subprocess
from typing import List


class Command:
    def execute(
            self,
            options: argparse.Namespace
    ) -> str:
        self.os_cmd = self.os_command(options)
        results = subprocess.run(
            self.os_cmd,
            check=True,
            stdout=subprocess.PIPE,
            text=True
        )
        self.output = results.stdout
        return self.output

    def os_command(
            self,
            options: argparse.Namespace
    ) -> List[str]:
        return [
            "echo", self.__class__.__name__, repr(options)
        ]


import Chapter_13.ch13_r05 as ch13_r05


class Simulate(Command):
    def execute(
            self,
            options: argparse.Namespace
    ) -> str:
        if 'seed' in options:
            os.environ["RANDOMSEED"] = str(options.seed)
        return super().execute(options)

    def os_command(
            self,
            options: argparse.Namespace
    ) -> List[str]:
        return [
            "python",
            "Chapter_13/ch13_r05.py",
            "--samples",
            str(options.samples),
            "-o",
            options.game_file,
        ]


import Chapter_13.ch13_r06 as ch13_r06


class Summarize(Command):
    def os_command(
            self,
            options: argparse.Namespace
    ) -> List[str]:
        return [
            "python",
            "Chapter_13/ch13_r06.py",
            "-o",
            options.summary_file,
        ] + options.game_files


from argparse import Namespace
import yaml


def demo() -> None:
    options = Namespace(
        samples=100,
        game_file="data/x13.yaml",
        game_files=["data/x13.yaml"],
        summary_file="data/y13.yaml",
        seed=42
    )
    step1 = Simulate()
    step2 = Summarize()
    output1 = step1.execute(options)
    print(step1.os_cmd, output1)
    output2 = step2.execute(options)
    print(step2.os_cmd, output2)

    with open("data/y13.yaml") as report_file:
        report_document = yaml.load(report_file, Loader=yaml.Loader)
    print(report_document)

test_demo = """
>>> from Chapter_14.ch14_r06 import demo
>>> demo()
['python', 'Chapter_13/ch13_r05.py', '--samples', '100', '-o', 'data/x13.yaml'] 
['python', 'Chapter_13/ch13_r06.py', '-o', 'data/y13.yaml', 'data/x13.yaml'] 
{('loss', 1): 15, ('loss', 2): 11, ('loss', 3): 8, ('loss', 4): 8, ('loss', 5): 4, ('loss', 6): 2, ('loss', 7): 1, ('loss', 11): 1, ('loss', 12): 1, ('win', 1): 24, ('win', 2): 4, ('win', 3): 6, ('win', 4): 4, ('win', 5): 3, ('win', 6): 3, ('win', 7): 4, ('win', 12): 1}

"""

__test__ = {
    n: v for n, v in locals().items() if n.startswith("test_")
}

class IterativeSimulate(Command):
    """Iterative Simulation"""
    def execute(
            self,
            options: argparse.Namespace
    ) -> str:
        step1 = Simulate()
        options.game_files = []
        output = ""
        for i in range(options.simulations):
            options.game_file = f"data/game_{i}.yaml"
            options.game_files.append(options.game_file)
            step_output = step1.execute(options)
            output += step_output
        step2 = Summarize()
        step_output = step2.execute(options)
        output += step_output
        return output


class ConditionalSummarize(Command):
    """Conditional Summarization"""
    def execute(
            self,
            options: argparse.Namespace
    ) -> str:
        step1 = Simulate()
        output = step1.execute(options)
        if "summary_file" in options:
            step2 = Summarize()
            output += step2.execute(options)
        return output

if __name__ == "__main__":
    demo()

    # options_i = Namespace(simulations=2, samples=100, summary_file="data/y13.yaml")
    # iterative = IterativeSimulate()
    # iterative.execute(options_i)
    #
    # options_c = Namespace(simulations=2, samples=100, game_file="data/x.yaml")
    # conditional = ConditionalSummarize()
    # conditional.execute(options_c)

