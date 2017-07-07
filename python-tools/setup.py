from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(build_exe = "./build/combo", packages = ["idna","queue"], excludes = [], silent=True)

base = 'Console'

executables = [
    Executable('trello_export.py', base=base),
    Executable('add_to_trello.py', base=base)
]

setup(name='trelloExport',
      version = '1',
      description = 'exporter',
      options = dict(build_exe = buildOptions),
      executables = executables)
