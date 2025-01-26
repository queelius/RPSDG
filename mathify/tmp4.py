import sympy as sp
import random

# Define the symbol
x = sp.symbols('x')

# Step 1: Generate More Complex Functions Randomly
def generate_complex_function():
    # Define possible function components
    base_functions = [
        lambda x: x**random.randint(2, 5),
        lambda x: sp.exp(random.randint(2, 10)*x),
        lambda x: sp.sin(random.randint(1, 10)*x),
        lambda x: sp.cos(random.randint(1, 10)*x),
        lambda x: sp.tan(random.randint(1, 10)*x),
        lambda x: sp.log(x),
        lambda x: sp.sqrt(x),
        lambda x: sp.asin(x),
        lambda x: sp.acos(x),
        lambda x: sp.atan(x),
        lambda x: sp.sinh(x),
        lambda x: sp.cosh(x),
        lambda x: sp.tanh(x),
        lambda x: sp.erf(x),  # Error function
    ]
    

    # Randomly generate a function consisting of a random 4 functions
    num_terms = 4
    f_xs = []
    for _ in range(num_terms):
        # Randomly select and compose functions
        num_layers = random.randint(2, 10)  # Depth of composition
        f_x = x
        for _ in range(num_layers):
            func = random.choice(base_functions)
            f_x = func(f_x)

    return f_x

# Step 2: Custom Differentiation Function with Step Recording
def differentiate_with_steps(expr):
    steps = []
    
    def diff(expr, var):
        if expr.is_Atom:
            # Derivative of constants and variables
            if expr == var:
                steps.append(f"The derivative of \( {sp.latex(expr)} \) with respect to \( {sp.latex(var)} \) is 1.")
                return sp.Integer(1)
            else:
                steps.append(f"The derivative of constant \( {sp.latex(expr)} \) is 0.")
                return sp.Integer(0)
        elif expr.is_Add:
            # Sum rule
            derivatives = []
            for arg in expr.args:
                derivative = diff(arg, var)
                derivatives.append(derivative)
            result = sum(derivatives)
            steps.append(f"Using sum rule, the derivative of \( {sp.latex(expr)} \) is \( {sp.latex(result)} \).")
            return result
        elif expr.is_Mul:
            # Product rule
            terms = expr.args
            derivatives = []
            for i, term in enumerate(terms):
                d_term = diff(term, var)
                other_terms = sp.Mul(*(terms[:i] + terms[i+1:]))
                derivative = d_term * other_terms
                derivatives.append(derivative)
                steps.append(f"Applying product rule, differentiating \( {sp.latex(term)} \), we get \( {sp.latex(derivative)} \).")
            result = sum(derivatives)
            steps.append(f"The derivative of the product \( {sp.latex(expr)} \) is \( {sp.latex(result)} \).")
            return result
        elif expr.is_Pow:
            # Power rule and chain rule
            base, exponent = expr.as_base_exp()
            if base.has(var) and exponent.has(var):
                # Both base and exponent depend on var
                derivative = sp.diff(expr, var)
                steps.append(f"Derivative of \( {sp.latex(expr)} \) using general differentiation is \( {sp.latex(derivative)} \).")
                return derivative
            elif exponent.has(var):
                # Exponent depends on variable
                ln_base = sp.log(base)
                d_exponent = diff(exponent, var)
                derivative = expr * (ln_base * d_exponent)
                steps.append(f"Using chain rule for exponent \( {sp.latex(exponent)} \), the derivative is \( {sp.latex(derivative)} \).")
                return derivative
            elif base.has(var):
                d_base = diff(base, var)
                derivative = exponent * base**(exponent - 1) * d_base
                steps.append(f"Using power rule, the derivative of \( {sp.latex(expr)} \) is \( {sp.latex(derivative)} \).")
                return derivative
            else:
                steps.append(f"The derivative of constant \( {sp.latex(expr)} \) is 0.")
                return sp.Integer(0)
        elif expr.is_Function:
            # Chain rule for functions
            inner = expr.args[0]
            d_inner = diff(inner, var)
            # Use a dummy symbol to compute the derivative of the outer function
            u = sp.Symbol('u')
            outer_func = expr.func(u)
            derivative_outer = sp.diff(outer_func, u).subs(u, inner)
            derivative = derivative_outer * d_inner
            steps.append(f"Using chain rule, the derivative of \( {sp.latex(expr)} \) is:")
            steps.append(f"Compute the derivative of the outer function:")
            steps.append(f"\( \\frac{{d}}{{du}} {sp.latex(outer_func)} = {sp.latex(sp.diff(outer_func, u))} \)")
            steps.append(f"Substitute back \( u = {sp.latex(inner)} \):")
            steps.append(f"\( \\frac{{d}}{{du}} {sp.latex(outer_func)} \\bigg|_{{u={sp.latex(inner)}}} = {sp.latex(derivative_outer)} \)")
            steps.append(f"Multiply by the derivative of the inner function:")
            steps.append(f"\( {sp.latex(derivative_outer)} \\times {sp.latex(d_inner)} = {sp.latex(derivative)} \)")
            return derivative
        else:
            derivative = sp.diff(expr, var)
            steps.append(f"Derivative of \( {sp.latex(expr)} \) is \( {sp.latex(derivative)} \).")
            return derivative
        
    derivative = diff(expr, x)
    return derivative, steps

# Step 3: Reverse Differentiation Steps to Simulate Integration Steps
def reverse_steps(steps):
    reversed_steps = steps[::-1]
    integration_steps = []
    for step in reversed_steps:
        # Reverse the logic of differentiation steps to integration steps
        if "derivative of constant" in step:
            integration_steps.append(step.replace("derivative of constant", "integral of zero is constant").replace("is 0", "is a constant"))
        elif "Compute the derivative of the outer function" in step:
            integration_steps.append(step.replace("Compute the derivative of the outer function", "Find the antiderivative of the outer function"))
        elif "Using chain rule" in step:
            integration_steps.append(step.replace("Using chain rule, the derivative", "Using substitution, the integral"))
        elif "Applying product rule" in step:
            integration_steps.append(step.replace("Applying product rule, differentiating", "Using integration by parts on"))
        elif "Using sum rule" in step:
            integration_steps.append(step.replace("Using sum rule, the derivative", "Using linearity, the integral"))
        elif "power rule" in step:
            integration_steps.append(step.replace("Using power rule, the derivative", "Using power rule, the integral"))
        else:
            integration_steps.append(step.replace("derivative", "integral").replace("Derivative", "Integral"))
    return integration_steps

# Step 4: Automate the Entire Process
def generate_problem():
    # Generate a complex function f(x)
    f_x = generate_complex_function()
    
    # Differentiate f(x) with steps
    f_prime, diff_steps = differentiate_with_steps(f_x)
    
    # Reverse the differentiation steps to simulate integration steps
    integration_steps = reverse_steps(diff_steps)
    
    # Output the problem and solutions
    print("### Integration Problem\n")
    print(f"Given the derivative:\n")
    print(f"$$ f'(x) = {sp.latex(f_prime)} $$\n")
    print("**Chain-of-Thought Solution:**\n")
    for step in integration_steps:
        print(f"{step}\n")
    print(f"**Final Answer:**\n")
    print(f"$$ f(x) = {sp.latex(f_x)} + C $$\n")
    print("="*80)

# Generate a single problem for testing
generate_problem()
