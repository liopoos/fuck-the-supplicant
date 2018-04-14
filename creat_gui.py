from distutils.core import setup
import py2exe

options = {"py2exe": {"compressed": 1,
                      "optimize": 2,
                      "bundle_files": 1
                      }
           }

setup(
    windows=[{"script": "main.py",
              "icon_resources": [(1, "app.ico")]
              }],
    options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}},
    data_files=[("", ["app.ico"])],
    version="0.1.0",
    description="Hey! let's fuck the supplicant.",
    name="FTsupplicant",

)
