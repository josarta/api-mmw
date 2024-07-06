from config.db import meta

locations = meta.tables['locations']

print(">>>>>> table locations <<<<<<")
print(locations.columns._all_columns)
