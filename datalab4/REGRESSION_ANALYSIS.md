# Gravity Model Regression Analysis - Datalab 4

## Executive Summary

This analysis implements a gravity model of international trade, examining how bilateral trade flows are influenced by distance and various cultural, historical, and institutional factors. The model uses fixed effects to control for country-specific characteristics and estimates the impact of bilateral factors on trade.

## Data and Methodology

- **Dataset**: Gravity_V202102.dta
- **Sample**: 903,272 observations (simple regression) and 168,435 observations (fixed effects regression)
- **Time Period**: 1948-2020
- **Methodology**: 
  1. Simple OLS regression of log trade on log distance
  2. Fixed effects regression with country-pair fixed effects (absorbing exporter and importer fixed effects)

### Variable Definitions

All binary variables are true/false indicators:
- **`comlang_off`**: Do origin (o) and destination (d) share a common official language?
- **`comrelig`**: Do o and d share a common religion?
- **`col_dep_ever`**: Do o and d share a common colonial metropolis (were colonized by the same colonial power)?
- **`contig`**: Do o and d share a border (are contiguous)?

## Regression Results

### 1. Simple Gravity Regression (Without Fixed Effects)

**Model**: `lntrade ~ lndist`

**Results**:
- **Intercept**: 16.7957 (SE: 0.044, p < 0.001)
- **lndist (log distance)**: -1.1156 (SE: 0.005, p < 0.001)
- **R-squared**: 0.050
- **Observations**: 903,272

**Interpretation**:
- The coefficient on log distance is **-1.1156**, meaning that a 1% increase in distance is associated with approximately a **1.12% decrease in trade flows**.
- This is consistent with the gravity model prediction that distance acts as a trade cost, reducing bilateral trade.
- The R-squared of 0.050 indicates that distance alone explains only 5% of the variation in trade flows, suggesting that other factors (country sizes, fixed effects, etc.) are important.

### 2. Fixed Effects Gravity Regression

**Model**: `lntrade_r ~ lndist_r + lang_r + leg_r + relig_r + colony_r + border_r`

After absorbing exporter and importer fixed effects, the regression results are:

| Variable | Coefficient | Std Error | t-statistic | p-value | Interpretation |
|----------|-------------|-----------|-------------|---------|----------------|
| **Intercept** | 0.0127 | 0.006 | 2.109 | 0.035 | Baseline trade level |
| **lndist_r** | -1.4737 | 0.010 | -153.190 | <0.001 | **Distance elasticity** |
| **lang_r** | 0.6558 | 0.020 | 32.779 | <0.001 | **Common language effect** |
| **leg_r** | 0.1959 | 0.031 | 6.263 | <0.001 | **Legal system similarity** |
| **relig_r** | 0.3996 | 0.032 | 12.675 | <0.001 | **Common religion effect** |
| **colony_r** | 1.0056 | 0.050 | 19.928 | <0.001 | **Colonial relationship effect** |
| **border_r** | 0.4632 | 0.045 | 10.329 | <0.001 | **Contiguity (shared border) effect** |

**Model Statistics**:
- **R-squared**: 0.188 (18.8% of variation explained)
- **Observations**: 168,435
- **F-statistic**: 6,492 (highly significant)

## Coefficient Interpretation

### 1. **Distance (lndist_r): -1.4737** ✓ Makes Economic Sense

- **Interpretation**: A 1% increase in distance reduces trade by approximately **1.47%**.
- **Economic Rationale**: 
  - Distance proxies for transportation costs, which directly reduce trade profitability
  - The magnitude (-1.47) is larger than the simple regression (-1.12), suggesting that after controlling for country fixed effects, the true distance effect is stronger
  - This is consistent with empirical gravity literature, which typically finds distance elasticities between -0.9 and -1.5
- **Policy Implication**: Reducing transportation costs (e.g., through infrastructure investment) can significantly boost trade

### 2. **Common Language (lang_r): +0.6558** ✓ Makes Economic Sense

- **Interpretation**: Countries sharing an official language trade approximately **92.6% more** (exp(0.6558) - 1 ≈ 0.926) than countries without a common language.
- **Variable Definition**: `comlang_off` is a binary indicator (true/false) for whether origin and destination countries share a common official language.
- **Economic Rationale**:
  - Common language reduces communication costs and transaction costs
  - Facilitates contract enforcement and business relationships
  - Reduces information asymmetries
- **Policy Implication**: Language barriers are significant trade impediments; translation services and language education can facilitate trade

### 3. **Legal System Similarity (leg_r): +0.1959** ✓ Makes Economic Sense

- **Interpretation**: Countries with similar legal systems trade approximately **21.6% more** (exp(0.1959) - 1 ≈ 0.216).
- **Economic Rationale**:
  - Similar legal systems reduce contract enforcement costs
  - Lower legal uncertainty encourages cross-border transactions
  - Facilitates dispute resolution
- **Policy Implication**: Legal harmonization (e.g., through trade agreements) can boost trade

### 4. **Common Religion (relig_r): +0.3996** ✓ Makes Economic Sense

- **Interpretation**: Countries sharing a common religion trade approximately **49.1% more** (exp(0.3996) - 1 ≈ 0.491).
- **Variable Definition**: `comrelig` is a binary indicator (true/false) for whether origin and destination countries share a common religion.
- **Economic Rationale**:
  - Shared cultural values reduce transaction costs
  - Religious networks can facilitate business relationships
  - Cultural similarity reduces information costs
- **Note**: This effect is substantial but smaller than language, suggesting language is a more direct trade facilitator

### 5. **Common Colonial Metropolis (colony_r): +1.0056** ✓ Makes Economic Sense

- **Interpretation**: Countries that share a common colonial metropolis (were colonized by the same colonial power) trade approximately **173.5% more** (exp(1.0056) - 1 ≈ 1.735), or nearly **2.7 times** as much.
- **Variable Definition**: `col_dep_ever` indicates whether origin and destination countries share a common colonial metropolis (true/false binary indicator).
- **Economic Rationale**:
  - Countries colonized by the same power share institutions, legal frameworks, and administrative structures
  - Established trade networks and infrastructure from the colonial era
  - Shared language, currency, or trade preferences from colonial relationships
  - This is the **largest effect** among all variables, highlighting the persistence of historical institutional and trade relationships
- **Policy Implication**: Historical colonial relationships create persistent trade advantages through shared institutions and networks

### 6. **Shared Border (border_r): +0.4632** ✓ Makes Economic Sense

- **Interpretation**: Contiguous countries (sharing a border) trade approximately **58.9% more** (exp(0.4632) - 1 ≈ 0.589).
- **Variable Definition**: `contig` is a binary indicator (true/false) for whether origin and destination countries share a border.
- **Economic Rationale**:
  - Lower transportation costs for land-based trade
  - Easier cross-border movement of goods and people
  - Often accompanied by trade agreements (e.g., NAFTA, EU)
- **Note**: This effect is substantial but smaller than colonial relationships, suggesting that historical ties matter more than just geographic proximity

## Key Findings and Lessons Learned

### 1. **Distance Matters, But Not Everything**

The distance elasticity of -1.47 confirms that geography is a fundamental determinant of trade. However, the R-squared of 18.8% (even with fixed effects) shows that bilateral factors alone don't explain all trade variation—country-specific factors (GDP, market size, etc.) captured by fixed effects are crucial.

### 2. **Cultural and Institutional Factors Are Powerful**

The coefficients on language, religion, legal systems, and colonial relationships are all highly significant and economically meaningful. This suggests that:
- **Transaction costs** (language, legal systems) are as important as transportation costs
- **Historical relationships** (colonial ties) have persistent effects on trade
- **Cultural similarity** (religion) facilitates trade through reduced information and enforcement costs

### 3. **Fixed Effects Are Essential**

Comparing the simple regression (R² = 0.050) to the fixed effects regression (R² = 0.188) shows that:
- Country-specific factors (size, income, institutions) explain a large portion of trade variation
- The distance coefficient changes from -1.12 to -1.47, suggesting that without fixed effects, the distance effect is biased downward
- Fixed effects control for unobserved country heterogeneity

### 4. **Policy Implications**

1. **Infrastructure Investment**: Reducing transportation costs (distance effect) can significantly boost trade
2. **Trade Agreements**: Can reduce transaction costs through legal harmonization
3. **Cultural Exchange**: Language and cultural programs can facilitate trade
4. **Historical Ties**: Existing relationships (colonial, linguistic) create persistent trade advantages

### 5. **Methodological Insights**

- The **absorbing least squares** approach properly handles high-dimensional fixed effects
- The residualized variables (with "_r" suffix) represent bilateral factors net of country-specific effects
- The model successfully identifies the causal effect of bilateral characteristics on trade flows

## Conclusion

The gravity model confirms that international trade follows predictable patterns based on:
1. **Geographic factors** (distance, contiguity)
2. **Cultural factors** (language, religion)
3. **Institutional factors** (legal systems)
4. **Historical factors** (colonial relationships)

All coefficients have the expected signs and are highly statistically significant. The magnitudes are economically meaningful and consistent with the gravity model literature. The exercise demonstrates that trade flows are determined by both economic fundamentals (captured by fixed effects) and bilateral characteristics that reduce trade costs.

The model provides valuable insights for understanding trade patterns and designing trade policies that can reduce barriers and facilitate international commerce.

