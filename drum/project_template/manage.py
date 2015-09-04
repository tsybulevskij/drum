#!/usr/bin/env python
import os
import sys
import project_name.settings as settings

if __name__ == "__main__":

    # from mezzanine.utils.conf import real_project_name
    # settings_module = "%s.settings" % real_project_name
    # settings_module = "%s.settings" % real_project_name("{{ project_name }}")
    # settings_module = "%s.settings" % settings.PROJECT_DIRNAME
    settings_module = "project_name.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    print settings_module

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
