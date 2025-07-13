import pandas as pd
from fastapi_app.preprocessing.extrac_features import extract_features
def clean_data(df):
    df["length_text"] = df["text"].apply(len)
    df["length_title"] = df["title"].apply(len)

    df['text_title_length_relation'] = df.apply(
        lambda row: row['length_text'] / row['length_title'] if row['length_title'] != 0 else 0, axis=1
    )

    features_df = df.apply(lambda row: extract_features(row['text'], row['title']), axis=1, result_type='expand')

    df = pd.concat([df, features_df], axis=1)
    df = df.drop(columns=['title', 'text', 'subject', 'date', 'label'])
    df = df.dropna()
    return df