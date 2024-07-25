from dataclasses import dataclass
from typing import List, Union, Optional
import random

debug = False

# AST node types
@dataclass
class Number:
    value: Union[int, float]

@dataclass
class Variable:
    name: str

@dataclass
class BinaryOp:
    op: str
    left: 'Expression'
    right: 'Expression'

@dataclass
class UnaryOp:
    op: str
    expr: 'Expression'

Expression = Union[Number, Variable, BinaryOp, UnaryOp]

class ExpressionPrinter:
    def to_string(self, expr: Expression) -> str:
        if isinstance(expr, Number):
            return str(expr.value)
        elif isinstance(expr, Variable):
            return expr.name
        elif isinstance(expr, BinaryOp):
            return f"({self.to_string(expr.left)} {expr.op} {self.to_string(expr.right)})"
        elif isinstance(expr, UnaryOp):
            return f"{expr.op}({self.to_string(expr.expr)})"

class Rule:
    def __init__(self, name: str, pattern: Expression, replacement: Expression, evaluate: bool = False):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement
        self.evaluate = evaluate  # flag to indicate if evaluation should be performed
    
    def apply(self, expr: Expression) -> Optional[Expression]:
        # Apply rule to the root of the expression
        new_expr = self._apply_to_root(expr)
        if new_expr:
            return new_expr

        # Recursively apply rule to sub-expressions
        if isinstance(expr, BinaryOp):
            left = self.apply(expr.left)
            right = self.apply(expr.right)
            if left or right:
                return BinaryOp(expr.op, left if left else expr.left, right if right else expr.right)
        elif isinstance(expr, UnaryOp):
            sub_expr = self.apply(expr.expr)
            if sub_expr:
                return UnaryOp(expr.op, sub_expr)

        return None

    def _apply_to_root(self, expr: Expression) -> Optional[Expression]:
        bindings = {}
        if self.match(expr, self.pattern, bindings):
            return self.instantiate(self.replacement, bindings)
        return None

    def match(self, expr: Expression, pattern: Expression, bindings: dict) -> bool:
        if debug:
            print(f"Matching {expr} with {pattern}")
        if isinstance(pattern, Variable):
            if pattern.name in bindings:
                return self.match(expr, bindings[pattern.name], {})
            bindings[pattern.name] = expr
            if debug:
                print(f"Bound variable {pattern.name} to {expr}")
            return True
        elif isinstance(pattern, Number) and isinstance(expr, Number):
            return pattern.value == expr.value
        elif isinstance(pattern, BinaryOp) and isinstance(expr, BinaryOp):
            if pattern.op == expr.op:
                # Special case for x + x or similar
                if (isinstance(pattern.left, Variable) and isinstance(pattern.right, Variable) and 
                    pattern.left.name == pattern.right.name):
                    # Both sides must match the same expression
                    return self.match(expr.left, pattern.left, bindings) and expr.left == expr.right
                return (self.match(expr.left, pattern.left, bindings) and
                        self.match(expr.right, pattern.right, bindings))
        elif isinstance(pattern, UnaryOp) and isinstance(expr, UnaryOp):
            return pattern.op == expr.op and self.match(expr.expr, pattern.expr, bindings)
        return False

    def instantiate(self, template: Expression, bindings: dict) -> Expression:
        if isinstance(template, Variable):
            return bindings.get(template.name, template)
        elif isinstance(template, Number):
            return template
        elif isinstance(template, BinaryOp):
            left = self.instantiate(template.left, bindings)
            right = self.instantiate(template.right, bindings)
            if self.evaluate and isinstance(left, Number) and isinstance(right, Number):
                if template.op == '+':
                    return Number(left.value + right.value)
                elif template.op == '-':
                    return Number(left.value - right.value)
                elif template.op == '*':
                    return Number(left.value * right.value)
                elif template.op == '/':
                    return Number(left.value / right.value)
            return BinaryOp(template.op, left, right)
        elif isinstance(template, UnaryOp):
            expr = self.instantiate(template.expr, bindings)
            if self.evaluate and isinstance(expr, Number):
                if template.op == '-':
                    return Number(-expr.value)
            return UnaryOp(template.op, expr)

class ProofGenerator:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
    
    def random_walk(self, start_expression: Expression, steps: int) -> List[tuple[str, Expression]]:
        current = start_expression
        proof = [("Initial", current)]
        for _ in range(steps):
            random.shuffle(self.rules)
            applicable_rules = [rule for rule in self.rules if rule.apply(current) is not None]
            if not applicable_rules:
                break
            rule = random.choice(applicable_rules)
            new_expression = rule.apply(current)
            if new_expression is not None:
                proof.append((rule.name, new_expression))
                current = new_expression
        return proof

def generate_random_expression(depth: int) -> Expression:
    if depth == 0 or random.random() < 0.5:
        return random.choice([Number(random.randint(1, 10)), Variable(chr(random.randint(97, 122)))])
    else:
        op = random.choice(["+", "-", "*", "/"])
        left = generate_random_expression(depth - 1)
        right = generate_random_expression(depth - 1)
        return BinaryOp(op, left, right)

# Define rules using AST expressions
simple_rules = [
    Rule("Commutativity of Addition",
         BinaryOp("+", Variable("A"), Variable("B")),
         BinaryOp("+", Variable("B"), Variable("A"))),
    Rule("Commutativity of Multiplication",
         BinaryOp("*", Variable("A"), Variable("B")),
         BinaryOp("*", Variable("B"), Variable("A"))),
    Rule("Associativity of Addition",
         BinaryOp("+", BinaryOp("+", Variable("A"), Variable("B")), Variable("C")),
         BinaryOp("+", Variable("A"), BinaryOp("+", Variable("B"), Variable("C")))),
    Rule("Distributive Property",
         BinaryOp("*", Variable("A"), BinaryOp("+", Variable("B"), Variable("C"))),
         BinaryOp("+", BinaryOp("*", Variable("A"), Variable("B")), BinaryOp("*", Variable("A"), Variable("C")))),
    Rule("Identity of Addition",
         BinaryOp("+", Variable("A"), Number(0)),
         Variable("A")),
    Rule("Identity of Multiplication",
         BinaryOp("*", Variable("A"), Number(1)),
         Variable("A")),
    Rule("Negation",
         UnaryOp("-", Variable("A")),
         BinaryOp("-", Number(0), Variable("A"))),
    Rule("Double Negation",
         UnaryOp("-", UnaryOp("-", Variable("A"))),
         Variable("A")),
    Rule("Additive Inverse",
         BinaryOp("+", Variable("A"), UnaryOp("-", Variable("A"))),
         Number(0)),
    Rule("Multiplicative Inverse",
         BinaryOp("*", Variable("A"), BinaryOp("/", Number(1), Variable("A"))),
         Number(1)),
    Rule("Rewrite 1 as X/X",
         Number(1),
         BinaryOp("/", Variable("X"), Variable("X"))),
    Rule("Rewrite -4 as -1 * 4",
         Number(-4),
         BinaryOp("*", Number(-1), Number(4))),
    Rule("Rewrite x + x as 2*x",
         BinaryOp("+", Variable("x"), Variable("x")),
         BinaryOp("*", Number(2), Variable("x"))),
    Rule("Evaluate Addition",
         BinaryOp("+", Variable("A"), Variable("B")),
         BinaryOp("+", Variable("A"), Variable("B")),  # pattern and replacement are the same
         evaluate=True),
    Rule("Evaluate Multiplication",
         BinaryOp("*", Variable("A"), Variable("B")),
         BinaryOp("*", Variable("A"), Variable("B")),  # pattern and replacement are the same
         evaluate=True),
    Rule("Eval",
         Variable("X"),
         Variable("X"),
         evaluate=True)
]

def evaluate_expression(expr: Expression) -> Expression:
    if isinstance(expr, BinaryOp):
        left = evaluate_expression(expr.left)
        right = evaluate_expression(expr.right)
        if isinstance(left, Number) and isinstance(right, Number):
            if expr.op == '+':
                return Number(left.value + right.value)
            elif expr.op == '-':
                return Number(left.value - right.value)
            elif expr.op == '*':
                return Number(left.value * right.value)
            elif expr.op == '/':
                return Number(left.value / right.value)
        return BinaryOp(expr.op, left, right)
    elif isinstance(expr, UnaryOp):
        sub_expr = evaluate_expression(expr.expr)
        if isinstance(sub_expr, Number):
            if expr.op == '-':
                return Number(-sub_expr.value)
        return UnaryOp(expr.op, sub_expr)
    return expr

# Test expressions using AST
test_expressions = [
    BinaryOp("*", BinaryOp("+", Variable("a"), Variable("a")), Number(4)),
    BinaryOp("*", BinaryOp("+", Variable("a"), Variable("a")), Variable("a")),
    BinaryOp("*", Number(2), BinaryOp("*", Number(3), Variable("x"))),
    BinaryOp("+", Number(2), Number(3)),
    BinaryOp("*", BinaryOp("+", Number(2), Number(3)), Number(4)),
    BinaryOp("+", Number(1), BinaryOp("*", Number(2), Number(3))),
    BinaryOp("+", BinaryOp("*", Variable("a"), Variable("b")), BinaryOp("*", Variable("a"), Variable("c"))),
    BinaryOp("+", Variable("x"), BinaryOp("+", Variable("y"), Variable("z"))),
    BinaryOp("+", Number(2), BinaryOp("+", Number(3), Number(4))),
]

# Run tests
printer = ExpressionPrinter()
generator = ProofGenerator(simple_rules)

for expr in test_expressions:
    print(f"\nStarting expression: {printer.to_string(expr)}")
    proof = generator.random_walk(expr, 10)  # Generate 10 steps
    
    print("Proof:")
    for step, expr in proof:
        print(f"{step}: {printer.to_string(expr)}")

# Generate and test random expressions
for _ in range(3):
    random_expr = generate_random_expression(3)  # Adjust depth as needed
    print(f"\nStarting random expression: {printer.to_string(random_expr)}")
    proof = generator.random_walk(random_expr, 10)  # Generate 10 steps
    
    print("Proof:")
    for step, expr in proof:
        print(f"{step}: {printer.to_string(expr)}")
