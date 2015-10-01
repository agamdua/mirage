# -*- coding: utf-8 -*-
from __future__ import print_function

"""
$ py.test
"""

import pytest

from mirage.assign import Repo
from mirage.query import filter_pulls


try:
    from mirage.config import ORG, REPO
except ImportError:
    raise ImportError(
        "This test looks for a repository defined in the format of"
        " '<organization>/<reponame>' in a file called cred.py in the mirage"
        " project. No one said its production ready yo ;)\n"
        "You should also know that the github looks to auth with my username"
        ": thats pretty silly IMO. I want to sleep for now though."
    )

repo = Repo('agamdua', "{}/{}".format(ORG, REPO))

@pytest.fixture()
def input_data():
    return [
    (['L2'], True), ([], False), (['!L2'], False), (['!L2'], True)
]


def test_filters(input_data):
    for data in input_data:
        output = filter_pulls(
            repo, repo.repo.iter_pulls(), labels=data[0], assigned=data[1]
        )

        print(
            "Numbers {} satisfy labels: {} and assigned: {}".format(
                [pull.number for pull in output], data[0], data[1]
            )
        )

if __name__ == '__main__':
    test(input_data)
