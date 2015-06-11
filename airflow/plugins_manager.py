import imp
import inspect
import logging
import os

from airflow.configuration import conf


plugins_folder = conf.get('core', 'plugins_folder')
if not plugins_folder:
    plugins_folder = conf.get('core', 'airflow_home') + '/plugins'

plugin_modules = []
# Crawl through the plugins folder to find pluggable_classes
for root, dirs, files in os.walk(plugins_folder):
    for f in files:
        try:
            filepath = os.path.join(root, f)
            if not os.path.isfile(filepath):
                continue
            mod_name, file_ext = os.path.splitext(
                os.path.split(filepath)[-1])
            if file_ext != '.py':
                continue
            m = imp.load_source(mod_name, filepath)
            print str(filepath)
            plugin_modules.append(m)
        except Exception() as e:
            logging.exception(e)
            logging.error('Failed to import plugin ' + filepath)

def get_plugins(baseclass):
    # Late Imports to aoid circular imort
    plugins = []
    for obj in m.__dict__.values():
        if (
                inspect.isclass(obj) and issubclass(obj, baseclass) and
                obj is not baseclass):
            plugins.append(obj)
    return plugins
