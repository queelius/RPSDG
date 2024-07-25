from dataclasses import dataclass
from typing import Union, Optional, Dict, Any, List

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
        # This method should be overridden in derived classes
        return expr

class ZeroMultiplicationRule(Rule):
    def apply(self, expr: Expression) -> Expression:
        if isinstance(expr, BinaryOp) and expr.op == '*':
            if isinstance(expr.left, Number) and expr.left.value == 0 or \
               isinstance(expr.right, Number) and expr.right.value == 0:
                return Number(0)
        return expr

class PowerOfProductRule(Rule):
    def apply(self, expr: Expression) -> Expression:
        if isinstance(expr, UnaryOp) and expr.op == 'pow' and isinstance(expr.expr, BinaryOp) and expr.expr.op == '*':
            base1 = expr.expr.left
            base2 = expr.expr.right
            return BinaryOp('*', UnaryOp('pow', base1), UnaryOp('pow', base2))
        return expr

class EvalRule(Rule):
    def apply(self, expr: Expression) -> Expression:
        if isinstance(expr, BinaryOp):
            if expr.op == '+':
                left = self.apply(expr.left)
                right = self.apply(expr.right)
                if isinstance(left, Number) and isinstance(right, Number):
                    return Number(left.value + right.value)
            elif expr.op == '*':
                left = self.apply(expr.left)
                right = self.apply(expr.right)
                if isinstance(left, Number) and isinstance(right, Number):
                    return Number(left.value * right.value)
        return expr

class GeneralRule(Rule):
    def apply(self, expr: Expression) -> Expression:
        if isinstance(expr, BinaryOp) and expr.op == '+':
            # Count how many times the same expression appears
            count = self.count_repeats(expr)
            if count > 1:
                return BinaryOp('*', Number(count), self.apply(expr.left))
        return super().apply(expr)

    def count_repeats(self, expr: Expression, count: int = 1) -> int:
        if isinstance(expr, BinaryOp) and expr.op == '+':
            if expr.left == expr.right:
                return self.count_repeats(expr.left, count + 1)
        return count

class ProofGenerator:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
    
    def generate_proof(self, expr: Expression) -> Expression:
        for rule in self.rules:
            expr = rule.apply(expr)
        return expr

# Instantiate rules and expression printer
printer = ExpressionPrinter()
rules = [EvalRule(), GeneralRule(), ZeroMultiplicationRule(), PowerOfProductRule()]
generator = ProofGenerator(rules)

# Example expressions with complex nested structures
expr1 = BinaryOp('*', UnaryOp('pow', BinaryOp('+', Number(2), Number(3))), Number(0))
expr2 = UnaryOp('pow', BinaryOp('*', BinaryOp('+', Variable('a'), Variable('b')), BinaryOp('+', Variable('c'), Variable('d'))))
expr3 = BinaryOp('+', BinaryOp('*', Number(3), UnaryOp('pow', BinaryOp('*', Variable('x'), Variable('y')))), Number(7))

# Generate proofs for complex expressions
print("Starting expression:", printer.to_string(expr1))
result_expr1 = generator.generate_proof(expr1)
print("Transformed expression:", printer.to_string(result_expr1))

print("\nStarting expression:", printer.to_string(expr2))
result_expr2 = generator.generate_proof(expr2)
print("Transformed expression:", printer.to_string(result_expr2))

print("\nStarting expression:", printer.to_string(expr3))
result_expr3 = generator.generate_proof(expr3)
print("Transformed expression:", printer.to_string(result_expr3))
