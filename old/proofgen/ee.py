from dataclasses import dataclass
from typing import Union, Optional, List

# AST node types
@dataclass
class Expression:
    pass

@dataclass
class Number(Expression):
    value: int

@dataclass
class Variable(Expression):
    name: str

@dataclass
class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression

@dataclass
class UnaryOp(Expression):
    op: str
    expr: Expression

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
    def apply(self, expr: Expression) -> Expression:
        return expr

class EvalRule(Rule):
    def apply(self, expr: Expression) -> Expression:
        if isinstance(expr, BinaryOp):
            left = self.apply(expr.left)
            right = self.apply(expr.right)
            if isinstance(left, Number) and isinstance(right, Number):
                if expr.op == '+':
                    return Number(left.value + right.value)
                elif expr.op == '*':
                    return Number(left.value * right.value)
        elif isinstance(expr, UnaryOp):
            sub_expr = self.apply(expr.expr)
            if isinstance(sub_expr, Number) and expr.op == 'pow':
                return Number(sub_expr.value ** 2)  # Simplifying power for demonstration
        return expr

class PowerOfProductRule(Rule):
    def apply(self, expr: Expression) -> Expression:
        if isinstance(expr, UnaryOp) and expr.op == 'pow':
            if isinstance(expr.expr, BinaryOp) and expr.expr.op == '*':
                base1 = self.apply(expr.expr.left)
                base2 = self.apply(expr.expr.right)
                return BinaryOp('*', UnaryOp('pow', base1), UnaryOp('pow', base2))
        return expr

class ProofGenerator:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
    
    def generate_proof(self, expr: Expression) -> Expression:
        current_expr = expr
        print("Initial expression:", printer.to_string(current_expr))
        for rule in self.rules:
            new_expr = rule.apply(current_expr)
            if new_expr != current_expr:  # Check if transformation occurred
                print(f"After applying {rule.__class__.__name__}:", printer.to_string(new_expr))
                current_expr = new_expr
        return current_expr

# Instantiate rules and expression printer
printer = ExpressionPrinter()
rules = [EvalRule(), PowerOfProductRule()]
generator = ProofGenerator(rules)

# Example complex expression
expr = BinaryOp('+', BinaryOp('*', Number(3), UnaryOp('pow', BinaryOp('*', Variable('x'), Variable('y')))), Number(7))

# Generate proof
result_expr = generator.generate_proof(expr)
print("Final transformed expression:", printer.to_string(result_expr))
