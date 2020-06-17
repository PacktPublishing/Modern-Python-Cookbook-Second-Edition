"""Python Cookbook

Chapter 14, recipe 3, Managing arguments and configuration in composite applications
"""
import yaml
import Chapter_14.ch14_r03

def test_simulate(monkeypatch, tmpdir):
    options = Chapter_14.ch14_r03.get_options(
        ["simulate", "-g", "5", "-o", str(tmpdir/"x.yaml"), "--seed", "42"]
    )
    assert options.command == Chapter_14.ch14_r03.Simulate

    cmd_instance = options.command()
    cmd_instance.execute(options)

    body = (tmpdir/"x.yaml").read_text(encoding="utf-8")
    sim_results = list(yaml.load_all(body, Loader=yaml.SafeLoader))
    expected = [
        [[4, 4], [6, 3], [1, 1], [1, 5], [4, 2], [2, 4], [3, 4]],
        [[2, 2], [3, 3], [6, 3], [6, 1]],
        [[4, 5], [6, 6], [6, 1]],
        [[2, 6], [2, 6]],
        [[6, 3], [1, 5], [6, 5], [2, 3], [4, 1], [3, 2], [1, 4],
         [5, 3], [2, 2], [1, 2], [2, 6], [2, 2], [4, 3]]
    ]
    assert expected == sim_results


def test_simulate_summarize(monkeypatch, tmpdir):
    options_1 = Chapter_14.ch14_r03.get_options(
        ["simulate", "-g", "5", "-o", str(tmpdir/"x.yaml"), "--seed", "42"]
    )
    assert options_1.command == Chapter_14.ch14_r03.Simulate

    cmd_instance = options_1.command()
    cmd_instance.execute(options_1)

    body = (tmpdir/"x.yaml").read_text(encoding="utf-8")
    sim_results = list(yaml.load_all(body, Loader=yaml.SafeLoader))
    expected = [
        [[4, 4], [6, 3], [1, 1], [1, 5], [4, 2], [2, 4], [3, 4]],
        [[2, 2], [3, 3], [6, 3], [6, 1]],
        [[4, 5], [6, 6], [6, 1]],
        [[2, 6], [2, 6]],
        [[6, 3], [1, 5], [6, 5], [2, 3], [4, 1], [3, 2], [1, 4],
         [5, 3], [2, 2], [1, 2], [2, 6], [2, 2], [4, 3]]
    ]
    assert expected == sim_results

    options_2 = Chapter_14.ch14_r03.get_options(
        ["summarize", "-o", str(tmpdir/"y.yaml"), str(tmpdir/"x.yaml")]
    )
    assert options_2.command == Chapter_14.ch14_r03.Summarize

    cmd_instance = options_2.command()
    cmd_instance.execute(options_2)
    body = (tmpdir/"y.yaml").read_text(encoding="utf-8")
    sum_results = list(yaml.load_all(body, Loader=yaml.UnsafeLoader))
    expected = [
        {('loss', 3): 1,
        ('loss', 4): 1,
        ('loss', 7): 1,
        ('loss', 13): 1,
        ('win', 2): 1}
    ]
    assert expected == sum_results


def test_simsumm(monkeypatch, tmpdir, capsys):
    options_1 = Chapter_14.ch14_r03.get_options(
        ["simsum", "-g", "5", "-o", str(tmpdir/"y.yaml"), "--seed", "42"]
    )
    assert options_1.command == Chapter_14.ch14_r03.SimSum

    cmd_instance = options_1.command()
    cmd_instance.execute(options_1)

    expected = [
        {('loss', 3): 1,
        ('loss', 4): 1,
        ('loss', 7): 1,
        ('loss', 13): 1,
        ('win', 2): 1}
    ]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "Counter({('loss', 7): 1, ('loss', 4): 1, ('loss', 3): 1, ('win', 2): 1, ('loss', 13): 1})"
    ]
