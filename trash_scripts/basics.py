import pandas as pd

data = pd.DataFrame({'1': 97,
                     '2': 86,
                     '3': 0}, index=['Downloaded_subchunk']).T
data.index.name = 'Chunk'

print(data)

print(data[data['Downloaded_subchunk'] == 0])
