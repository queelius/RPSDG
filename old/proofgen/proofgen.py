from dataclasses import dataclass
from typing import List, Union, Tuple
import random

@dataclass
class Variable:
    name: str

@dataclass
class Function:
    name: str
    args: List['Term']

Term = Union[Variable, Function]

def vars(term: Term) -> List[Variable]:
    if isinstance(term, Variable):
        return [term]
    return [var for arg in term.args for var in vars(arg)]

def substitute(term: Term, substitution: dict) -> Term:
    if isinstance(term, Variable):
        return substitution.get(term, term)
    return Function(term.name, [substitute(arg, substitution) for arg in term.args])

@dataclass
class Rule:
    lhs: Term
    rhs: Term

    def apply(self, term: Term) -> Union[Term, None]:
        substitution = {}
        if self.match(self.lhs, term, substitution):
            return substitute(self.rhs, substitution)
        return None

    def match(self, pattern: Term, term: Term, substitution: dict) -> bool:
        if isinstance(pattern, Variable):
            if pattern in substitution:
                return substitution[pattern] == term
            substitution[pattern] = term
            return True
        if isinstance(term, Function) and isinstance(pattern, Function):
            if pattern.name != term.name or len(pattern.args) != len(term.args):
                return False
            return all(self.match(p, t, substitution) for p, t in zip(pattern.args, term.args))
        return False

def parse(s: str) -> Term:
    if '(' not in s:
        return Variable(s)
    name, args_str = s.split('(', 1)
    args_str = args_str[:-1]  # Remove trailing ')'
    args = [parse(arg.strip()) for arg in args_str.split(',')]
    return Function(name.strip(), args)

def to_string(term: Term) -> str:
    if isinstance(term, Variable):
        return term.name
    return f"{term.name}({', '.join(to_string(arg) for arg in term.args)})"

rules = [
    Rule(parse("+(x, y)"), parse("+(y, x)")),
    Rule(parse("*(x, y)"), parse("*(y, x)")),
    Rule(parse("*(x, +(y, z))"), parse("+(*(x, y), *(x, z))")),
]

def rewrite(term: Term, steps: int) -> List[Tuple[str, Term]]:
    result = [("Initial", term)]
    current = term
    for _ in range(steps):
        applicable_rules = [(rule, rule.apply(current)) for rule in rules]
        applicable_rules = [(r, t) for r, t in applicable_rules if t is not None]
        if not applicable_rules:
            break
        rule, new_term = random.choice(applicable_rules)
        result.append((rule.__class__.__name__, new_term))
        current = new_term
    return result

# Test expressions
test_expressions = [
    "*(a, +(b, c))",
    "+(*(2, 3), 1)",
    "+(*(a, b), *(a, c))",
    "+(x, +(y, z))",
    "+(*(a, a), 1)"
]

# Run tests
for expr_str in test_expressions:
    print(f"\nStarting expression: {expr_str}")
    expr = parse(expr_str)
    proof = rewrite(expr, 5)  # Generate 5 steps
    
    print("Proof:")
    for step_name, term in proof:
        print(f"{step_name}:")
        print(f"  Expression: {to_string(term)}")
    print()  # Add a blank line for readability