# File: ai_features/employee_performance.py

def calculate_performance(data: dict) -> tuple[float, dict]:
    """
    Calculate performance metrics for a given employee and period.

    Args:
        data (dict): Must include:
            - 'employee_id' (int)
            - 'period' (str)
    Returns:
        tuple:
            - performance_score (float)
            - metrics (dict[str, float])
    """
    # TODO: implement your performance calculation here
    raise NotImplementedError("Implement employee performance logic")

# Alias for backward compatibility in signals
calculate_employee_performance = calculate_performance
