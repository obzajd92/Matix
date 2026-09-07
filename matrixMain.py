import numpy as np

# 1. Define a 3x3 Matrix representing an operator in 3D space
# (Change the values below to fit your specific matrix)
A = np.array([
    [2,  1, -1],
    [-3,  4,  2],
    [1,  1,  5]
])

# 2. Define a 3D Vector to demonstrate axis projections
v = np.array([3, 4, 5])

# --- Calculations ---

# Trace (sum of diagonal elements)
matrix_trace = np.trace(A)

# Rank (number of linearly independent rows/columns)
matrix_rank = np.linalg.matrix_rank(A)

# Matrix Norms 
norm_l1  = np.linalg.norm(A, ord=1)        # Maximum absolute column sum
norm_l2  = np.linalg.norm(A, ord=2)        # Spectral norm (largest singular value)
norm_inf = np.linalg.norm(A, ord=np.inf)   # Maximum absolute row sum

# Determinant
matrix_det = np.linalg.det(A)

# Projections onto X, Y, and Z axes
# Extracting or isolating the respective coordinate while zeroing out the rest
proj_x = np.array([v[0], 0, 0])
proj_y = np.array([0, v[1], 0])
proj_z = np.array([0, 0, v[2]])

# --- Print Results ---
print("=== Matrix Properties ===")
print(f"Matrix:\n{A}\n")
print(f"Trace:        {matrix_trace}")
print(f"Rank:         {matrix_rank}")
print(f"L1 Norm:      {norm_l1}")
print(f"L2 Norm:      {norm_l2:.4f}")
print(f"L-infinity:   {norm_inf}")
print(f"Determinant:  {matrix_det:.4f}")
