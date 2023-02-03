"""Custom validators for DESQ."""

from ckan.common import _
from ckan.logic.validators import int_validator, is_positive_integer
from ckan.plugins.toolkit import Invalid


def is_year(value, context):
    value = int_validator(value, context)
    if value is not None:
        if value < 1900:
            raise Invalid(_("Must be greater than 1900"))
        if value > 2100:
            raise Invalid(_("Must be less than 2100"))
    return value
