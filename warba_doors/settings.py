"""Compatibility shim for settings.

This module preserves the original import path `warba_doors.settings` so existing
deployments and migrations continue to work. It delegates to the split settings
under `config.settings` based on the `DJANGO_ENV` environment variable.

Allowed DJANGO_ENV values: 'development' (default), 'production'.
"""

import importlib
import os

env = os.environ.get('DJANGO_ENV', 'development')
module_name = f'config.settings.{env}'

try:
    module = importlib.import_module(module_name)
except Exception:
    # Fallback to development if import fails to avoid breaking local runs
    module = importlib.import_module('config.settings.development')

# Export all uppercase attributes from selected settings module into this namespace
for key in dir(module):
    if key.isupper():
        globals()[key] = getattr(module, key)

