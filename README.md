# ckanext-desq

Customizations for DESQ. This CKAN plugin is *not* designed to be generic or
easily applicable to other data portals.


## Requirements

Tested with the following CKAN 2.9 fork:
https://github.com/whiskyechobravo/ckan/tree/desq-2.9.5


## Installation

1. Activate your CKAN virtualenv, for example:
   ```bash
   . /usr/lib/ckan/default/bin/activate
   ```

2. Install ckanext-desq in the virtualenv:
   ```bash
   pip install -e 'git+https://github.com/whiskyechobravo/ckanext-desq.git#egg=ckanext-desq'
   ```

   **TODO:** Specify `[requirements]` if `requirements.txt` is not empty.

3. Add `desq` to the `ckan.plugins` setting in your CKAN
   config file, e.g., `/etc/ckan/default/ckan.ini`.

4. Restart CKAN. Assuming it's installed as a systemd service:
   ```bash
   sudo service ckan restart
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

Compile translations:

```bash
python setup.py compile_catalog --locale LANG
```
