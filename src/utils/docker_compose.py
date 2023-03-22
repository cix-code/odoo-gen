"""
DockerCompose file generator class
"""

import yaml

from ..constants import DEF_DOCKER_COMPOSE_VERSION
from ..constants import DEF_PSQL_VERSION
from .helper import generate_password


class DockerCompose:  # pylint: disable=too-few-public-methods
    """
    DockerCompose file generator class
    """

    compose: dict
    key_paths: dict
    pg_pass: str
    network_name: str

    def __init__(self, key_paths: dict, project_name: str):
        self.key_paths = key_paths
        self.network_name = f'net_{project_name}'

        self.compose = {
            'version': DEF_DOCKER_COMPOSE_VERSION,
            'services': {}
        }

    def _rel_path(self, path_key):
        project_path = self.key_paths.get('project', '')
        return self.key_paths.get(path_key, '').replace(project_path, '.')

    def _add_service(self, serv:dict) -> None:
        self.compose['services'].update(serv)

    def _set_db(self) -> None:

        db_data_path = self._rel_path('db_data')

        self.pg_pass = generate_password()

        db_config = {
            'image': f'postgres:{DEF_PSQL_VERSION}',
            'volumes': [
                f'{db_data_path}:/var/lib/postgresql/data'
            ],
            'env_file': ['.env'],
            'networks': [
                self.network_name
            ],
        }
        self._add_service({'db': db_config})

    def _set_odoo(self) -> None:
        dockerfile_path = self._rel_path('docker_file')
        custom_addons_path = self._rel_path('custom_addons')
        conf_dir_path = self._rel_path('conf_dir')
        odoo_path = self._rel_path('odoo')
        odoo_data_path = self._rel_path('odoo_data')

        odoo_config = {
            'build': {
                'context': '.',
                'dockerfile': dockerfile_path
            },
            'volumes': [
                f'{custom_addons_path}:/mnt/addons',
                f'{odoo_path}:/mnt/odoo',
                f'{odoo_data_path}:/var/lib/odoo',
                f'{conf_dir_path}:/etc/odoo/',
            ],
            'env_file': ['.env'],
            'ports': [
                '8069:8069',
                '8071:8071',
                '8072:8072',
            ],
            'depends_on': ['db'],
            'networks': [
                self.network_name
            ]
        }

        self._add_service({'odoo': odoo_config})

    def _set_network(self):
        network_config = {
            self.network_name: {
                'external': 'true',
                'name': self.network_name
            }
        }

        self.compose.update({'networks': network_config})

    def get_content(self) -> str:
        """
        Aggregates and returns the content of the dockerfile based on specific Odoo version

        Returns:
            str: Content of the dockerfile
        """
        self._set_db()
        self._set_odoo()
        self._set_network()

        return yaml.dump(self.compose)
