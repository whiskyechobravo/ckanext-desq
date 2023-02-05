"""Custom validators for DESQ."""

from datetime import datetime
from itertools import count

from ckan.common import _
from ckan.logic.validators import (int_validator, is_positive_integer,
                                   tag_length_validator, tag_name_validator)
from ckan.plugins.toolkit import Invalid

from ckanext.desq import query


def is_year(value, context):
    value = int_validator(value, context)
    if value is not None:
        if value < 1900:
            raise Invalid(_("Must be greater than 1900"))
        if value > 2100:
            raise Invalid(_("Must be less than 2100"))
    return value


def tag_convert(key, data, errors, context):
    """
    Parse comma-separated tags, validate and add them to the data dict.

    For each tag, a vocabulary id is selected based on the `key` argument.
    """
    # Derived from ckan.logic.validators.tag_string_convert().

    # Note: This assumes that the vocabulary name is the same as the field key!
    vocabulary = query.get_vocabulary_by_name(context, key)

    if isinstance(data[key], str):
        tags = [tag.strip() for tag in data[key].split(',') if tag.strip()]
    else:
        tags = data[key]

    current_index = max([int(k[1]) for k in data.keys() if len(k) == 3 and k[0] == 'tags'] + [-1])

    for num, tag in zip(count(current_index + 1), tags):
        data[('tags', num, 'name')] = tag
        data[('tags', num, 'vocabulary_id')] = vocabulary.id if vocabulary else None

    for tag in tags:
        tag_length_validator(tag, context)
        tag_name_validator(tag, context)


def no_future_date(key, data, errors, context):
    value = data.get(key)
    if value and value > datetime.today():
        raise Invalid(_("Date may not be in the future."))
    return value
