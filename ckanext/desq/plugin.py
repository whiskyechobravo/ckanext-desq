"""Plugin interfaces definitions."""

from ckan import plugins
from ckan.plugins import toolkit

from ckanext.desq import validators as desq_validators


class DesqPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IFacets)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'desq')

    # IValidators
    # Guide: https://docs.ckan.org/en/2.9/extensions/adding-custom-fields.html#custom-validators

    def get_validators(self):
        return {
            'desq_is_year': desq_validators.is_year,
        }

    # IFacets
    # Reference: https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html?highlight=ifacet#ckan.plugins.interfaces.IFacets

    def dataset_facets(self, facets_dict, package_type):
        """Modify and return the facets_dict for the dataset search page."""
        facets_dict['year'] = toolkit._('Year')
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        """Modify and return the facets_dict for a group’s page."""
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        """Modify and return the facets_dict for an organization’s page."""
        return facets_dict
