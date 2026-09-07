import numpy as np
from scipy.linalg import svd
from sklearn.decomposition import PCA

# 1. Define a sample 3D square matrix (3x3)
# (Treating rows as data samples in a 3D space)
A = np.array([
    [3.0, 2.0, 4.0],
    [2.0, 0.0, 2.0],
    [4.0, 2.0, 3.0]
])

print("--- Original Matrix A ---")
print(A)

# 2. Trace
# Sum of diagonal elements: 3 + 0 + 3 = 6
matrix_trace = np.trace(A)

# 3. Rank
# Number of linearly independent rows/columns
matrix_rank = np.linalg.matrix_rank(A)

# 4. Matrix Norms
# L1 Norm: Maximum absolute column sum
norm_l1 = np.linalg.norm(A, ord=1)
# L2 Norm: Spectral norm (maximum singular value)
norm_l2 = np.linalg.norm(A, ord=2)
# L-infinity Norm: Maximum absolute row sum
norm_inf = np.linalg.norm(A, ord=np.inf)

# 5. Determinant
matrix_det = np.linalg.det(A)

# 6. Projections onto X, Y, and Z axes/planes in 3D space
# Standard projection matrices setting other coordinates to 0
P_x = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
P_y = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
P_z = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])

proj_x = P_x @ A
proj_y = P_y @ A
proj_z = P_z @ A

# 7. Singular Value Decomposition (SVD)
# Decomposes A into U (left singular), S (singular values), Vt (right singular transpose)
U, S, Vt = svd(A)

# 8. Principal Component Analysis (PCA)
# Reduces features/dimensions based on maximum variance
pca = PCA(n_components=3)
A_pca = pca.fit_transform(A)

# --- Display Results ---
print(f"\nTrace: {matrix_trace}")
print(f"Rank: {matrix_rank}")
print(f"Norm L1: {norm_l1} | Norm L2: {norm_l2:.4f} | Norm L-infinity: {norm_inf}")
print(f"Determinant: {matrix_det:.4f}")

print("\n--- Projections ---")
print("Projection on X:\n", proj_x)
print("Projection on Y:\n", proj_y)
print("Projection on Z:\n", proj_z)

print("\n--- Singular Value Decomposition (SVD) ---")
print("Singular Values (S):", S)

print("\n--- Principal Component Analysis (PCA) ---")
print("Transformed PCA coordinates:\n", A_pca)
print("Explained Variance Ratio:", pca.explained_variance_ratio_)
