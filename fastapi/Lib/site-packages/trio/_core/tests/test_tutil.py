import pytest

from .tutil import check_sequence_matches


def test_check_sequence_matches():
    check_sequence_matches([1, 2, 3], [1, 2, 3])
    with pytest.raises(AssertionError):
        check_sequence_matches([1, 3, 2], [1, 2, 3])
    check_sequence_matches([1, 2, 3, 4], [1, {2, 3}, 4])
    check_sequence_matches([1, 3, 2, 4], [1, {2, 3}, 4])
    with pytest.raises(AssertionError):
        check_sequence_matches([1, 2, 4, 3], [1, {2, 3}, 4])
