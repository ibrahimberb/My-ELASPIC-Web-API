import pandas as pd

data = pd.DataFrame({'A': [1, 2, 3],
                     'B': [4, 5, 6],
                     'C': [7, 8, 9]}).set_index('A')
# print(data)
print(data.loc[2, 'C'])
