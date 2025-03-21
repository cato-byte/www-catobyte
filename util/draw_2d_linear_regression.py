# Importing necessary libraries
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Sample data: House sizes (in square feet) and prices
sizes = np.array([140, 230, 110, 160, 200]).reshape(-1, 1)  # Feature (Size in sq mt)
prices = np.array([700000, 1000000, 500000, 800000, 950000])  # Target (Price in Simoleons)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(sizes, prices)

# Predict prices for the fitted line
predicted_prices = model.predict(sizes)

# Plotting the points and the regression line
plt.scatter(sizes, prices, color='blue', label='Actual Prices')  # Scatter plot of actual prices
plt.plot(sizes, predicted_prices, color='red', label='Regression Line')  # Linear regression line

# Adding labels and title
plt.xlabel('Size (sq mt)')
plt.ylabel('Price (Simoleons) §')
plt.title('House Prices vs Size with Linear Regression')
plt.legend()

# Show grid
plt.grid(True)

plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# Save the plot to a file (PNG format)
plt.savefig('understanding_neural_networks_2d_linear_reg_example.png')  # You can change the file format by changing the extension (e.g., .jpg, .pdf)

# To visualize in the script itself, use plt.show(), but it is not necessary for saving the file.
#plt.show()