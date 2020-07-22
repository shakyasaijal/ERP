import subprocess

apps_for_migration_folder = []

for i in apps_for_migration_folder:
    subprocess.call(
        'cd {} && mkdir migrations && touch migrations/__init__.py'.format(i.replace("'", '')), shell=True)
