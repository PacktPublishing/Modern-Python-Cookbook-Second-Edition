"""Python Cookbook

Chapter 13, recipe 6, Using logging for control and audit output
"""
import argparse
import collections
import logging
from pathlib import Path
import sys
from typing import List, Iterable, Tuple, Counter, TextIO
import yaml

detail_log = logging.getLogger("overview_stats.detail")
write_log = logging.getLogger("overview_stats.write")


def get_options(
        argv: List[str] = sys.argv[1:]
    ) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="*", type=Path)
    parser.add_argument("-o", "--output")
    options = parser.parse_args(argv)
    detail_log.debug("options: %r", options)
    return options


def main(argv: List[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    if options.output is not None:
        report_path = Path(options.output)
        with report_path.open("w") as result_file:
            process_all_files(result_file, options.file)
        write_log.info("wrote %r", report_path)
    else:
        process_all_files(sys.stdout, options.file)


def process_all_files(
        result_file: TextIO,
        file_paths: Iterable[Path]
    ) -> None:
    for source_path in file_paths:
        detail_log.info("read %r", source_path)
        with source_path.open() as source_file:
            game_iter = yaml.load_all(
                source_file,
                Loader=yaml.SafeLoader)
            statistics = gather_stats(game_iter)
            result_file.write(
                yaml.dump(
                    dict(statistics),
                    explicit_start=True))


Outcome = Tuple[str, int]


def gather_stats(
        game_iter: Iterable[List[List[int]]]
    ) -> Counter[Outcome]:
    counts: Counter[Outcome] = collections.Counter()
    for game in game_iter:
        if len(game) == 1 and sum(game[0]) in (2, 3, 12):
            outcome = "loss"
        elif len(game) == 1 and sum(game[0]) in (7, 11):
            outcome = "win"
        elif len(game) > 1 and sum(game[-1]) == 7:
            outcome = "loss"
        elif (len(game) > 1
              and sum(game[0]) == sum(game[-1])):
            outcome = "win"
        else:
            detail_log.error("problem with %r", game)
            raise Exception(
                f"Wait, What? "
                f"Inconsistent len {len(game)} and "
                f"final {sum(game[-1])} roll"
            )
        event = (outcome, len(game))
        detail_log.debug("game %r -> event %r", game, event)
        counts[event] += 1
    return counts


import logging.config

if __name__ == "__main__":
    from textwrap import dedent
    config_yaml = dedent("""\
    version: 1
    formatters:
        default:
            style: "{"
            format: "{levelname}:{name}:{message}"
            #   Example: INFO:overview_stats.detail:read x.yaml
        timestamp:
            style: "{"
            format: "{asctime}//{levelname}//{name}//{message}"
    
    handlers:
        console:
            class: logging.StreamHandler
            stream: ext://sys.stderr
            formatter: default
        file:
            class: logging.FileHandler
            filename: data/write.log
            formatter: timestamp
    
    loggers:
        overview_stats.detail:
            handlers:
            -   console
        overview_stats.write:
            handlers:
            -   file
            -   console
    
    root:
        level: INFO
    """)
    logging.config.dictConfig(
        yaml.load(config_yaml, Loader=yaml.SafeLoader))
    # logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    main()
    logging.shutdown()
