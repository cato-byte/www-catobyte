# Importing necessary libraries
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FuncFormatter , MaxNLocator

# Sample data: House sizes (in square feet), number of bedrooms, and prices (in Simoleons)
sizes = np.array([140, 230, 110, 160, 200])  # Feature 1 (Size in sq mt)
bedrooms = np.array([2, 3, 1, 2, 3])            # Feature 2 (Number of bedrooms)
prices = np.array([700000, 1000000, 500000, 800000, 950000])  # Target (Price in Simoleons)

# Stack features together (size and number of bedrooms)
X = np.column_stack((sizes, bedrooms))

# Create and fit the linear regression model
model = LinearRegression()
model.fit(X, prices)

# Predict prices for the actual data points (for comparison)
predicted_prices = model.predict(X)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the actual 5 data points
ax.scatter(sizes, bedrooms, prices, color='blue', label='Actual Prices')  # Scatter plot of actual prices

# Generate a mesh grid for the plane to visualize the linear regression plane
size_range = np.linspace(min(sizes), max(sizes), 10)
bathroom_range = np.linspace(min(bedrooms), max(bedrooms), 10)
size_grid, bathroom_grid = np.meshgrid(size_range, bathroom_range)

# Predict prices for the mesh grid (for plane visualization)
price_grid = model.predict(np.column_stack((size_grid.ravel(), bathroom_grid.ravel()))).reshape(size_grid.shape)

# Plot the regression plane
ax.plot_surface(size_grid, bathroom_grid, price_grid, color='red', alpha=0.5)

# Set labels
ax.set_xlabel('Size (sq mt)', labelpad=20)
ax.set_ylabel('Number of bedrooms', labelpad=20)
ax.set_zlabel('Price (Simoleons)', labelpad=20)
ax.set_title('House Prices vs Size and bedrooms with Linear Regression')

# Set the z-axis limits (price range) from 500,000 to 1,000,000
ax.set_zlim(500000, 1000000)

# Format the z-axis ticks to avoid scientific notation
ax.zaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# Ensure the Y-axis (number of bedrooms) only shows whole numbers
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# Move the z-axis tick labels (prices) to the left by increasing the pad value
ax.tick_params(axis='z', pad=10)  # Adjust the pad value to control distance

# Show the plot
plt.legend()
#plt.show()

plt.savefig('understanding_neural_networks_3d_linear_reg_example.png')  # You can change the file format by changing the extension (e.g., .jpg, .pdf)
