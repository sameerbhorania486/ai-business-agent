import ast
import operator

from langchain_core.tools import tool


# =========================
# ALLOWED OPERATORS
# =========================

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


# =========================
# SAFE CALCULATOR
# =========================

def safe_calculate(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):

            return node.value

        raise ValueError("Invalid value.")

    if isinstance(node, ast.UnaryOp):

        operator_function = ALLOWED_OPERATORS.get(
            type(node.op)
        )

        if not operator_function:
            raise ValueError("Operator not allowed.")

        return operator_function(
            safe_calculate(node.operand)
        )

    if isinstance(node, ast.BinOp):

        operator_function = ALLOWED_OPERATORS.get(
            type(node.op)
        )

        if not operator_function:
            raise ValueError("Operator not allowed.")

        left = safe_calculate(node.left)
        right = safe_calculate(node.right)

        return operator_function(left, right)

    raise ValueError("Invalid mathematical expression.")


# =========================
# LANGCHAIN TOOL
# =========================

@tool
def calculate(expression: str) -> str:
    """
    Calculate a basic mathematical expression safely.
    Supports +, -, *, /, %, and **.
    """

    try:

        expression = expression.strip()

        if not expression:
            return "Invalid mathematical expression."

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = safe_calculate(
            tree.body
        )

        return str(result)

    except Exception:

        return "Invalid mathematical expression."