import logging
from airflow.configuration import conf

__version__ = "1.0.1"

'''
Authentication is implemented using flask_login and different environments can
implement their own login mechanisms by providing an `airflow_login` module
in their PYTHONPATH. airflow_login should be based off the
`airflow.www.login`
'''

class PluginView(object):
    @classmethod
    def get_views(self):
        raise NotImplemented("Derive me")

from models import DAG
