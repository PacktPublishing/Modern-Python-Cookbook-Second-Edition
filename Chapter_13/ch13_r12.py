"""Python Cookbook

Chapter 13, recipe 12
"""
import argparse
import os
import subprocess
from typing import List


class Command:
    def execute(self, options: argparse.Namespace) -> str:
        self.command = self.create_command(options)
        results = subprocess.run(
            self.command, check=True, stdout=subprocess.PIPE, text=True
        )
        self.output = results.stdout
        return self.output

    def create_command(self, options: argparse.Namespace) -> List[str]:
        return ["echo", self.__class__.__name__, repr(options)]


import Chapter_13.ch13_r05 as ch13_r05


class Simulate(Command):
    def __init__(self, seed: int = None) -> None:
        self.seed = seed

    def execute(self, options: argparse.Namespace) -> str:
        if self.seed:
            os.environ["RANDOMSEED"] = str(self.seed)
        return super().execute(options)

    def create_command(self, options: argparse.Namespace) -> List[str]:
        return [
            "python3",
            "Chapter_13/ch13_r05.py",
            "--samples",
            str(options.samples),
            "-o",
            options.game_file,
        ]


import Chapter_13.ch13_r06 as ch13_r06


class Summarize(Command):
    def create_command(self, options: argparse.Namespace) -> List[str]:
        return [
            "python3",
            "Chapter_13/ch13_r06.py",
            "-o",
            options.summary_file,
        ] + options.game_files


from argparse import Namespace
import yaml


def demo():
    options = Namespace(
        samples=100,
        game_file="data/x12.yaml",
        game_files=["data/x12.yaml"],
        summary_file="data/y12.yaml",
    )
    step1 = Simulate()
    step2 = Summarize()
    output1 = step1.execute(options)
    print(step1.command, output1)
    output2 = step2.execute(options)
    print(step2.command, output2)

    with open("data/y12.yaml") as report_file:
        report_document = yaml.load(report_file)
    print(report_document)


def process_i(options: argparse.Namespace):
    step1 = Simulate()
    options.game_files = []
    for i in range(options.simulations):
        options.game_file = f"data/game_{i}.yaml"
        options.game_files.append(options.game_file)
        step1.execute(options)
    step2 = Summarize()
    step2.execute(options)


def process_c(options: argparse.Namespace):
    step1 = Simulate()
    step1.execute(options)
    if "summary_file" in options:
        step2 = Summarize()
        step2.execute(options)


if __name__ == "__main__":
    demo()
    options_i = Namespace(simulations=2, samples=100, summary_file="data/y12.yaml")
    process_i(options_i)
    options_c = Namespace(simulations=2, samples=100, game_file="data/x.yaml")
    process_c(options_c)
