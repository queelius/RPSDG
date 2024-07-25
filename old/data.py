import numpy as np
from scipy.stats import ortho_group
from typing import Callable, Tuple
import sympy as sp
from scipy.optimize import minimize

class FunctionGenerator:
    def __init__(self, n_dims: int):
        self.n_dims = n_dims
        self.symbols = sp.symbols(f'x:{self.n_dims}')

    def generate_optimum(self) -> np.ndarray:
        return np.round(np.random.uniform(-10, 10, self.n_dims), 3)

    def basic_function(self, optimum: np.ndarray) -> Tuple[Callable, sp.Expr]:
        # Add a non-zero constant to ensure the global minimum is not zero
        constant = round(np.random.uniform(1, 10), 2)
        expr = sum((xi - ai)**2 for xi, ai in zip(self.symbols, optimum)) + constant
        return lambda x: expr.subs(dict(zip(self.symbols, x))).evalf(), expr

    def apply_rotation(self, func_expr: Tuple[Callable, sp.Expr], optimum: np.ndarray) -> Tuple[Callable, sp.Expr, np.ndarray]:
        func, expr = func_expr
        R = np.round(ortho_group.rvs(self.n_dims), 3)
        new_optimum = np.round(R @ optimum, 3)
        rotated_symbols = R @ sp.Matrix(self.symbols)
        rotated_expr = expr.subs(dict(zip(self.symbols, rotated_symbols)))
        rounded_expr = self.round_expr(rotated_expr, 3)
        return lambda x: rounded_expr.subs(dict(zip(self.symbols, x))).evalf(), rounded_expr, new_optimum

    def generate_function(self) -> Tuple[Callable, np.ndarray, sp.Expr]:
        optimum = self.generate_optimum()
        f, expr = self.basic_function(optimum)
        f, expr, optimum = self.apply_rotation((f, expr), optimum)
        return f, optimum, expr

def try_sympy_solve(expr, symbols):
    try:
        solution = sp.solve(sp.diff(expr, symbols), symbols)
        return solution
    except Exception:
        return None

def optimize_function(f, initial_guess, bounds):
    result = minimize(f, initial_guess, method='L-BFGS-B', bounds=bounds)
    return result.x, result.fun

def generate_dataset(n_problems, n_dims):
    generator = FunctionGenerator(n_dims)
    dataset = []
    for _ in range(n_problems):
        f, optimum, expr = generator.generate_function()
        dataset.append((f, optimum, expr))
    return dataset

if __name__ == "__main__":
    np.random.seed()  # Ensures we get different random numbers each time
    generator = FunctionGenerator(n_dims=2)
    bounds = [(-20, 20)] * generator.n_dims
    
    # Generate 3 problems in 2 dimensions
    print("\nGenerating a small dataset:")
    dataset = generate_dataset(3, 2)
    for i, (f, optimum, expr) in enumerate(dataset):
        print(f"\nProblem {i+1}:")
        print(f"Optimum: {optimum}")
        print(f"Function definition:\n{expr}")
        print(f"Function value at optimum: {f(optimum):.6f}")
        
        sympy_solution = try_sympy_solve(expr, generator.symbols)
        if sympy_solution:
            print("SymPy found an analytical solution:")
            print(sympy_solution)
        else:
            print("SymPy couldn't find an analytical solution.")
        
        # Optimization attempt
        initial_guess = optimum + np.random.normal(0, 1, generator.n_dims)
        found_optimum, found_value = optimize_function(f, initial_guess, bounds)
        print(f"Optimization result:")
        print(f"Found optimum: {np.round(found_optimum, 4)}")
        print(f"Found value: {found_value:.6f}")
        print(f"Distance from true optimum: {np.linalg.norm(found_optimum - optimum):.6f}")
