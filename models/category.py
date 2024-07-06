from config.db import meta

categories = meta.tables['categories']

print(">>>>>> table categories <<<<<<")
print(categories.columns._all_columns)



