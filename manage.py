#!/usr/bin/env python
import os, sys
import app.tools

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfg.settings")
    sys.dont_write_bytecode = True
    app.tools.ManagementExtra(sys.argv).execute()
