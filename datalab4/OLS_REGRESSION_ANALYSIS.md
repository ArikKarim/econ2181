# OLS Gravity Regression Analysis

## Variable Definitions - True/False Answers

Based on the regression analysis documentation:

1. **df["comlang_off"]: do o, d share common language?** 
   - **Answer: TRUE** ✓

2. **df["comrelig"]: do o, d share common religion?**
   - **Answer: TRUE** ✓

3. **df["col_dep_ever"]: do o, d share common colonial metropolis?**
   - **Answer: TRUE** ✓

4. **df["contig"]: do o, d share a border?**
   - **Answer: TRUE** ✓

All variables are binary (true/false) indicators.

---

## Regression Specification

**Model**: 
```
ln Xod,t = α + β1 × ln distod + β2 × languageod + β3 × religionod + β4 × colonialod + β5 × borderod + ẽod,t
```

**Implementation**: `lntrade ~ lndist + lang + relig + colony + border`

This is a simple OLS regression **without fixed effects**, allowing us to see the raw relationships between bilateral characteristics and trade flows.

---

## Regression Results

### Model Statistics
- **R-squared**: 0.068 (6.8% of variation explained)
- **Observations**: 840,167
- **F-statistic**: 12,250 (highly significant, p < 0.001)
- **Method**: Ordinary Least Squares (OLS)

### Coefficient Estimates

| Variable | Coefficient | Std Error | t-statistic | p-value | 95% CI |
|----------|-------------|-----------|-------------|---------|--------|
| **Intercept** | 15.9255 | 0.050 | 315.829 | <0.001 | [15.827, 16.024] |
| **lndist** | -0.9869 | 0.006 | -173.328 | <0.001 | [-0.998, -0.976] |
| **lang** | -0.7576 | 0.012 | -62.398 | <0.001 | [-0.781, -0.734] |
| **relig** | -0.4108 | 0.017 | -23.987 | <0.001 | [-0.444, -0.377] |
| **colony** | 4.0596 | 0.033 | 121.658 | <0.001 | [3.994, 4.125] |
| **border** | 1.9684 | 0.031 | 64.251 | <0.001 | [1.908, 2.028] |

---

## Coefficient Interpretation

### 1. **Distance (lndist): -0.9869** ✓ Makes Economic Sense

- **Interpretation**: A 1% increase in distance reduces trade by approximately **0.99%**.
- **Economic Rationale**: 
  - Distance proxies for transportation costs
  - Longer distances increase shipping costs, reducing trade profitability
  - This coefficient is close to -1, which is consistent with standard gravity model estimates
- **Comparison**: This is slightly smaller in magnitude than the fixed effects estimate (-1.47), suggesting that without controlling for country characteristics, the distance effect is slightly attenuated

### 2. **Common Language (lang): -0.7576** ⚠️ Counterintuitive Sign

- **Interpretation**: Countries sharing a common language trade approximately **53.1% less** (exp(-0.7576) - 1 ≈ -0.531) than countries without a common language.
- **Problem**: This **negative coefficient is counterintuitive** and contradicts economic theory and the fixed effects results.
- **Possible Explanations**:
  1. **Omitted Variable Bias**: Without country fixed effects, the language variable may be picking up other country-specific characteristics
  2. **Selection Effect**: Countries that share languages might be systematically different in other ways (e.g., smaller countries, different income levels)
  3. **Correlation with Other Factors**: Language might be correlated with distance or other omitted variables
- **Comparison**: The fixed effects regression shows a **positive** coefficient (+0.6558), which makes economic sense. This suggests that the negative coefficient here is due to omitted variable bias.

### 3. **Common Religion (relig): -0.4108** ⚠️ Counterintuitive Sign

- **Interpretation**: Countries sharing a common religion trade approximately **33.7% less** (exp(-0.4108) - 1 ≈ -0.337) than countries without a common religion.
- **Problem**: This **negative coefficient is counterintuitive** and contradicts the fixed effects results.
- **Possible Explanations**:
  1. **Omitted Variable Bias**: Similar to language, religion may be correlated with unobserved country characteristics
  2. **Geographic Clustering**: Countries with common religions may be clustered in regions with lower overall trade volumes
  3. **Income Effects**: Religious similarity might be correlated with income levels or other economic factors
- **Comparison**: The fixed effects regression shows a **positive** coefficient (+0.3996), confirming that religion facilitates trade once country-specific factors are controlled for.

### 4. **Common Colonial Metropolis (colony): +4.0596** ✓ Makes Economic Sense

- **Interpretation**: Countries sharing a common colonial metropolis trade approximately **57.8 times more** (exp(4.0596) ≈ 57.8) than countries without this relationship.
- **Economic Rationale**:
  - This is an **extremely large effect**, the largest in the regression
  - Countries colonized by the same power share institutions, legal systems, and trade networks
  - Established infrastructure and business relationships from colonial era
  - Often share language, currency, or trade preferences
- **Comparison**: The fixed effects estimate (+1.0056) is much smaller but still substantial. The difference suggests that colonial relationships are correlated with country-specific factors (size, income, etc.) that boost trade.

### 5. **Shared Border (border): +1.9684** ✓ Makes Economic Sense

- **Interpretation**: Contiguous countries trade approximately **6.2 times more** (exp(1.9684) ≈ 7.2) than non-contiguous countries.
- **Economic Rationale**:
  - Lower transportation costs for land-based trade
  - Easier cross-border movement of goods and people
  - Often accompanied by trade agreements (e.g., NAFTA, EU)
  - Geographic proximity facilitates trade
- **Comparison**: The fixed effects estimate (+0.4632) is much smaller, suggesting that border effects are partially explained by country-specific characteristics.

---

## Key Findings and Lessons Learned

### 1. **The Importance of Fixed Effects**

The comparison between OLS and fixed effects regressions reveals critical insights:

- **Language and Religion**: Show **opposite signs** in OLS vs. fixed effects regressions
  - OLS: Negative (counterintuitive)
  - Fixed Effects: Positive (makes economic sense)
  - **Lesson**: Without controlling for country-specific factors, these variables suffer from omitted variable bias

- **Colonial and Border Effects**: Are **much larger** in OLS than fixed effects
  - OLS: colony = 4.06, border = 1.97
  - Fixed Effects: colony = 1.01, border = 0.46
  - **Lesson**: These effects are partially explained by country characteristics (size, income, etc.)

### 2. **Omitted Variable Bias is Real**

The negative coefficients for language and religion in the OLS regression demonstrate the importance of controlling for unobserved heterogeneity:
- Countries that share languages or religions may differ systematically in other ways
- Without fixed effects, we cannot identify the causal effect of these bilateral characteristics
- Fixed effects regression is essential for identifying the true bilateral effects

### 3. **Distance Effect is Robust**

The distance coefficient is negative and significant in both specifications:
- OLS: -0.99
- Fixed Effects: -1.47
- **Lesson**: Distance is a fundamental trade barrier, and its effect is robust to specification

### 4. **Historical Relationships Matter Most**

The colonial relationship has the largest effect in both specifications:
- This suggests that historical institutional and trade relationships have persistent effects
- These effects are partially explained by country characteristics but remain substantial even after controlling for fixed effects

### 5. **R-squared is Low Without Fixed Effects**

- OLS R² = 0.068 (6.8%)
- Fixed Effects R² = 0.188 (18.8%)
- **Lesson**: Country-specific factors (GDP, market size, institutions) explain a large portion of trade variation that cannot be captured by bilateral characteristics alone

---

## Do the Coefficients Make Sense?

### ✓ **Make Economic Sense:**
1. **Distance (-0.9869)**: Negative, as expected - distance reduces trade
2. **Colonial Relationship (+4.0596)**: Positive and large - historical ties boost trade
3. **Shared Border (+1.9684)**: Positive - geographic proximity facilitates trade

### ⚠️ **Counterintuitive (Due to Omitted Variable Bias):**
1. **Common Language (-0.7576)**: Negative sign contradicts theory and fixed effects results
2. **Common Religion (-0.4108)**: Negative sign contradicts theory and fixed effects results

**Conclusion**: The OLS regression without fixed effects suffers from omitted variable bias, particularly for language and religion. The fixed effects regression provides more reliable estimates of the causal effects of bilateral characteristics on trade.

---

## What Have We Learned?

1. **Fixed Effects Are Essential**: Without controlling for country-specific factors, regression estimates can be biased and even have the wrong sign.

2. **Omitted Variable Bias is Serious**: The negative coefficients for language and religion demonstrate how unobserved country characteristics can confound estimates.

3. **Distance is a Fundamental Trade Barrier**: The distance effect is robust across specifications, confirming that geography matters for trade.

4. **Historical Relationships Persist**: Colonial relationships have the largest effect on trade, even after controlling for country characteristics.

5. **Model Specification Matters**: The choice between OLS and fixed effects regression dramatically affects coefficient estimates and interpretations.

6. **Gravity Model Works**: Despite the issues with OLS, the model successfully identifies key determinants of trade flows, with distance, colonial relationships, and borders showing expected effects.

7. **Country Characteristics Matter**: The low R-squared in OLS (6.8%) vs. fixed effects (18.8%) shows that country-specific factors are crucial for explaining trade patterns.

---

## Policy Implications

1. **Infrastructure Investment**: Reducing transportation costs (distance effect) can significantly boost trade.

2. **Trade Agreements**: Can facilitate trade between neighboring countries (border effect).

3. **Historical Ties**: Existing colonial relationships create persistent trade advantages that can be leveraged.

4. **Methodological Caution**: Policy analysis should use fixed effects regressions to avoid biased estimates from omitted variable bias.

---

## Conclusion

The OLS regression reveals important patterns in international trade, but also demonstrates the limitations of simple regression models. The counterintuitive signs for language and religion highlight the importance of controlling for country-specific factors through fixed effects. The robust effects of distance, colonial relationships, and borders confirm that geography and history are fundamental determinants of trade flows.

The exercise teaches us that **proper econometric specification matters** - what appears to be a negative effect of language on trade is actually a positive effect once we control for country characteristics. This is a crucial lesson for empirical trade analysis.

