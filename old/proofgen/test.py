from dataclasses import dataclass
from typing import List, Union, Optional
import random

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
    def __init__(self, name: str, pattern: Expression, replacement: Expression):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement
    
    def apply(self, expr: Expression) -> Optional[Expression]:
        bindings = {}
        if self.match(expr, self.pattern, bindings):
            return self.instantiate(self.replacement, bindings)
        return None

    def match(self, expr: Expression, pattern: Expression, bindings: dict) -> bool:
        if isinstance(pattern, Variable):
            if pattern.name in bindings:
                return self.match(expr, bindings[pattern.name], {})
            bindings[pattern.name] = expr
            return True
        elif isinstance(pattern, Number) and isinstance(expr, Number):
            return pattern.value == expr.value
        elif isinstance(pattern, BinaryOp) and isinstance(expr, BinaryOp):
            return (pattern.op == expr.op and
                    self.match(expr.left, pattern.left, bindings) and
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
            return BinaryOp(template.op,
                            self.instantiate(template.left, bindings),
                            self.instantiate(template.right, bindings))
        elif isinstance(template, UnaryOp):
            return UnaryOp(template.op, self.instantiate(template.expr, bindings))

class ProofGenerator:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
    
    def random_walk(self, start_expression: Expression, steps: int) -> List[tuple[str, Expression]]:
        current = start_expression
        proof = [("Initial", current)]
        for _ in range(steps):
            applicable_rules = [rule for rule in self.rules if rule.apply(current) is not None]
            if not applicable_rules:
                break
            rule = random.choice(applicable_rules)
            new_expression = rule.apply(current)
            if new_expression is not None:
                proof.append((rule.name, new_expression))
                current = new_expression
        return proof

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
         Variable("A"))
]

# Test expressions using AST
test_expressions = [
    BinaryOp("*", BinaryOp("+", Number(2), Number(3)), Number(4)),
    BinaryOp("+", Number(1), BinaryOp("*", Number(2), Number(3))),
    BinaryOp("+", BinaryOp("*", Variable("a"), Variable("b")), BinaryOp("*", Variable("a"), Variable("c"))),
    BinaryOp("+", Variable("x"), BinaryOp("+", Variable("y"), Variable("z")))
]

# Run tests
printer = ExpressionPrinter()
generator = ProofGenerator(simple_rules)

for expr in test_expressions:
    print(f"\nStarting expression: {printer.to_string(expr)}")
    proof = generator.random_walk(expr, 5)  # Generate 5 steps
    
    print("Proof:")
    for step, expr in proof:
        print(f"{step}: {printer.to_string(expr)}")
