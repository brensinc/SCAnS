def find_comma(input_str):
    """
    Find locations of commas that separate parameters in the input string.
    
    Returns:
        comma_index: list of positions of valid commas
        comma_num: number of such commas
    """
    n = len(input_str)
    comma_index = []
    comma_num = 0

    # Get the positions of all left and right parentheses
    left_par = [i for i, c in enumerate(input_str) if c == '(']
    right_par = [i for i, c in enumerate(input_str) if c == ')']

    for i, char in enumerate(input_str):
        if char == ',':
            # Count how many left/right parentheses are up to this index
            num_left = sum(pos <= i for pos in left_par)
            num_right = sum(pos <= i for pos in right_par)
            if num_left == num_right:
                comma_index.append(i)
                comma_num += 1

    return comma_index, comma_num
