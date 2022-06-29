import pandas as pd
import numpy as np
import jupyter
import sklearn
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# Load cleaned data
df = pd.read_pickle('Merged data')

df.set_index('town_id')

# Creating dict of spending data variables
spending = {
    'gov': ['gov_rev', 'gov_rev_int', 'gov_tx', 'gov_exp_dir', 'gov_exp_educ', 'gov_exp_hth_hosp', 'gov_exp_hwy',
            'gov_exp_wlf'],
    'r_gov': [],
    'sr_gov': [],
    'lr_gov': [],
    'lgsr_gov': []}

# Populating dict and the keys' respective items
for i in spending['gov']:
    spending['r_gov'].append('r_' + i)
    spending['sr_gov'].append('sr_' + i)
    spending['lr_gov'].append('lr_' + i)
    spending['lgsr_gov'].append('lgsr_' + i)

# Creating 4 pd series of each variables
for i in range(len(spending['gov'])):
    # Real spending
    df[spending['r_gov'][i]] = (df[spending['gov'][i]] / df['defl_gdp_fin']) * 100
    # Share of government revenue (real)
    df[spending['sr_gov'][i]] = (df[spending['r_gov'][i]] / df['r_gov_rev']) * 100
    # Log of real spending
    df[spending['lr_gov'][i]] = np.log(df[spending['r_gov'][i]])
    # Log of share of government revenue (real)
    df[spending['lgsr_gov'][i]] = np.log((df[spending['r_gov'][i]] / df['r_gov_rev']) * 100)

# Creating dict of education spending variables
educ = {'base': ['fed_educ', 'xfer_educ', 'st_educ', 'loc_educ', 'tot_educ'],
        'r_educ': [],
        'pcr_educ': [],
        'l_educ': []}

# Populating dict and the keys' respective items
for i in educ['base']:
    educ['r_educ'].append('r_' + i)
    educ['pcr_educ'].append('pcr_' + i)
    educ['l_educ'].append('l_' + i)

# Creating 3 pd series of each variables
for i in range(len(educ['base'])):
    # Total real education spending
    df[educ['r_educ'][i]] = (df[educ['base'][i]] / df['defl_gdp_fin']) * 100
    # Per capita real education spending
    df[educ['pcr_educ'][i]] = df[educ['r_educ'][i]] / df['tot_popl']
    # Log of total real education spending
    df[educ['l_educ'][i]] = np.log(df[educ['base'][i]])

# Creating log of population
df['l_popl'] = np.log(df['tot_popl'])

# Saving dataframe
df.to_pickle('Prepared data')