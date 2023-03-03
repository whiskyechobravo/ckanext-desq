"""Custom Jinja2 filters."""

from jinja2.filters import environmentfilter, ignore_case, make_attrgetter
from natsort import humansorted


@environmentfilter
def do_humansort(
    environment, value, reverse=False, case_sensitive=False, attribute=None
):
    """Replicates Jinja's `sort` filter, but with `humansorted`."""
    key_func = make_attrgetter(
        environment, attribute,
        postprocess=ignore_case if not case_sensitive else None
    )
    return humansorted(value, key=key_func, reverse=reverse)


def do_dicthumansort(value, case_sensitive=False, by='key', reverse=False):
    """Replicates Jinja's `dictsort` filter, but with `humansorted`."""
    if by == 'key':
        pos = 0
    elif by == 'value':
        pos = 1
    else:
        raise FilterArgumentError(
            'You can only sort by either "key" or "value"'
        )

    def sort_func(item):
        value = item[pos]

        if not case_sensitive:
            value = ignore_case(value)

        return value

    return humansorted(value.items(), key=sort_func, reverse=reverse)
