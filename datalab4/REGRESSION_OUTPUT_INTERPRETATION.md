# Regression Output and Interpretation

## Model Specification

**Equation**: 
```
ln Xod,t = α + β1 × ln distod + β2 × languageod + β3 × religionod + β4 × colonialod + β5 × borderod + ẽod,t
```

**Implementation**: `lntrade ~ lndist + lang + relig + colony + border`

---

## Regression Results

### Model Statistics
- **R-squared**: 0.0680 (6.80% of variation explained)
- **Adjusted R-squared**: 0.0679
- **Observations**: 840,167
- **F-statistic**: 12,250.45 (p < 0.001)
- **Method**: Ordinary Least Squares (OLS)

### Coefficient Estimates

| Coefficient | Estimate | Std Error | t-statistic | p-value | 95% CI |
|-------------|----------|-----------|-------------|---------|--------|
| **α (Intercept)** | 15.9255 | 0.0504 | 315.83 | <0.001 | [15.827, 16.024] |
| **β1 (lndist)** | -0.9869 | 0.0057 | -173.33 | <0.001 | [-0.998, -0.976] |
| **β2 (lang)** | -0.7576 | 0.0121 | -62.40 | <0.001 | [-0.781, -0.734] |
| **β3 (relig)** | -0.4108 | 0.0171 | -23.99 | <0.001 | [-0.444, -0.377] |
| **β4 (colony)** | 4.0596 | 0.0334 | 121.66 | <0.001 | [3.994, 4.125] |
| **β5 (border)** | 1.9684 | 0.0306 | 64.25 | <0.001 | [1.908, 2.028] |

---

## Detailed Coefficient Interpretations

### 1. **Intercept (α = 15.9255)**

**Interpretation**: 
- The baseline log trade level when all independent variables are zero
- In levels: exp(15.9255) ≈ $8.1 million (baseline trade value)
- **Statistical Significance**: Highly significant (t = 315.83, p < 0.001)

**Economic Meaning**: 
- Represents the average log trade flow when distance is at its minimum and all binary variables (language, religion, colonial, border) are zero
- This is a scaling constant that sets the baseline trade level

---

### 2. **Distance (β1 = -0.9869)** ✓ **Makes Economic Sense**

**Interpretation**: 
- A **1% increase in distance reduces trade by approximately 0.99%**
- This is the **distance elasticity of trade**
- The coefficient is close to -1, which is consistent with standard gravity model estimates

**Economic Rationale**:
- Distance proxies for transportation costs
- Longer distances increase shipping costs, reducing trade profitability
- This is a fundamental trade barrier in gravity models
- The magnitude (-0.99) suggests that distance has a nearly proportional negative effect on trade

**Statistical Significance**: 
- Highly significant (t = -173.33, p < 0.001)
- Standard error is very small (0.0057), indicating precise estimation
- 95% confidence interval: [-0.998, -0.976]

**Policy Implication**: 
- Reducing transportation costs (through infrastructure investment) can significantly boost trade
- Distance is a fundamental constraint on international trade

---

### 3. **Common Language (β2 = -0.7576)** ⚠️ **Counterintuitive Sign**

**Interpretation**: 
- Countries sharing a common official language trade approximately **53.1% less** (exp(-0.7576) - 1 ≈ -0.531) than countries without a common language
- This is **counterintuitive** and contradicts economic theory

**Problem**: 
- The negative sign suggests that common language reduces trade, which contradicts:
  - Economic theory (language should reduce transaction costs)
  - Fixed effects regression results (which show a positive coefficient of +0.66)
  - Empirical evidence from the gravity model literature

**Possible Explanations**:
1. **Omitted Variable Bias**: 
   - Without country fixed effects, the language variable may be picking up other country-specific characteristics
   - Countries that share languages might be systematically different (e.g., smaller countries, different income levels, different trade patterns)

2. **Selection Effect**: 
   - Language sharing might be correlated with other factors that reduce trade
   - For example, countries with common languages might be in regions with lower overall trade volumes

3. **Correlation with Other Variables**: 
   - Language might be correlated with distance, colonial relationships, or other omitted factors
   - Without controlling for these, the coefficient is biased

**Statistical Significance**: 
- Highly significant (t = -62.40, p < 0.001), but the sign is likely wrong due to omitted variable bias

**Conclusion**: 
- This coefficient should **not be interpreted causally**
- The fixed effects regression (which controls for country characteristics) shows the correct positive effect of language on trade

---

### 4. **Common Religion (β3 = -0.4108)** ⚠️ **Counterintuitive Sign**

**Interpretation**: 
- Countries sharing a common religion trade approximately **33.7% less** (exp(-0.4108) - 1 ≈ -0.337) than countries without a common religion
- This is **counterintuitive** and contradicts economic theory

**Problem**: 
- Similar to language, the negative sign contradicts:
  - Economic theory (religion should reduce transaction costs through cultural similarity)
  - Fixed effects regression results (which show a positive coefficient of +0.40)
  - Empirical evidence

**Possible Explanations**:
1. **Omitted Variable Bias**: 
   - Religion may be correlated with unobserved country characteristics
   - Countries with common religions may be clustered in regions with different trade patterns

2. **Geographic Clustering**: 
   - Religious similarity might be correlated with geographic proximity or other factors
   - Without controlling for these, the coefficient is biased

3. **Income or Development Effects**: 
   - Religious similarity might be correlated with income levels or development stages that affect trade differently

**Statistical Significance**: 
- Highly significant (t = -23.99, p < 0.001), but the sign is likely wrong due to omitted variable bias

**Conclusion**: 
- This coefficient should **not be interpreted causally**
- The fixed effects regression shows the correct positive effect of religion on trade

---

### 5. **Common Colonial Metropolis (β4 = 4.0596)** ✓ **Makes Economic Sense**

**Interpretation**: 
- Countries sharing a common colonial metropolis trade approximately **57.0 times more** (exp(4.0596) ≈ 57.0) than countries without this relationship
- This is an **extremely large effect**, the largest in the regression

**Economic Rationale**:
- Countries colonized by the same power share:
  - Institutions and legal frameworks
  - Administrative structures and governance systems
  - Trade networks and infrastructure from the colonial era
  - Often share language, currency, or trade preferences
  - Established business relationships and cultural ties

**Statistical Significance**: 
- Highly significant (t = 121.66, p < 0.001)
- Standard error is small (0.0334), indicating precise estimation
- 95% confidence interval: [3.994, 4.125]

**Comparison with Fixed Effects**: 
- The fixed effects estimate is much smaller (+1.01), suggesting that colonial relationships are partially explained by country-specific factors (size, income, etc.)
- However, even after controlling for fixed effects, the effect remains substantial

**Policy Implication**: 
- Historical colonial relationships create persistent trade advantages
- These relationships can be leveraged for trade promotion
- Institutional similarity from colonial relationships facilitates trade

---

### 6. **Shared Border (β5 = 1.9684)** ✓ **Makes Economic Sense**

**Interpretation**: 
- Contiguous countries (sharing a border) trade approximately **6.2 times more** (exp(1.9684) ≈ 7.2) than non-contiguous countries
- This is a **large and economically meaningful effect**

**Economic Rationale**:
- Lower transportation costs for land-based trade
- Easier cross-border movement of goods and people
- Often accompanied by trade agreements (e.g., NAFTA, EU, Mercosur)
- Geographic proximity facilitates trade
- Reduced border frictions for neighboring countries

**Statistical Significance**: 
- Highly significant (t = 64.25, p < 0.001)
- Standard error is small (0.0306), indicating precise estimation
- 95% confidence interval: [1.908, 2.028]

**Comparison with Fixed Effects**: 
- The fixed effects estimate is smaller (+0.46), suggesting that border effects are partially explained by country-specific characteristics
- However, the effect remains substantial even after controlling for fixed effects

**Policy Implication**: 
- Trade agreements between neighboring countries can significantly boost trade
- Reducing border frictions (customs, regulations) can facilitate trade
- Infrastructure investment at borders can enhance trade flows

---

## Overall Model Assessment

### Strengths:
1. **Distance Effect is Robust**: The negative distance coefficient (-0.99) is consistent with gravity model theory and is highly significant
2. **Historical Relationships Matter**: Colonial relationships have the largest effect, confirming the persistence of historical trade patterns
3. **Geographic Proximity Matters**: Shared borders significantly boost trade
4. **Large Sample Size**: 840,167 observations provide high statistical power
5. **All Coefficients Statistically Significant**: All variables are highly significant (p < 0.001)

### Weaknesses:
1. **Low R-squared**: Only 6.8% of variation explained, suggesting many important factors are omitted
2. **Omitted Variable Bias**: 
   - Language and religion show counterintuitive negative signs
   - This is likely due to omitted country-specific factors (GDP, market size, institutions)
3. **No Fixed Effects**: Without controlling for country characteristics, estimates may be biased
4. **Counterintuitive Signs**: Language and religion coefficients contradict theory and fixed effects results

---

## Do the Coefficients Make Sense?

### ✓ **Make Economic Sense:**
1. **Distance (-0.9869)**: Negative, as expected - distance reduces trade
2. **Colonial Relationship (+4.0596)**: Positive and very large - historical ties boost trade dramatically
3. **Shared Border (+1.9684)**: Positive and large - geographic proximity facilitates trade

### ⚠️ **Counterintuitive (Due to Omitted Variable Bias):**
1. **Common Language (-0.7576)**: Negative sign contradicts theory
2. **Common Religion (-0.4108)**: Negative sign contradicts theory

**Conclusion**: 
- Three out of five coefficients make economic sense
- The two counterintuitive coefficients (language and religion) are likely biased due to omitted variable bias
- Fixed effects regression is needed to obtain unbiased estimates

---

## What Have We Learned?

### 1. **Distance is a Fundamental Trade Barrier**
- The distance elasticity of -0.99 confirms that geography matters fundamentally for trade
- This is robust across specifications and consistent with gravity model theory

### 2. **Historical Relationships Have Persistent Effects**
- Colonial relationships have the largest effect on trade (57x increase)
- This demonstrates the long-lasting impact of historical institutions and trade networks
- Even after controlling for country characteristics, the effect remains substantial

### 3. **Geographic Proximity Facilitates Trade**
- Shared borders increase trade by over 6 times
- This confirms that geographic proximity reduces trade costs and facilitates trade

### 4. **Omitted Variable Bias is Serious**
- The negative coefficients for language and religion demonstrate how unobserved country characteristics can confound estimates
- Without fixed effects, we cannot identify the causal effect of these bilateral characteristics
- This highlights the importance of proper econometric specification

### 5. **Model Specification Matters**
- The low R-squared (6.8%) shows that country-specific factors are crucial for explaining trade
- Simple OLS without fixed effects captures only a small portion of trade variation
- Fixed effects regression is essential for obtaining unbiased estimates

### 6. **Gravity Model Works**
- Despite the issues with some coefficients, the model successfully identifies key determinants of trade flows
- Distance, colonial relationships, and borders show expected effects
- The model provides valuable insights into trade patterns

### 7. **Policy Implications**
- **Infrastructure Investment**: Reducing transportation costs can significantly boost trade
- **Trade Agreements**: Can facilitate trade between neighboring countries
- **Historical Ties**: Existing colonial relationships create persistent trade advantages
- **Methodological Caution**: Policy analysis should use fixed effects regressions to avoid biased estimates

---

## Conclusion

The OLS regression reveals important patterns in international trade:
- **Distance** is a fundamental trade barrier (elasticity ≈ -1)
- **Colonial relationships** have the largest effect on trade (57x increase)
- **Shared borders** significantly boost trade (6x increase)
- **Language and religion** show counterintuitive signs due to omitted variable bias

The exercise demonstrates that **proper econometric specification matters** - what appears to be a negative effect of language on trade is actually a positive effect once we control for country characteristics through fixed effects. This is a crucial lesson for empirical trade analysis.

**Recommendation**: For policy analysis and causal inference, use fixed effects regression to control for country-specific factors and obtain unbiased estimates of bilateral trade determinants.

