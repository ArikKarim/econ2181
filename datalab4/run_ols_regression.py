import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# Load data
data = r'C:\Users\15613\Downloads\Gravity_V202102.dta'
df = pd.read_stata(data)

# Filter existing countries
df = df[(df['country_exists_o'] == 1) & (df['country_exists_d'] == 1)].copy()

# Create variables
df['lntrade'] = np.log(df['tradeflow_comtrade_d'])
df['lndist'] = np.log(df['distw'])
df['lang'] = df['comlang_off']      # Common language (binary)
df['relig'] = df['comrelig']        # Common religion (binary)
df['colony'] = df['col_dep_ever']   # Common colonial metropolis (binary)
df['border'] = df['contig']         # Shared border (binary)

# Drop NAs
df_ols = df.dropna(subset=['lntrade', 'lndist', 'lang', 'relig', 'colony', 'border']).copy()

# Run regression: ln Xod,t = α + β1×ln distod + β2×languageod + β3×religionod + β4×colonialod + β5×borderod + ẽod,t
model = smf.ols('lntrade ~ lndist + lang + relig + colony + border', data=df_ols).fit()

print('='*80)
print('REGRESSION: ln Xod,t = α + β1×ln distod + β2×languageod + β3×religionod + β4×colonialod + β5×borderod + ẽod,t')
print('='*80)
print(model.summary())

print('\n' + '='*80)
print('COEFFICIENT INTERPRETATIONS')
print('='*80)
print(f'\nIntercept (α): {model.params["Intercept"]:.4f}')
print(f'  Standard Error: {model.bse["Intercept"]:.4f}')
print(f'  t-statistic: {model.tvalues["Intercept"]:.2f}')
print(f'  p-value: {model.pvalues["Intercept"]:.4f}')

print(f'\nDistance (β1): {model.params["lndist"]:.4f}')
print(f'  Interpretation: A 1% increase in distance reduces trade by {abs(model.params["lndist"]):.2f}%')
print(f'  Standard Error: {model.bse["lndist"]:.4f}')
print(f'  t-statistic: {model.tvalues["lndist"]:.2f}')
print(f'  p-value: {model.pvalues["lndist"]:.4f}')

print(f'\nLanguage (β2): {model.params["lang"]:.4f}')
lang_effect = (np.exp(model.params["lang"]) - 1) * 100
print(f'  Interpretation: Countries with common language trade {lang_effect:.1f}% {"more" if lang_effect > 0 else "less"} than those without')
print(f'  Standard Error: {model.bse["lang"]:.4f}')
print(f'  t-statistic: {model.tvalues["lang"]:.2f}')
print(f'  p-value: {model.pvalues["lang"]:.4f}')

print(f'\nReligion (β3): {model.params["relig"]:.4f}')
relig_effect = (np.exp(model.params["relig"]) - 1) * 100
print(f'  Interpretation: Countries with common religion trade {relig_effect:.1f}% {"more" if relig_effect > 0 else "less"} than those without')
print(f'  Standard Error: {model.bse["relig"]:.4f}')
print(f'  t-statistic: {model.tvalues["relig"]:.2f}')
print(f'  p-value: {model.pvalues["relig"]:.4f}')

print(f'\nColonial (β4): {model.params["colony"]:.4f}')
colony_effect = (np.exp(model.params["colony"]) - 1) * 100
print(f'  Interpretation: Countries with common colonial metropolis trade {colony_effect:.1f}% more than those without')
print(f'  Standard Error: {model.bse["colony"]:.4f}')
print(f'  t-statistic: {model.tvalues["colony"]:.2f}')
print(f'  p-value: {model.pvalues["colony"]:.4f}')

print(f'\nBorder (β5): {model.params["border"]:.4f}')
border_effect = (np.exp(model.params["border"]) - 1) * 100
print(f'  Interpretation: Countries sharing a border trade {border_effect:.1f}% more than those without')
print(f'  Standard Error: {model.bse["border"]:.4f}')
print(f'  t-statistic: {model.tvalues["border"]:.2f}')
print(f'  p-value: {model.pvalues["border"]:.4f}')

print('\n' + '='*80)
print('MODEL STATISTICS')
print('='*80)
print(f'R-squared: {model.rsquared:.4f} ({model.rsquared*100:.2f}% of variation explained)')
print(f'Adjusted R-squared: {model.rsquared_adj:.4f}')
print(f'Observations: {int(model.nobs):,}')
print(f'F-statistic: {model.fvalue:.2f}')
print(f'Prob (F-statistic): {model.f_pvalue:.4f}')

