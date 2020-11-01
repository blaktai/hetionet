import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def create_dictionary(df, filter):
    dict = df[df['kind'] == filter]
    del dict['kind']
    return df.set_index('id')['name'].to_dict()

