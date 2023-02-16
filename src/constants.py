"""
Static values used by oCLI
"""
# App
VERSION = '0.0.1'
APP_NAME = 'odoo-cli'
DEF_STRUCTURE_YML = 'default.yml'
TAB_SIZE = 4 # Number of space chars composing a Tab

# Odoo
SUPPORTED_ODOO_VERSIONS = ['15.0', '16.0']
DEF_ODOO_VERSION = '16.0'
DEF_ODOO_REPO = 'https://github.com/odoo/odoo.git'
ODOO_SHALLOW = True

# Project Structure

# !!! The order of elements in this list is important.
#     E.g. Odoo repo has to cloned before dockerfile is created.
EXPECTED_KEY_PATHS = [
    'odoo',
    'custom_addons',
    'docker',
    'docker_file',
    'docker_compose',
    'env_file',
    'odoo_conf'
]

DEF_PROJECT_STRUCTURE = {
    'odoo': {
        'type': 'dir',
        'repo': 'https://github.com/odoo/odoo.git',
        'key': 'odoo'
    },
    'addons': {
        'type': 'dir',
        'key': 'custom_addons'
    },
    'conf': {
        'type': 'dir',
        'childs': {
            'odoo.conf': {
                'type': 'file',
                'key': 'odoo_conf'
            }
        }
    },
    'data': {
        'type': 'dir',
        'childs': {
            'db_data': {
                'type': 'dir'
            },
            'odoo_data': {
                'type': 'dir'
            }
        }
    },
    '.env': {
        'type': 'file',
        'key': 'env_file'
    },
    '.ocli.conf': {
        'type': 'file'
    },
    'docker': {
        'type': 'dir',
        'key': 'docker',
        'childs': {
            'DOCKERFILE': {
                'type': 'file',
                'key': 'docker_file'
            }
        }
    },
    'docker-compose.yml': {
        'type': 'file',
        'key': 'docker_compose'
    }
}
