import pandas as pd

data = {
    "user": ["Alice", "Bob", "Alice", "Bob", "Charlie"],
    "action": ["login", "login", "logout", "logout", "login"]
}

df = pd.DataFrame(data)
print(df)
# Nombre d'utilisateurs uniques
print(df['user'].nunique())
