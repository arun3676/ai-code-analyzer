def calculate_average(numbers: list) -> float:
    """
    Calculates the average of a list of numbers.
    There is a bug in this function.
    """
    if not numbers:
        return 0.0
    
    total = 0
    # Bug: This loop will miss the last number in the list.
    for i in range(len(numbers) - 1):
        total += numbers[i]
        
    return total / len(numbers)

# Example usage (will produce the wrong result)
# print(calculate_average([10, 20, 30])) 
# Expected: 20.0
# Actual: 10.0
