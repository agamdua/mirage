"""
Design notes & future API changes
=================================

This is an incredibly clever module. There may or may not be pride while
writing that little confession.

These functions are independent of a class right now, this is to eliminate
dependency of the functionality on the ``repo`` object.

At the moment though, we still use the ``repo`` object, and it will be changed
once the switch to ``github3.py>=1.0.0``  is complete. In the meanwhile,
expect the API to change rapidly without any concern for anything dependent
on this code.
"""
from functools import partial


def filter_by_label(label_names=None):
    """Returns a list of callables that can be applied as label filters

    Supports (limited) querying.

    Returns:
        - [] if label_names is None
        - list of label filters as callables

    Example:
        label_names = ['mylabel', '!not-my-label']

        will get the pull requests with `mylabel`, but not the ones
        with `not-my-label`
    """
    if label_names is None:
        return []

    label_filters = []

    def not_label(x, label):
        return x.name != label.split('!')[-1]

    def has_label(x, label):
        return x.name == label

    for label in label_names:
        if label.startswith('!'):
            fn = partial(not_label, label=label)
            fn.__name__ = "not_label_{}".format(label.split('!')[-1])
        else:
            fn = partial(has_label, label=label)
            fn.__name__ = "has_label_{}".format(label)

        fn.__doc__ = "filter for {}".format(label)
        label_filters.append(fn)

    return label_filters


def actually_filter_by_labels(iterfunc, iterable):
    if [] == iterfunc or [] == iterable == iterfunc:
        return True

    import mock
    if not iterable:
        # yeah, this just happened.
        iterable = [mock.Mock()]

    decided = []

    for fn in iterfunc:
        decider = all if fn.__name__.startswith('not_') else any
        decided.append(decider(map(fn, iterable)))

    return all(decided)


def satisfies(iterfunc, iterable):
    # if both lists are empty its a no-op and we return true
    if [] == iterfunc or [] == iterable == iterfunc:
        return True

    import mock
    if not iterable:
        # TODO: yeah, this just happened.
        iterable = [mock.Mock()]

    decided = []
    for fn in iterfunc:
        decider = all if fn.__name__.startswith('not_') else any
        decided.append(decider(map(fn, iterable)))

    return all(decided)


def filter_pulls(repo, pulls, assigned=None, state='open', labels=None):
    """
    Returns a list based on filters

    Args:
        pulls (iterable of pull request objects)
        assigned (bool or None): assigned to nobody or assigned to somebody
            True returns all that are assigned
        state (str): 'all', 'open', 'closed' (mirroring github3 api)
        labels (iterable)

    TODOs:
        - assigned needs to support specific assignees
        - only supports open pull requests
    """
    filtered = []
    issue_filters = []

    # TODO: filter by specific assignees
    if assigned:
        issue_filters.append(lambda x: x.assignee)
    else:
        issue_filters.append(lambda x: not x.assignee)

    if state != 'open':
        raise NotImplementedError(
            "Feel free to contribute to github.com/agamdua/mirage!"
        )

    if labels is not None:
        label_filters = filter_by_label(labels)
    else:
        label_filters = []

    for pull in pulls:
        if all([
            satisfies(label_filters, repo.repo.issue(pull.number).labels),
            satisfies(issue_filters, [pull])
        ]):
            filtered.append(pull)

    # TODO: do we want to actually yield here; can actually reuse the github3.py
    # iterator for pull requests
    return filtered
