# ckanext-desq

Customizations for DESQ. This CKAN plugin is *not* designed to be generic or
easily applicable to other data portals.


## Requirements

- Python 3.9
- Ubuntu packages required by PyICU:
  ```bash
  sudo apt install libicu-dev python3-icu pkg-config
  ```
- CKAN 2.9.5 fork, installed with:
  ```bash
  pip install -e 'git+https://github.com/whiskyechobravo/ckan.git@desq-2.9.5#egg=ckan[requirements]'
  ```

Tested under Ubuntu 20.04 and 22.04.


## Installation

1. Activate your CKAN virtualenv, for example:
   ```bash
   . /usr/lib/ckan/default/bin/activate
   ```

2. Install ckanext-desq in the virtualenv:
   ```bash
   pip install -e 'git+https://github.com/whiskyechobravo/ckanext-desq.git#egg=ckanext-desq'
   ```

   That will also install some dependencies (listed in `ckanext-desq/setup.cfg`).

3. Use `config/ckan/sample.ini` as a replacement to
   `/etc/ckan/default/ckan.ini`, but edit the following settings:

    - `beaker.session.secret`
    - `sqlalchemy.url`
    - `api_token.jwt.encode.secret`
    - `api_token.jwt.decode.secret`
    - `solr_url`
    - `solr_user`
    - `solr_password`
    - `licenses_group_url` (must link to `ckanext-desq/config/ckan/licenses.json`)
    - `ckan.storage_path` (if need to change from `/var/lib/ckan/default`)

4. Copy the required webfonts to the `ckanext/desq/public/webfonts/` directory.

5. Restart CKAN. Assuming it's installed as a systemd service:
   ```bash
   sudo service ckan restart
   ```


## Performing manual backup and restore

References:
- https://docs.ckan.org/en/2.9/maintaining/database-management.html#import-and-export
- https://docs.ckan.org/en/2.9/maintaining/cli.html#search-index-rebuild-search-index

Backup:

```bash
sudo -u postgres pg_dump --format=custom -d ckan_default > desq-$(date +%Y%m%d-%H%M).pgdump
```

Restore (replace path to `.ini` file if necessary):

```bash
ckan -c /etc/ckan/default/ckan.ini db clean
sudo -u postgres pg_restore --clean --if-exists -d ckan_default < desq-YYYYMMDD-HHMM.pgdump
ckan -c /etc/ckan/default/ckan.ini search-index rebuild
```


## Managing translations

References:
- https://docs.ckan.org/en/2.9/contributing/i18n.html
- https://docs.ckan.org/en/2.9/extensions/translating-extensions.html

Creating the `.pot` file:

```bash
python setup.py extract_messages
```

Creating a `.po` file for a locale:

```bash
python setup.py init_catalog --locale LANG
```

Updating existing translations:

```bash
python setup.py update_catalog --locale LANG
```

Compile translations into a `.mo` file:

```bash
python setup.py compile_catalog --locale LANG
```

The binary `.mo` file is commited to the repository for ease of deployment.
