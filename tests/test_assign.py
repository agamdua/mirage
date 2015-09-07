from __future__ import print_function

from collections import Counter

from mirage.assign import Repo, assign_pulls
from mirage.config import FIRST_REVIEWS, ORG, REPO, FINAL_PASS

repo = Repo('agamdua', "{}/{}".format(ORG, REPO))


def test_assignment():
    """This is going to actually assign things
    """
    # raise NotImplementedError
    assign_pulls(repo=repo, labels=['!L2'], reviewers=FIRST_REVIEWS)
    assign_pulls(repo=repo, labels=['L2'], reviewers=FINAL_PASS)
