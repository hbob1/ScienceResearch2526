import numpy as np
from scipy import stats

delta = np.array([
    1.84, 1.49, -0.71, 0.64, 1.44, -0.04,
   -0.43, 0.98, 0.21, 1.68, 1.93, 0.68
])

percent = np.array([
    25.6, 20.19, -4.46, 11.41, 10.1, -0.51,
   -4.05, 14.76, 2.57, 13.97, 11.24, 8.35
])

t_stat_delta, p_value_delta = stats.ttest_1samp(delta, 0)
t_stat_percent, p_value_percent = stats.ttest_1samp(percent, 0)

mean = percent.mean()
sem = stats.sem(percent)  # standard error of the mean

ci_low, ci_high = stats.t.interval(
    0.95,
    len(percent)-1,
    loc=mean,
    scale=sem
)

w_stat, p_wilcoxon = stats.wilcoxon(percent)

print("Wilcoxon W =", w_stat)
print("Wilcoxon p =", p_wilcoxon)

print("95% CI:", (str(ci_low), str(ci_high)))

d = delta.mean() / delta.std(ddof=1)
print("Cohen's d =", d)

print("t_delta =", t_stat_delta)
print("p_delta =", p_value_delta)

print("t_percent =", t_stat_percent)
print("p_percent =", p_value_percent)




