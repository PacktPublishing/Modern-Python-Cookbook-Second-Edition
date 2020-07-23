"""Python Cookbook

Chapter 14, recipe 1, Combining two applications into one
"""
import argparse
import collections
import logging
import time
import sys
from typing import List, Counter, Tuple, Optional, Dict
from Chapter_13.ch13_r05 import roll_iter
from Chapter_13.ch13_r06 import gather_stats, Outcome


logger = logging.getLogger("ch13_r07")

def summarize_games(
        total_games: int, *, seed: int = None
    ) -> Counter[Outcome]:
    game_statistics = gather_stats(
        roll_iter(total_games, seed=seed))
    return game_statistics


def win_loss(stats: Dict[Tuple[str, int], int]) -> Counter[str]:
    summary: Counter[str] = collections.Counter()
    for outcome, game_length in stats:
        summary[outcome] += stats[(outcome, game_length)]
    return summary


def simple_composite(
        games: int = 100, rolls: int = 1_000) -> None:
    start = time.perf_counter()
    stats = summarize_games(games*rolls)
    end = time.perf_counter()
    # for outcome in sorted(stats):
    #    logger.debug(f"{outcome}, {total_stats[outcome]}")
    games = sum(stats.values())
    print("games", games, "rolls", rolls)
    print(win_loss(stats))
    print(f"serial: {end-start:.2f} seconds")


from concurrent import futures
import multiprocessing

def parallel_composite(
        games: int = 100,
        rolls: int = 1_000,
        workers: Optional[int] = None) -> None:
    start = time.perf_counter()
    total_stats: Counter[Outcome] = collections.Counter()
    worker_list = []
    with futures.ProcessPoolExecutor(
            max_workers=workers) as executor:
        for i in range(games):
            worker_list.append(executor.submit(summarize_games, rolls))
        for worker in worker_list:
            stats = worker.result()
            total_stats.update(stats)
    end = time.perf_counter()
    # for outcome in sorted(total_stats):
    #    logger.debug(f"{outcome}, {total_stats[outcome]}")
    games = sum(total_stats.values())
    print("games", games, "rolls", rolls)
    print(win_loss(total_stats))
    if workers is None:
        workers = multiprocessing.cpu_count()
    print(f"parallel ({workers}): {end-start:.2f} seconds")


def get_options(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--games", action="store", type=int, default=100)
    parser.add_argument("-r", "--rolls", action="store", type=int, default=1_000)
    parser.add_argument("-w", "--workers", action="store", type=int, default=None)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--parallel", action="store_true", dest="parallel")
    mode.add_argument("-s", "--serial", action="store_true", dest="serial")
    options = parser.parse_args(argv)
    return options


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    opt = get_options()
    if opt.serial:
        simple_composite(games=opt.games, rolls=opt.rolls)
    else:
        parallel_composite(games=opt.games, rolls=opt.rolls, workers=opt.workers)
    logging.shutdown()
