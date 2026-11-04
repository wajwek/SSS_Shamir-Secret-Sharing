from shamir.validation import (
    SECRET,
    all_share_combinations,
    can_reconstruct_secret,
    validate_example,
)


POINTS = [(1, 15), (2, 14), (3, 2)]


def test_validate_example_prints_q_and_reconstructed_secret(capsys):
    assert validate_example() == 5

    assert capsys.readouterr().out == (
        "Secret = 5\n"
        "Reconstructed secret = 5\n"
    )


def test_all_share_combinations_include_all_valid_combination_sizes():
    combinations = all_share_combinations()

    assert len(combinations) == 16
    assert {len(points) for points in combinations} == {3, 4, 5}


def test_all_share_combinations_reconstruct_secret():
    assert all(
        can_reconstruct_secret(list(points), secret=SECRET)
        for points in all_share_combinations()
    )


def test_can_reconstruct_secret_rejects_wrong_secret():
    assert not can_reconstruct_secret(POINTS, secret=6, degree=2, q=17)


def test_can_reconstruct_secret_rejects_too_few_shares():
    assert not can_reconstruct_secret(POINTS[:2], secret=5, degree=2, q=17)
