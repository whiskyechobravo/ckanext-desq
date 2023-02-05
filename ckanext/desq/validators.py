"""Custom validators for DESQ."""

from datetime import datetime
from itertools import count

from ckan.common import _
from ckan.logic.validators import (int_validator, is_positive_integer,
                                   tag_length_validator, tag_name_validator)
from ckan.plugins.toolkit import Invalid


def is_year(value, context):
    value = int_validator(value, context)
    if value is not None:
        if value < 1900:
            raise Invalid(_("Must be greater than 1900"))
        if value > 2100:
            raise Invalid(_("Must be less than 2100"))
    return value


def no_future_date(key, data, errors, context):
    value = data.get(key)
    if value and value > datetime.today():
        raise Invalid(_("Date may not be in the future."))
    return value
