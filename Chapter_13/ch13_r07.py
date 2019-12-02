"""Python Cookbook

Chapter 13, recipe 7
"""
from Chapter_13.ch13_r05 import roll_iter
from Chapter_13.ch13_r06 import gather_stats, Outcome
import collections
import time
from typing import List, Counter, Tuple, Iterable, Dict


def summarize_games(total_games: int, *, seed: int = None) -> Counter[Outcome]:
    game_statistics = gather_stats(roll_iter(total_games, seed=seed))
    return game_statistics


def win_loss(stats: Dict[Tuple[str, int], int]):
    summary: Counter[str] = collections.Counter()
    for outcome, game_length in stats:
        summary[outcome] += stats[(outcome, game_length)]
    return summary


def simple_composite(games: int = 100_000) -> None:
    start = time.perf_counter()
    stats = summarize_games(games)
    end = time.perf_counter()
    # for outcome in sorted(stats):
    #    print(outcome, stats[outcome])
    games = sum(stats.values())
    print("games", games)
    print(win_loss(stats))
    print(f"{end-start:.2f} seconds")


import concurrent.futures


def parallel_composite(games: int = 100, rolls: int = 1_000) -> None:
    start = time.perf_counter()
    total_stats: Counter[Outcome] = collections.Counter()
    worker_list = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(games):
            worker_list.append(executor.submit(summarize_games, rolls))
        for worker in worker_list:
            stats = worker.result()
            total_stats.update(stats)
    end = time.perf_counter()
    # for outcome in sorted(total_stats):
    #    print(outcome, total_stats[outcome])
    games = sum(total_stats.values())
    print("games", games)
    print(win_loss(total_stats))
    print("{end-start:.2f} seconds")


import logging, sys

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    simple_composite(100_000)
    # parallel_composite()
    logging.shutdown()
