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

    for label in label_names:
        if label.startswith('!'):
            label_filters.append(lambda x: x.name != label)
        else:
            label_filters.append(lambda x: x.name == label)

    return label_filters


def satisfies(iterfunc, iterable):
    # if both lists are empty its a no-op and we return true
    if [] == iterable == iterfunc:
        return True

    # even one match is sufficient
    return any(
        func(item) for item in iterable for func in iterfunc
    )


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

    return filtered
