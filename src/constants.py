"""
Static values used by oCLI
"""

VERSION = '0.0.1'
APP_NAME = 'odoo-cli'
DEF_STRUCTURE_YML = 'default.yml'

SUPPORTED_ODOO_VERSIONS = ['15.0', '16.0']
DEF_ODOO_VERSION = '16.0'

DEF_PROJECT_STRUCTURE = {
    'odoo': {
        'type': 'dir',
        'repo': 'https://github.com/odoo/odoo.git',
        'key': 'odoo_dir'
    },
    'addons': {
        'type': 'dir',
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
