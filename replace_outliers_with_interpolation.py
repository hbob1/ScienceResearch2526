import numpy as np

def replace_outliers(data, jump_factor=5, tol=1e-6, max_iter=10):
    """
    Replace outliers in a monotonically increasing function with linearly interpolated values.
    Outliers are defined as points where the difference from the previous (accepted/interpolated)
    value is negative or exceeds jump_factor times the median positive increment.
    
    Parameters:
        data (array-like): Input sequence (1D sequence, e.g., list or np.array)
        jump_factor (float): Factor to determine outlier threshold (default 5)
        tol (float): Convergence tolerance
        max_iter (int): Maximum number of iterations
        
    Returns:
        cleaned (np.array): The sequence with outliers replaced by interpolated values.
    """
    data = np.array(data, dtype=np.float64)  # work in float
    cleaned = data.copy()
    
    for iteration in range(max_iter):
        prev_cleaned = cleaned.copy()
        
        # Compute differences between successive points of the current cleaned series.
        diffs = np.diff(cleaned)
        # Only consider positive differences for median calculation.
        positive_diffs = diffs[diffs >= 0]
        median_diff = np.median(positive_diffs) if len(positive_diffs) > 0 else 0

        # Identify outliers (starting at index 1; index 0 always accepted)
        outlier_mask = np.zeros_like(cleaned, dtype=bool)
        for i in range(1, len(cleaned)):
            delta = cleaned[i] - cleaned[i-1]
            # Mark as outlier if the jump is negative or larger than jump_factor*median_diff.
            if delta < 0 or (median_diff > 0 and delta > jump_factor * median_diff):
                outlier_mask[i] = True

        # Replace outlier points with np.nan.
        cleaned[outlier_mask] = np.nan

        # Perform linear interpolation over the NaN positions.
        inds = np.arange(len(cleaned))
        # np.interp ignores NaNs; fill them using non-NaN values.
        # For endpoints, we assume they are not outliers.
        # (If the first or last point is NaN, np.interp will set them to the boundary value.)
        cleaned = np.interp(inds, inds[~np.isnan(cleaned)], cleaned[~np.isnan(cleaned)])
        
        # Check for convergence.
        if np.allclose(cleaned, prev_cleaned, atol=tol, rtol=tol):
            break
    return cleaned

# # ------------------------------------------
# # Example usage:

# # Generate synthetic data that is roughly monotonically increasing
# # Use the function to clean the data.
# cleaned_tot1 = replace_outliers_with_interpolation(tot1, jump_factor=5)
# cleaned_tot2 = replace_outliers_with_interpolation(tot2, jump_factor=5)

# # Plot the original and cleaned sequences.
# plt.figure(figsize=(10, 6))
# plt.plot(tot1, 'o-', label="Original Data")
# plt.plot(cleaned_tot1, 's-', label="Cleaned Data")
# plt.xlabel("Index")
# plt.ylabel("Value")
# plt.title("Monotonic Increasing Function with Outliers Removed")
# plt.legend()
# plt.show()