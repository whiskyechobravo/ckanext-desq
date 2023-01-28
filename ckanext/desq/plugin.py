"""Plugin interfaces definitions."""

from ckan import plugins
from ckan.plugins import toolkit

from ckanext.desq import validators as desq_validators


class DesqPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IDatasetForm)
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
            'is_year': desq_validators.is_year,
        }

    # IDatasetForm
    # Guide: https://docs.ckan.org/en/2.9/extensions/adding-custom-fields.html

    def _modify_package_schema(self, schema):
        schema.update({
            'year': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_validator('is_year'),
                toolkit.get_converter('convert_to_extras'),
            ]
        })
        return schema

    def create_package_schema(self):
        """Return the schema for validating new dataset dicts."""
        schema = super().create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        """Return the schema for validating updated dataset dicts."""
        schema = super().update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        """Return a schema to validate datasets before they’re shown to the user."""
        schema = super().show_package_schema()
        schema.update({
            'year': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing'),
            ]
        })
        return schema

    def is_fallback(self):
        """Return True if this plugin is the fallback plugin."""
        # This plugin is the default handler for package types not handled by
        # any other IDatasetForm plugin.
        return True

    def package_types(self):
        """Return an iterable of dataset (package) types that this plugin handles."""
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above)
        return []

    # IFacets
    # Reference: https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html?highlight=ifacet#ckan.plugins.interfaces.IFacets

    def dataset_facets(self, facets_dict, package_type):
        """Modify and return the facets_dict for the dataset search page."""
        facets_dict['year'] = toolkit._('Year')
        return facets_dict
