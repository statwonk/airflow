import logging

from airflow.configuration import conf

from airflow.executors.local_executor import LocalExecutor
from airflow.executors.celery_executor import CeleryExecutor
from airflow.executors.sequential_executor import SequentialExecutor
from airflow.executors.base_executor import BaseExecutor


_EXECUTOR = conf.get('core', 'EXECUTOR')

if _EXECUTOR == 'LocalExecutor':
    DEFAULT_EXECUTOR = LocalExecutor()
elif _EXECUTOR == 'CeleryExecutor':
    DEFAULT_EXECUTOR = CeleryExecutor()
elif _EXECUTOR == 'SequentialExecutor':
    DEFAULT_EXECUTOR = SequentialExecutor()
elif _EXECUTOR in globals():
    DEFAULT_EXECUTOR = globals()[_EXECUTOR]
else:
    # Loading plugins
    from airflow.plugins_manager import get_plugins
    executor_plugins = {}
    for _plugin in get_plugins(BaseExecutor):
        globals()[_plugin.__name__] = _plugin
    raise Exception("Executor {0} not supported.".format(_EXECUTOR))

logging.info("Using executor " + _EXECUTOR)
