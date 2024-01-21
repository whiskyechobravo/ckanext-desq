"""Plugin interfaces definitions."""

import json
from collections import OrderedDict

from ckan import plugins
from ckan.lib.plugins import DefaultTranslation
from ckan.lib.search.query import QUERY_FIELDS
from ckan.plugins import toolkit

from ckanext.desq import helpers, jinja
from ckanext.desq import validators as desq_validators
from ckanext.desq.blueprint import blueprint as desq_blueprint


class DesqPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware)
    plugins.implements(plugins.IPluginObserver)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'desq')
        toolkit.add_resource('assets', 'desq')

    # IMiddleware

    def make_middleware(self, app, config):
        app.jinja_env.filters['humansort'] = jinja.do_humansort
        app.jinja_env.filters['dicthumansort'] = jinja.do_dicthumansort
        return app

    def make_error_log_middleware(self, app, config):
        return app

    # IValidators
    # Guide: https://docs.ckan.org/en/2.9/extensions/adding-custom-fields.html#custom-validators

    def get_validators(self):
        return {
            'desq_is_year': desq_validators.is_year,
            'desq_no_future_date': desq_validators.no_future_date,
        }

    # IPluginObserver

    @staticmethod
    def _create_vocabulary(vocabulary_id):
        """Create the specified tag vocabulary if it does not already exists."""
        # Guide: https://docs.ckan.org/en/2.9/extensions/adding-custom-fields.html#tag-vocabularies
        user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        context = {'user': user['name']}
        try:
            data = {'id': vocabulary_id}
            toolkit.get_action('vocabulary_show')(context, data)
        except toolkit.ObjectNotFound:
            data = {'name': vocabulary_id}
            return toolkit.get_action('vocabulary_create')(context, data)

    def before_load(self, plugin):
        pass

    def after_load(self, service):
        # Make sure the required vocabularies exist.
        self._create_vocabulary('dimension')

    def before_unload(self, plugin):
        pass

    def after_unload(self, service):
        pass

    # IFacets
    # Reference: https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IFacets

    def dataset_facets(self, facets_dict, package_type):
        """Modify and return the facets_dict for the dataset search page."""
        # Instead of updating facets_dict, we fully replace it to reorder everything.
        facets_dict = OrderedDict({
            'census_year': toolkit._('Census year'),
            'data_type': toolkit._('Data type'),
            'topic': toolkit._('Topic'),
            'geo_area': toolkit._('Geographical area'),
            'res_format': toolkit._('Format'),
            'language': toolkit._('Language of dataset'),
            'license': toolkit._('License'),
            'organization': toolkit._('Contributing DESQ Partners'),
        })
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        """Modify and return the facets_dict for a group’s page."""
        facets_dict = OrderedDict({
            'census_year': toolkit._('Census year'),
            'data_type': toolkit._('Data type'),
            'topic': toolkit._('Topic'),
            'geo_area': toolkit._('Geographical area'),
            'res_format': toolkit._('Format'),
            'language': toolkit._('Language of dataset'),
            'license': toolkit._('License'),
        })
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        """Modify and return the facets_dict for an organization’s page."""
        return facets_dict

    # ITemplateHelpers
    # Reference: https://docs.ckan.org/en/2.9/extensions/adding-custom-fields.html?highlight=get_helpers#adding-tags-to-templates

    def get_helpers(self):
        return {
            'desq_get_license': helpers.get_license,
            'desq_dataset_field_choices': helpers.get_dataset_field_choices,
            'desq_dataset_sort_variables': helpers.dataset_sort_variables,
            'desq_organization_title': helpers.get_organization_title,
            'desq_organization_abbr_or_title': helpers.get_organization_abbr_or_title,
            'desq_is_field_empty': helpers.is_field_empty,
        }

    # IPackageController
    # Reference: https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IPackageController

    def read(self, entity):
        """Called after IPackageController.before_view inside package_show."""
        pass

    def create(self, entity):
        """Called after the dataset had been created inside package_create."""
        pass

    def edit(self, entity):
        """Called after the dataset had been updated inside package_update."""
        pass

    def delete(self, entity):
        """Called before commit inside package_delete."""
        pass

    def after_create(self, context, pkg_dict):
        """
        Extensions will receive the validated data dict after the dataset
        has been created (Note that the create method will return a dataset
        domain object, which may not include all fields). Also the newly
        created dataset id will be added to the dict.
        """
        pass

    def after_update(self, context, pkg_dict):
        """
        Extensions will receive the validated data dict after the dataset
        has been updated.
        """
        pass

    def after_delete(self, context, pkg_dict):
        """
        Extensions will receive the data dict (typically containing
        just the dataset id) after the dataset has been deleted.
        """
        pass

    def after_show(self, context, pkg_dict):
        """
        Extensions will receive the validated data dict after the dataset
        is ready for display.
        """
        pass

    def before_search(self, search_params):
        """
        Extensions will receive a dictionary with the query parameters,
        and should return a modified (or not) version of it.

        search_params will include an `extras` dictionary with all values
        from fields starting with `ext_`, so extensions can receive user
        input from specific fields.
        """
        # Add and boost the product_number field to list of query fields.
        search_params['qf'] = f"{QUERY_FIELDS} product_number^32"
        return search_params

    def after_search(self, search_results, search_params):
        """
        Extensions will receive the search results, as well as the search
        parameters, and should return a modified (or not) object with the
        same structure::

            {'count': '', 'results': '', 'facets': ''}

        Note that count and facets may need to be adjusted if the extension
        changed the results for some reason.

        search_params will include an `extras` dictionary with all values
        from fields starting with `ext_`, so extensions can receive user
        input from specific fields.
        """
        return search_results

    def before_index(self, data_dict):
        """
        Process data before passing it to Solr.

        Extensions will receive what will be given to Solr for
        indexing. This is essentially a flattened dict (except for
        multi-valued fields such as tags) of all the terms sent to
        the indexer. The extension can modify this by returning an
        altered version.
        """

        # Index language-specific fields.
        data_dict['sort_title'] = json.loads(data_dict.get('title_translated', {})).get('en', "")
        data_dict['sort_title_fr'] = json.loads(data_dict.get('title_translated', {})).get('fr', "")

        def get_choice_value_label(choices, value, language='en'):
            for choice in choices:
                if choice.get('value') == value:
                    return choice.get('label', {}).get(language, '')

        def get_select_text(data_dict, field_name, language='en'):
            choices = helpers.get_dataset_field_choices(field_name)
            value = data_dict.get(field_name, '')
            return get_choice_value_label(choices, value, language)

        def get_multiselect_text(data_dict, field_name, language='en'):
            choices = helpers.get_dataset_field_choices(field_name)
            values = json.loads(data_dict.get(field_name, '[]'))
            return [get_choice_value_label(choices, value, language) for value in values]

        # Prepare text corresponding to each facet value.
        data_dict['choices_data_type'] = get_select_text(data_dict, 'data_type', 'en')
        data_dict['choices_data_type_fr'] = get_select_text(data_dict, 'data_type', 'fr')
        data_dict['choices_topic'] = get_multiselect_text(data_dict, 'topic', 'en')
        data_dict['choices_topic_fr'] = get_multiselect_text(data_dict, 'topic', 'fr')
        data_dict['choices_geo_area'] = get_multiselect_text(data_dict, 'geo_area', 'en')
        data_dict['choices_geo_area_fr'] = get_multiselect_text(data_dict, 'geo_area', 'fr')
        data_dict['choices_language'] = get_multiselect_text(data_dict, 'language', 'en')
        data_dict['choices_language_fr'] = get_multiselect_text(data_dict, 'language', 'fr')

        # Prepare faceting values from multiple-select fields.
        data_dict['topic'] = json.loads(data_dict.get('topic', '[]'))
        data_dict['geo_area'] = json.loads(data_dict.get('geo_area', '[]'))
        data_dict['language'] = json.loads(data_dict.get('language', '[]'))

        # TODO: Remove the scheming_nerf_index plugin, and handle repeating subfields properly.
        # References:
        # - https://github.com/ckan/ckanext-scheming#repeating_subfields
        # - https://ckan.org/blog/scheming-subfields

        return data_dict

    def before_view(self, data_dict):
        """
        Extensions will receive this before the dataset gets
        displayed. The dictionary passed will be the one that gets
        sent to the template.
        """
        return data_dict

    # IBlueprint

    def get_blueprint(self):
        return desq_blueprint
