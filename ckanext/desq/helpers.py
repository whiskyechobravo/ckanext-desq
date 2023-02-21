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
