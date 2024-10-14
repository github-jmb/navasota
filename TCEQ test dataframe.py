import pandas as pd
import os

directory = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(directory, 'swqmispublicdata.txt')

df = pd.read_csv(filepath, delimiter='|')
grouped = df.groupby('Station ID')

for segment_id, group in grouped:
    filename = f'segment_{segment_id}.xlsx'
    full_path = os.path.join(directory, filename)
    
    group.to_excel(filename, index=False)

    print(f'Saved: {full_path}')