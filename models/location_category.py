from config.db import meta

location_category_reviewed = meta.tables['location_category_reviewed']

print(">>>>>> table location category reviewed <<<<<<")
print(location_category_reviewed.columns._all_columns)
