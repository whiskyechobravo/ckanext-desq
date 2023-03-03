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


def get_organization_title(organization):
    """Return the organization's translated name, including the abbreviation if applicable."""
    title = get_translated(organization, 'title').strip() or organization.get('name', '')
    title_abbr = get_translated(organization, 'title_abbr').strip()
    if title_abbr:
        return f"{title} ({title_abbr})"
    return title


def get_organization_abbr_or_title(organization):
    """Return the organization's translated abbreviation, or available, otherwise return its name."""
    title_abbr = get_translated(organization, 'title_abbr').strip()
    if title_abbr:
        return title_abbr
    return get_translated(organization, 'title').strip() or organization.get('name', '')
