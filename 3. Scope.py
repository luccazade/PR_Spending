import numpy as np
import statsmodels.api as sm
import pandas as pd
import jupyter
from linearmodels import PanelOLS

df = pd.read_pickle('Prepared data')

df = df.set_index(['town_id', 'year'])

exog = df[['PR', 'l_popl', 'lr_gov_rev_int', 'med_inc']]
exog = sm.add_constant(exog)
model = PanelOLS(df.r_gov_exp_educ, exog, entity_effects=True, time_effects=True)
res = model.fit(cov_type='clustered', cluster_entity=True)
print(res)