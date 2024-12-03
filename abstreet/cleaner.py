import pandas as pd

def cleanRooster(df):
    df = df[df['location'].str.contains('REC')]
    df['start_time'] = df['lesson_time'].str.split(' - ').str[0]
    df['end_time'] = df['lesson_time'].str.split(' - ').str[1]
    df['day'] = pd.to_datetime(df['date']).dt.day_name()

    df = df.drop_duplicates()

    df['location'] = df['location'].str[:5]

    # recode each location value by dict
    dict = {
        'REC J': 'REC_J/K',
        'REC C': 'REC_ABC',
        'REC V': 'REC_V',
        'REC A': 'REC_ABC',
        'REC B': 'REC_ABC',
        'REC E': 'REC_E',
        'REC M': 'REC_M',
        'REC G': 'REC_G',
        'REC L': 'REC_LAB',
    }

    df['location'] = df['location'].replace(dict)
    # drop any rows where location is not in dict
    df = df[df['location'].isin(dict.values())]

    return df
