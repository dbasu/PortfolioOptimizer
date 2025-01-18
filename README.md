```markdown
# Portfolio Optimizer

**Portfolio Optimizer** is a Python package designed to solve the **mean-variance portfolio optimization** problem in quantitative finance. This package allows for optimization with the ability to apply constraints at both the asset and factor levels. It provides different methods for portfolio optimization, including closed-form solutions, heuristic methods, and optimization algorithms.

## Features

- Solve **mean-variance portfolio optimization** problem.
- Support for **asset-level** and **factor-level** constraints.
- Three optimization methods:
  - **AnalyticOptimization**: Uses a closed-form solution for mean-variance optimization and heuristics for applying constraints.
  - **ScipyOptimization**: Utilizes SciPy’s optimization algorithms to solve the problem.
  - **CVXOptimizer**: Solves convex and second-order cone programming (SOCP) problems.

## Installation

To install the **Portfolio Optimizer** package, you can use `pip`:

```bash
pip install portfolio-optimizer
```

## Usage

The package provides a base class `PortfolioOptimization` that defines the core structure for optimization. There are three derived classes for different optimization approaches:

### 1. **AnalyticOptimization** (Closed-form solution)

This approach uses the closed-form solution for mean-variance optimization and applies heuristics to handle constraints.

```python
from portfolio_optimizer import AnalyticOptimization

# Example usage
optimizer = AnalyticOptimization(expected_returns, covariance_matrix)
optimizer.set_constraints(asset_constraints, factor_constraints)
optimal_weights = optimizer.optimize()
```

### 2. **ScipyOptimization** (SciPy-based optimization)

This class utilizes SciPy's optimization library to solve the mean-variance optimization problem.

```python
from portfolio_optimizer import ScipyOptimization

# Example usage
optimizer = ScipyOptimization(expected_returns, covariance_matrix)
optimizer.set_constraints(asset_constraints, factor_constraints)
optimal_weights = optimizer.optimize()
```

### 3. **CVXOptimizer** (Convex & SOCP optimization)

This class is used for solving optimization problems that can be formulated as convex or second-order cone programming (SOCP) problems, using the CVXPY library.

```python
from portfolio_optimizer import CVXOptimizer

# Example usage
optimizer = CVXOptimizer(expected_returns, covariance_matrix)
optimizer.set_constraints(asset_constraints, factor_constraints)
optimal_weights = optimizer.optimize()
```

## API

### `PortfolioOptimization` Class

This is the base class for all optimization strategies. The general interface includes:

- `set_constraints(self, asset_constraints, factor_constraints)`: Set asset-level and factor-level constraints.
- `optimize(self)`: Solve the optimization problem and return the optimal portfolio weights.

### `AnalyticOptimization` Class

- Inherits from `PortfolioOptimization`.
- Uses a closed-form solution for mean-variance optimization and applies heuristics to handle constraints.

### `ScipyOptimization` Class

- Inherits from `PortfolioOptimization`.
- Uses SciPy's optimization functions for solving the problem.

### `CVXOptimizer` Class

- Inherits from `PortfolioOptimization`.
- Uses the **CVXPY** library to solve convex and SOCP problems.

## Constraints

The package allows for both **asset-level** and **factor-level** constraints.

- **Asset-level constraints**: These include limits on the individual assets' weight (e.g., minimum and maximum allocation, no short selling, etc.).
- **Factor-level constraints**: These include constraints on factors like sector exposure, risk, and other relevant financial factors.

## Examples

```python
from portfolio_optimizer import AnalyticOptimization
import numpy as np

# Example data: Expected returns and covariance matrix
expected_returns = np.array([0.12, 0.18, 0.08])  # Example returns for 3 assets
covariance_matrix = np.array([[0.1, 0.03, 0.05],  # Covariance matrix
                              [0.03, 0.12, 0.07],
                              [0.05, 0.07, 0.15]])

# Create the optimizer object
optimizer = AnalyticOptimization(expected_returns, covariance_matrix)

# Set asset and factor constraints (example)
asset_constraints = {"min_weight": 0.05, "max_weight": 0.5}
factor_constraints = {"max_risk": 0.2}

# Apply constraints and optimize
optimizer.set_constraints(asset_constraints, factor_constraints)
optimal_weights = optimizer.optimize()

print("Optimal Portfolio Weights:", optimal_weights)
```

## Requirements

- Python 3.x
- `numpy` (for array and matrix operations)
- `scipy` (for optimization tasks)
- `cvxpy` (for convex optimization)
  
You can install the required dependencies using:

```bash
pip install numpy scipy cvxpy
```

## Contributing

Contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Create a new pull request.

Please ensure that your code adheres to the coding standards and includes relevant tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to use this package as part of your quantitative portfolio optimization workflows. If you have any questions or need further support, please open an issue or submit a pull request!
```

This is the complete README in Markdown format.