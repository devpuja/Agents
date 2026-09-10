def calculate_expression(expression: str) -> str:
    try:
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")