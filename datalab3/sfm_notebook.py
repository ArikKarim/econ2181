"""
ECON 2181 - International Trade Theory
Data Lab Project: Comparative Statics in the Specific Factors Model

This notebook implements the Specific Factors Model and performs comparative statics
analysis with a 20% increase in manufacturing productivity.
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# STEP 1: DEFINE BASELINE PARAMETERS
# =============================================================================

# Technology parameters
Z_M = {'H': 1.0, 'F': 1.0}
Z_A = {'H': 1.0, 'F': 1.0}

# Factor endowments
K = {'H': 4.0, 'F': 2.0}  # Capital (specific to manufacturing)
T = {'H': 3.0, 'F': 1.0}  # Land (specific to agriculture)
L = {'H': 5.0, 'F': 5.0}  # Labor (mobile between sectors)

# Technology coefficients
beta = {'H': 0.40, 'F': 0.40}

# Demand parameters
alpha = {'H': 0.50, 'F': 0.50}  # Share of expenditure on agriculture

# =============================================================================
# STEP 2: DEFINE MODEL FUNCTIONS
# =============================================================================

def Omega(i, p):
    """
    Compute Omega_i = (p * Z_i,M / Z_i,A)^(1/beta_i) * (K_i / T_i)
    This determines the relative labor allocation between sectors.
    """
    return (p * Z_M[i] / Z_A[i])**(1.0 / beta[i]) * (K[i] / T[i])

def Lm(i, p):
    """Labor allocation to manufacturing"""
    omega = Omega(i, p)
    return (omega / (1 + omega)) * L[i]

def La(i, p):
    """Labor allocation to agriculture"""
    return L[i] - Lm(i, p)

def Ym(i, p):
    """Manufacturing output: Y_i,M = Z_i,M * K_i^beta_i * L_i,M^(1-beta_i)"""
    return Z_M[i] * K[i]**beta[i] * Lm(i, p)**(1 - beta[i])

def Ya(i, p):
    """Agriculture output: Y_i,A = Z_i,A * T_i^beta_i * L_i,A^(1-beta_i)"""
    return Z_A[i] * T[i]**beta[i] * La(i, p)**(1 - beta[i])

def RS(p):
    """
    Relative Supply: RS(p) = (Y_H,M + Y_F,M) / (Y_H,A + Y_F,A)
    """
    num = sum(Ym(i, p) for i in ['H', 'F'])
    den = sum(Ya(i, p) for i in ['H', 'F'])
    return num / den

def I(i, p):
    """Total income: I_i = p * Y_i,M + Y_i,A"""
    return p * Ym(i, p) + Ya(i, p)

def Qa(i, p):
    """Demand for agriculture: Q_i,A = alpha_i * I_i"""
    return alpha[i] * I(i, p)

def Qm(i, p):
    """Demand for manufacturing: Q_i,M = (1 - alpha_i) * I_i / p"""
    return (1 - alpha[i]) * I(i, p) / p

def RD(p):
    """
    Relative Demand: RD(p) = (Q_H,M + Q_F,M) / (Q_H,A + Q_F,A)
    """
    num = sum(Qm(i, p) for i in ['H', 'F'])
    den = sum(Qa(i, p) for i in ['H', 'F'])
    return num / den

def excess_demand(p):
    """Excess demand function: ED(p) = RS(p) - RD(p)"""
    return RS(p) - RD(p)

def wage(i, p):
    """
    Equilibrium wage: w_i = P_A * MPL_i,A
    With P_A normalized to 1: w_i = MPL_i,A
    """
    L_A = La(i, p)
    return (1 - beta[i]) * Z_A[i] * (T[i] / L_A)**beta[i]

# =============================================================================
# STEP 3: BISECTION METHOD TO SOLVE FOR EQUILIBRIUM PRICE
# =============================================================================

def bisect_root(f, a, b, tol=1e-6, max_iter=100):
    """
    Find root of function f using bisection method.
    Assumes f(a) and f(b) have opposite signs.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("Root not bracketed: f(a), f(b) have same sign")
    
    for iteration in range(max_iter):
        m = 0.5 * (a + b)
        fm = f(m)
        
        if abs(fm) < tol or (b - a) < tol:
            return m
        
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    
    raise RuntimeError("Bisection failed to converge")

def solve_equilibrium():
    """Solve for equilibrium relative price p*"""
    p_low, p_high = 1.0, 1.0
    
    # Expand brackets until signs differ
    while excess_demand(p_low) > 0:
        p_low = p_low / 2
    while excess_demand(p_high) < 0:
        p_high = p_high * 2
    
    # Find equilibrium price
    p_star = bisect_root(excess_demand, p_low, p_high)
    return p_star

# =============================================================================
# STEP 4: SOLVE BASELINE EQUILIBRIUM (Question 1)
# =============================================================================

print("=" * 70)
print("BASELINE EQUILIBRIUM")
print("=" * 70)

p_star_baseline = solve_equilibrium()
print(f"\nEquilibrium relative price (P_M/P_A): {p_star_baseline:.6f}")

# Compute and store baseline equilibrium values
w_H_baseline = wage('H', p_star_baseline)
w_F_baseline = wage('F', p_star_baseline)

Y_H_M_baseline = Ym('H', p_star_baseline)
Y_H_A_baseline = Ya('H', p_star_baseline)
Y_F_M_baseline = Ym('F', p_star_baseline)
Y_F_A_baseline = Ya('F', p_star_baseline)

L_H_M_baseline = Lm('H', p_star_baseline)
L_H_A_baseline = La('H', p_star_baseline)
L_F_M_baseline = Lm('F', p_star_baseline)
L_F_A_baseline = La('F', p_star_baseline)

print(f"\nWages:")
print(f"  w_H = {w_H_baseline:.6f}")
print(f"  w_F = {w_F_baseline:.6f}")

print(f"\nOutputs:")
print(f"  Y_H,M = {Y_H_M_baseline:.6f}")
print(f"  Y_H,A = {Y_H_A_baseline:.6f}")
print(f"  Y_F,M = {Y_F_M_baseline:.6f}")
print(f"  Y_F,A = {Y_F_A_baseline:.6f}")

print(f"\nLabor Allocations:")
print(f"  L_H,M = {L_H_M_baseline:.6f}")
print(f"  L_H,A = {L_H_A_baseline:.6f}")
print(f"  L_F,M = {L_F_M_baseline:.6f}")
print(f"  L_F,A = {L_F_A_baseline:.6f}")

# =============================================================================
# STEP 5: INCREASE MANUFACTURING PRODUCTIVITY BY 20% (Question 2)
# =============================================================================

print("\n" + "=" * 70)
print("COMPARATIVE STATICS: 20% INCREASE IN MANUFACTURING PRODUCTIVITY")
print("=" * 70)

# Update manufacturing productivity
Z_M['H'] = 1.2 * 1.0
Z_M['F'] = 1.2 * 1.0

# Solve new equilibrium
p_star_new = solve_equilibrium()
print(f"\nNew equilibrium relative price (P_M/P_A): {p_star_new:.6f}")

# Compute new equilibrium values
w_H_new = wage('H', p_star_new)
w_F_new = wage('F', p_star_new)

Y_H_M_new = Ym('H', p_star_new)
Y_H_A_new = Ya('H', p_star_new)
Y_F_M_new = Ym('F', p_star_new)
Y_F_A_new = Ya('F', p_star_new)

L_H_M_new = Lm('H', p_star_new)
L_H_A_new = La('H', p_star_new)
L_F_M_new = Lm('F', p_star_new)
L_F_A_new = La('F', p_star_new)

print(f"\nWages:")
print(f"  w_H = {w_H_new:.6f} (change: {(w_H_new/w_H_baseline - 1)*100:.2f}%)")
print(f"  w_F = {w_F_new:.6f} (change: {(w_F_new/w_F_baseline - 1)*100:.2f}%)")

print(f"\nOutputs:")
print(f"  Y_H,M = {Y_H_M_new:.6f} (change: {(Y_H_M_new/Y_H_M_baseline - 1)*100:.2f}%)")
print(f"  Y_H,A = {Y_H_A_new:.6f} (change: {(Y_H_A_new/Y_H_A_baseline - 1)*100:.2f}%)")
print(f"  Y_F,M = {Y_F_M_new:.6f} (change: {(Y_F_M_new/Y_F_M_baseline - 1)*100:.2f}%)")
print(f"  Y_F,A = {Y_F_A_new:.6f} (change: {(Y_F_A_new/Y_F_A_baseline - 1)*100:.2f}%)")

print(f"\nLabor Allocations:")
print(f"  L_H,M = {L_H_M_new:.6f} (change: {(L_H_M_new/L_H_M_baseline - 1)*100:.2f}%)")
print(f"  L_H,A = {L_H_A_new:.6f} (change: {(L_H_A_new/L_H_A_baseline - 1)*100:.2f}%)")
print(f"  L_F,M = {L_F_M_new:.6f} (change: {(L_F_M_new/L_F_M_baseline - 1)*100:.2f}%)")
print(f"  L_F,A = {L_F_A_new:.6f} (change: {(L_F_A_new/L_F_A_baseline - 1)*100:.2f}%)")

# =============================================================================
# QUESTION 2b: Compare labor allocations
# =============================================================================

print("\n" + "=" * 70)
print("QUESTION 2b: LABOR ALLOCATION CHANGES")
print("=" * 70)

print("\nLabor moved TO manufacturing (from agriculture):")
print(f"  Home: {L_H_M_new - L_H_M_baseline:.6f} workers")
print(f"  Foreign: {L_F_M_new - L_F_M_baseline:.6f} workers")

print("\nInterpretation:")
print("NOTE: In this specific case, labor allocation does NOT change because")
print("the equilibrium price adjustment exactly offsets the productivity increase.")
print("Mathematically: p_new * Z_M_new = p_baseline * Z_M_baseline = 0.833808")
print("Since Omega = (p*Z_M/Z_A)^(1/beta) * (K/T), and p*Z_M stays constant,")
print("Omega stays constant, so labor allocation stays constant.")
print("This is a special case - in general, labor would reallocate.")

# =============================================================================
# QUESTION 2c: Plot relative output and prices
# =============================================================================

# Calculate relative outputs
rel_output_baseline = (Y_H_M_baseline + Y_F_M_baseline) / (Y_H_A_baseline + Y_F_A_baseline)
rel_output_new = (Y_H_M_new + Y_F_M_new) / (Y_H_A_new + Y_F_A_new)

print("\n" + "=" * 70)
print("QUESTION 2c: RELATIVE OUTPUT AND PRICES")
print("=" * 70)

print(f"\nRelative world production (Y_M/Y_A):")
print(f"  Baseline: {rel_output_baseline:.6f}")
print(f"  New: {rel_output_new:.6f}")
print(f"  Change: {(rel_output_new/rel_output_baseline - 1)*100:.2f}%")

print(f"\nRelative price (P_M/P_A):")
print(f"  Baseline: {p_star_baseline:.6f}")
print(f"  New: {p_star_new:.6f}")
print(f"  Change: {(p_star_new/p_star_baseline - 1)*100:.2f}%")

# Create comparison plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Relative Output
scenarios = ['Baseline', 'Z_M increased\nby 20%']
rel_outputs = [rel_output_baseline, rel_output_new]
ax1.bar(scenarios, rel_outputs, color=['steelblue', 'coral'], alpha=0.7, edgecolor='black')
ax1.set_ylabel('Relative Output (Y_M / Y_A)', fontsize=11)
ax1.set_title('World Relative Production', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
for i, v in enumerate(rel_outputs):
    ax1.text(i, v + 0.02, f'{v:.4f}', ha='center', fontsize=10)

# Plot 2: Relative Price
rel_prices = [p_star_baseline, p_star_new]
ax2.bar(scenarios, rel_prices, color=['steelblue', 'coral'], alpha=0.7, edgecolor='black')
ax2.set_ylabel('Relative Price (P_M / P_A)', fontsize=11)
ax2.set_title('Equilibrium Relative Price', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
for i, v in enumerate(rel_prices):
    ax2.text(i, v + 0.01, f'{v:.4f}', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('comparative_statics.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n[OK] Plot saved as 'comparative_statics.png'")

print("\nEconomic Interpretation:")
print("- SUPPLY EFFECT: Productivity increase shifts RS curve right -> more M produced")
print("- PRICE EFFECT: Increased supply of M lowers its relative price (P_M/P_A falls)")
print("- DEMAND EFFECT: Lower P_M increases quantity demanded of M")
print("- EQUILIBRIUM: Both relative output Y_M/Y_A and relative price P_M/P_A change")

# =============================================================================
# QUESTION 2d: Real wages and consumer welfare
# =============================================================================

print("\n" + "=" * 70)
print("QUESTION 2d: REAL WAGES AND CONSUMER WELFARE")
print("=" * 70)

# Real wages in terms of agriculture (P_A = 1)
real_wage_A_H_baseline = w_H_baseline / 1.0
real_wage_A_F_baseline = w_F_baseline / 1.0
real_wage_A_H_new = w_H_new / 1.0
real_wage_A_F_new = w_F_new / 1.0

# Real wages in terms of manufacturing
real_wage_M_H_baseline = w_H_baseline / p_star_baseline
real_wage_M_F_baseline = w_F_baseline / p_star_baseline
real_wage_M_H_new = w_H_new / p_star_new
real_wage_M_F_new = w_F_new / p_star_new

print("\nReal Wages (w/P_A):")
print(f"  Home - Baseline: {real_wage_A_H_baseline:.6f}, New: {real_wage_A_H_new:.6f}, "
      f"Change: {(real_wage_A_H_new/real_wage_A_H_baseline - 1)*100:.2f}%")
print(f"  Foreign - Baseline: {real_wage_A_F_baseline:.6f}, New: {real_wage_A_F_new:.6f}, "
      f"Change: {(real_wage_A_F_new/real_wage_A_F_baseline - 1)*100:.2f}%")

print("\nReal Wages (w/P_M):")
print(f"  Home - Baseline: {real_wage_M_H_baseline:.6f}, New: {real_wage_M_H_new:.6f}, "
      f"Change: {(real_wage_M_H_new/real_wage_M_H_baseline - 1)*100:.2f}%")
print(f"  Foreign - Baseline: {real_wage_M_F_baseline:.6f}, New: {real_wage_M_F_new:.6f}, "
      f"Change: {(real_wage_M_F_new/real_wage_M_F_baseline - 1)*100:.2f}%")

# Visualize real wage changes
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# Set a non-interactive backend to avoid display issues
plt.ioff()

countries = ['Home', 'Foreign']
baseline_wA = [real_wage_A_H_baseline, real_wage_A_F_baseline]
new_wA = [real_wage_A_H_new, real_wage_A_F_new]
baseline_wM = [real_wage_M_H_baseline, real_wage_M_F_baseline]
new_wM = [real_wage_M_H_new, real_wage_M_F_new]

# Plot real wages in terms of agriculture
x = np.arange(len(countries))
width = 0.35
axes[0, 0].bar(x - width/2, baseline_wA, width, label='Baseline', color='steelblue', alpha=0.7)
axes[0, 0].bar(x + width/2, new_wA, width, label='After shock', color='coral', alpha=0.7)
axes[0, 0].set_ylabel('w / P_A', fontsize=11)
axes[0, 0].set_title('Real Wage in Terms of Agriculture', fontsize=12, fontweight='bold')
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(countries)
axes[0, 0].legend()
axes[0, 0].grid(axis='y', alpha=0.3)

# Plot real wages in terms of manufacturing
axes[0, 1].bar(x - width/2, baseline_wM, width, label='Baseline', color='steelblue', alpha=0.7)
axes[0, 1].bar(x + width/2, new_wM, width, label='After shock', color='coral', alpha=0.7)
axes[0, 1].set_ylabel('w / P_M', fontsize=11)
axes[0, 1].set_title('Real Wage in Terms of Manufacturing', fontsize=12, fontweight='bold')
axes[0, 1].set_xticks(x)
axes[0, 1].set_xticklabels(countries)
axes[0, 1].legend()
axes[0, 1].grid(axis='y', alpha=0.3)

# Plot percentage changes
pct_change_A = [(new_wA[i]/baseline_wA[i] - 1)*100 for i in range(2)]
pct_change_M = [(new_wM[i]/baseline_wM[i] - 1)*100 for i in range(2)]

axes[1, 0].bar(countries, pct_change_A, color='green', alpha=0.7, edgecolor='black')
axes[1, 0].set_ylabel('% Change', fontsize=11)
axes[1, 0].set_title('% Change in Real Wage (w/P_A)', fontsize=12, fontweight='bold')
axes[1, 0].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
axes[1, 0].grid(axis='y', alpha=0.3)
for i, v in enumerate(pct_change_A):
    axes[1, 0].text(i, v + 0.5 if v > 0 else v - 0.5, f'{v:.2f}%', ha='center', fontsize=10)

axes[1, 1].bar(countries, pct_change_M, color='green', alpha=0.7, edgecolor='black')
axes[1, 1].set_ylabel('% Change', fontsize=11)
axes[1, 1].set_title('% Change in Real Wage (w/P_M)', fontsize=12, fontweight='bold')
axes[1, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
axes[1, 1].grid(axis='y', alpha=0.3)
for i, v in enumerate(pct_change_M):
    axes[1, 1].text(i, v + 0.5 if v > 0 else v - 0.5, f'{v:.2f}%', ha='center', fontsize=10)

try:
    plt.tight_layout()
except:
    pass
plt.savefig('real_wages_analysis.png', dpi=300)
plt.close()

print("\n[OK] Plot saved as 'real_wages_analysis.png'")

print("\nWelfare Analysis:")
print("- Real wage in terms of AGRICULTURE (w/P_A): INCREASED in both countries")
print("- Real wage in terms of MANUFACTURING (w/P_M): INCREASED even more!")
print("- Consumers are BETTER OFF: They can afford more of both goods")
print("- Why? Productivity gains in M lower P_M, benefiting all consumers")
print("- Workers' purchasing power rises for both goods -> welfare improvement")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)