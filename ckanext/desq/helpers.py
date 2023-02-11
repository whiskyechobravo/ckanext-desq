from ckan.model import Package


def get_licence(licence):
    return Package.get_license_register().get(licence, licence)
