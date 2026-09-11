def calculate_expression(expression: str) -> str:
    try:
        # Evaluate the expression safely
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")