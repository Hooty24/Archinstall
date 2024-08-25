def replace_line_in_file(file_path: str, old_line: str, new_line: str) -> None:
    """
    Replaces the first line in a file that matches the old_line string with the new_line string

    Args:
        file_path: The path to the file where the line should be replaced
        old_line: The string to be replaced
        new_line: The new string to replace with

    Returns:
        None

    Raises:
        FileNotFoundError: If the file with the specified path is not found
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip() == old_line.strip():
            lines[i] = new_line + '\n'
            break
    with open(file_path, 'w') as f:
        f.writelines(lines)
