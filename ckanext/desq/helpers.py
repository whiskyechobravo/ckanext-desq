from ckan.lib.helpers import get_translated
from ckan.model import Package

from ckanext.scheming.helpers import (scheming_field_by_name,
                                      scheming_field_choices,
                                      scheming_get_dataset_schema)


def get_license(license):
    return Package.get_license_register().get(license, license)


def get_dataset_field_choices(field_name):
    fields = scheming_get_dataset_schema('dataset')['dataset_fields']
    field = scheming_field_by_name(fields, field_name)
    if field:
        return scheming_field_choices(field)


def get_full_organization_title(organization):
    """Return the translated organization name, including the abbreviation if applicable."""
    title = get_translated(organization, 'title') or organization.get('name', '')
    title_abbr = get_translated(organization, 'title_abbr')
    if title_abbr:
        return f"{title} ({title_abbr})"
    return title
