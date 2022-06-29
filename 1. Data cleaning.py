import pandas as pd
import numpy as np
import jupyter
import re
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# Importing data
df = pd.read_stata(
    '/Users/laws/Library/Mobile Documents/com~apple~CloudDocs/Cambridge/Part IIB/Dissertation data/Electoral rules/US '
    'towns/DS0001/usdiss.dta')

# Dropping duplicate columns ending in 'F'
df = df[df.columns[~df.columns.str.endswith('F')]]

# Renaming cities which have duplicated names
df['town_id'] = df['STATE1'] + df['PLACE1']

#  Dropping redundant location variables
df.drop(['RECNUM1', 'STATE1', 'STATE2', 'STATE3', 'STATE4', 'STATE5', 'PLACE1', 'AREANAME'],
        axis='columns', inplace=True)

# df.drop(df[df.town_id % 10000 == 0].index, inplace = True)

# Recoding missing values as nan
df.replace(0, np.nan, inplace=True)

# Renaming variables
df.rename(columns={'CC0006': 'popl1930',
                   'CC0007': 'popl1940',
                   'CC0008': 'popl1950',
                   'CC0009': 'popl1960',
                   'CC0010': 'popl1970',
                   'CC0011': 'popl1975',
                   'CC0401': 'gov_rev1942',
                   'CC0402': 'gov_rev1948',
                   'CC0403': 'gov_rev1950',
                   'CC0404': 'gov_rev1955',
                   'CC0405': 'gov_rev1960',
                   'CC0406': 'gov_rev1965',
                   'CC0407': 'gov_rev1970',
                   'CC0408': 'gov_rev1975',
                   'CC0410': 'gov_rev_int1942',
                   'CC0411': 'gov_rev_int1948',
                   'CC0412': 'gov_rev_int1950',
                   'CC0413': 'gov_rev_int1955',
                   'CC0414': 'gov_rev_int1960',
                   'CC0415': 'gov_rev_int1965',
                   'CC0417': 'gov_rev_int1970',
                   'CC0416': 'gov_rev_int1975',
                   'CC0236': 'med_inc1950',
                   'CC0237': 'med_inc1960',
                   'CC0238': 'med_inc1970',
                   'CC0419': 'gov_tx1942',
                   'CC0420': 'gov_tx1948',
                   'CC0421': 'gov_tx1950',
                   'CC0422': 'gov_tx1955',
                   'CC0423': 'gov_tx1960',
                   'CC0424': 'gov_tx1965',
                   'CC0425': 'gov_tx1970',
                   'CC0426': 'gov_tx1975',
                   'CC0446': 'gov_exp_dir1942',
                   'CC0447': 'gov_exp_dir1948',
                   'CC0448': 'gov_exp_dir1950',
                   'CC0449': 'gov_exp_dir1955',
                   'CC0450': 'gov_exp_dir1960',
                   'CC0451': 'gov_exp_dir1965',
                   'CC0452': 'gov_exp_dir1970',
                   'CC0453': 'gov_exp_dir1975',
                   'CC0469': 'gov_exp_educ1948',
                   'CC0470': 'gov_exp_educ1950',
                   'CC0471': 'gov_exp_educ1955',
                   'CC0472': 'gov_exp_educ1960',
                   'CC0473': 'gov_exp_educ1965',
                   'CC0476': 'gov_exp_educ1970',
                   'CC0477': 'gov_exp_educ1975',
                   'CC0478': 'gov_exp_hwy1948',
                   'CC0479': 'gov_exp_hwy1955',
                   'CC0480': 'gov_exp_hwy1960',
                   'CC0481': 'gov_exp_hwy1965',
                   'CC0482': 'gov_exp_hwy1970',
                   'CC0483': 'gov_exp_hwy1975',
                   'CC0484': 'gov_exp_wlf1948',
                   'CC0485': 'gov_exp_wlf1950',
                   'CC0486': 'gov_exp_wlf1960',
                   'CC0487': 'gov_exp_wlf1965',
                   'CC0488': 'gov_exp_wlf1970',
                   'CC0489': 'gov_exp_wlf1975',
                   'CC0490': 'gov_exp_hth_hosp1948',
                   'CC0491': 'gov_exp_hth_hosp1950',
                   'CC0492': 'gov_exp_hth_hosp1960',
                   'CC0493': 'gov_exp_hth_hosp1965',
                   'CC0495': 'gov_exp_swg1948',
                   'CC0496': 'gov_exp_swg1955',
                   'CC0497': 'gov_exp_swg1960',
                   'CC0498': 'gov_exp_swg1970',
                   'CC0499': 'gov_exp_swg1975'}, inplace=True)

# Individual changes
df['gov_exp_swg1965'] = df['CC0494'] + df['CC0500']

# Drop redundant variables
df = df.drop(list(df.filter(regex='CC*')), axis=1, inplace=False)

# Imputing missing populations
df['popl1942'] = ((df['popl1950'] - df['popl1940']) / 5) + df['popl1940']
df['popl1948'] = ((df['popl1950'] - df['popl1940']) * 0.8) + df['popl1940']
df['popl1955'] = ((df['popl1960'] - df['popl1950']) / 2) + df['popl1950']
df['popl1965'] = ((df['popl1970'] - df['popl1960']) / 5) + df['popl1960']

# Transforming populations
df.update(df.filter(regex='popl.*') / 1000)

# list of columns that need to be divided by certain amounts
thousands = ['gov_rev1942', 'gov_rev1948', 'gov_rev1950', 'gov_rev1955', 'gov_rev1960', 'gov_rev1965',
             'popl1942', 'popl1948', 'popl1950', 'popl1955', 'popl1960', 'popl1965', 'popl1970', 'popl1975',
             'gov_tx1942', 'gov_tx1948', 'gov_tx1950', 'gov_tx1955', 'gov_tx1960', 'gov_tx1965',
             'gov_rev_int1942', 'gov_rev_int1948', 'gov_rev_int1950', 'gov_rev_int1955', 'gov_rev_int1960',
             'gov_rev_int1965',
             'gov_exp_dir1942', 'gov_exp_dir1948', 'gov_exp_dir1950', 'gov_exp_dir1955', 'gov_exp_dir1960',
             'gov_exp_dir1965',
             'gov_exp_educ1948', 'gov_exp_educ1950', 'gov_exp_educ1955', 'gov_exp_educ1960', 'gov_exp_educ1965',
             'gov_exp_hwy1948', 'gov_exp_hwy1955', 'gov_exp_hwy1960', 'gov_exp_hwy1965',
             'gov_exp_wlf1948', 'gov_exp_wlf1950', 'gov_exp_wlf1960', 'gov_exp_wlf1965',
             'gov_exp_hth_hosp1948', 'gov_exp_hth_hosp1950', 'gov_exp_hth_hosp1960', 'gov_exp_hth_hosp1965',
             'gov_exp_swg1948', 'gov_exp_swg1955', 'gov_exp_swg1960', 'gov_exp_swg1965']

df.update(df.filter(thousands) / 1000)

# Transform ones that are %s of other variables
df.update(df.filter('gov_rev_int1970') * 'gov_rev1970' / 100)
df.update(df.filter('gov_exp_educ1970') * 'gov_exp_dir1970' / 100)
df.update(df.filter('gov_exp_educ1975') * 'gov_exp_dir1975' / 100)
df.update(df.filter('gov_exp_hwy1970') * 'gov_exp_dir1970' / 100)
df.update(df.filter('gov_exp_hwy1975') * 'gov_exp_dir1975' / 100)
df.update(df.filter('gov_exp_wlf1970') * 'gov_exp_dir1970' / 100)
df.update(df.filter('gov_exp_wlf1975') * 'gov_exp_dir1975' / 100)
df.update(df.filter('gov_exp_swg1970') * 'gov_exp_dir1970' / 100)
df.update(df.filter('gov_exp_swg1975') * 'gov_exp_dir1975' / 100)

# Reshape data

# Selecting time series columns
cols = list(df.columns)
regex_yrs = re.compile('.*[19].*')
year_vars = [x for x in cols if regex_yrs.match(x)]

# Creating unique stubs
stub_vars = [x[:-4] for x in year_vars]
stub_vars = list(set(stub_vars))

# Sorting columns lexicographically
df = df.reindex(sorted(df.columns), axis=1)

# Putting town_id as first column as index
# town_id = df['town_id']
# df.drop(labels=['town_id'], axis=1,inplace = True)
# df.insert(0, 'town_id', town_id)
df.set_index('town_id')

df = pd.wide_to_long(df, stub_vars, i='town_id', j='Year')

# Prepare PR data to merge

# Import data
df_pr = pd.read_stata(' PR data.dta')

# Make sure town_id is a series not the index
df = df.reset_index()
df_pr = df_pr.reset_index()

# Make columns match up
df.rename(columns={'Year':'year'}, inplace=True)

# Make town_id a string so that it can be merged (need same type)
df['town_id'] = df['town_id'].astype(str).astype(int)

# Merge
df_join = pd.merge_ordered(df, df_pr, on=['town_id', 'year'])

# Code in 0s for non-PR towns - so default is First Past The Post
df_join['PR'] = df_join['PR'].fillna(0)

# Merge in deflator data
df_price = pd.read_csv('Price deflators.csv')

df_price_join = pd.merge_ordered(df_join, df_price, on=['year'])

# Merge in education spending data
df_tot_educ = pd.read_stata('Total education spending.dta')

df_ready = pd.merge_ordered(df_price_join, df_tot_educ, on=['year'])

# Pickle dataframe for future use
df_ready.to_pickle('Merged data')

