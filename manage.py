#!/usr/bin/env python
import os, sys
import app

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfg.settings")

    sys.dont_write_bytecode = True
    
    from django.core.management import execute_from_command_line
    app.tools.ManagementExtra(sys.argv).execute()
