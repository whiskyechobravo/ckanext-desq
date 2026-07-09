import re

from ckan.lib import i18n
from ckan.lib.helpers import get_organization, get_translated, url_for
from ckan.model import Package
from natsort import humansorted

from ckanext.scheming.helpers import (
    scheming_field_by_name,
    scheming_field_choices,
    scheming_get_dataset_schema,
    scheming_language_text,
)


def get_license(license):
    return Package.get_license_register().get(license, license)


def get_dataset_field_choices(field_name):
    fields = scheming_get_dataset_schema("dataset")["dataset_fields"]
    field = scheming_field_by_name(fields, field_name)
    if field:
        return scheming_field_choices(field)


def get_organization_title(organization):
    """Return the organization's translated name, including the abbreviation if applicable."""
    title = get_translated(organization, "title").strip() or organization.get(
        "name", ""
    )
    title_abbr = get_translated(organization, "title_abbr").strip()
    if title_abbr:
        return f"{title} ({title_abbr})"
    return title


def get_organization_abbr_or_title(organization):
    """Return the organization's translated abbreviation, if available, otherwise return its name."""
    title_abbr = get_translated(organization, "title_abbr").strip()
    if title_abbr:
        return title_abbr
    return get_translated(organization, "title").strip() or organization.get("name", "")


def get_citation(data_dict):
    product = []
    if data_dict.get("product_number"):
        product.append(data_dict.get("product_number"))
    if get_translated(data_dict, "product_part"):
        product.append("({})".format(get_translated(data_dict, "product_part")))
    product = " ".join(product)

    url = url_for(
        data_dict.get("type", "") + ".read", id=data_dict.get("id", ""), _external=True
    )

    org = get_organization(data_dict.get("organization", {}).get("id", ""))
    if org:
        org = get_organization_title(org)
    else:
        org = ""

    # Format the citation, replacing %(product)s, %(date)s, %(org)s, %(url)s.
    # Not using % string formatting to make this more tolerant of missing values or incorrect format strings.
    citation = get_translated(data_dict, "citation").strip()
    if product:
        citation = citation.replace("%(product)s", str(product))
    if year := data_dict.get("census_year"):
        citation = citation.replace("%(date)s", str(year))
    if org:
        citation = citation.replace("%(org)s", str(org))
    if url:
        citation = citation.replace("%(url)s", str(url))
    return citation


def is_field_empty(data_dict, field):
    """Check if a field is empty. Works with translatable fields."""
    field_data = data_dict.get(field.get("field_name", ""))
    if not field_data:
        return True
    if (
        re.match("^fluent_", field.get("form_snippet", ""))
        and not scheming_language_text(field_data).strip()
    ):
        return True
    return False


def dataset_sort_variables(data_dict):
    """
    Alter the data_dict to sort dataset variables by name, for the current language.

    This is totally specific to the dataset 'variable' field!
    """
    if "variable" not in data_dict:
        return
    language = i18n.get_lang()

    def key_func(item):
        return item.get("variable_name", {}).get(language, "")

    data_dict["variable"] = humansorted(data_dict["variable"], key=key_func)
    return data_dict
