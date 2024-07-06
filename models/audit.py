from config.db import meta

audits = meta.tables['audit']

print(">>>>>> table audit <<<<<<")
print(audits.columns._all_columns)
