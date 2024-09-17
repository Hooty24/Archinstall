def replace_line_in_file(file_path: str, old_line: str, new_line: str) -> None:
    """
    Replaces the first line in a file that matches the old_line string with the new_line string
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip() == old_line.strip():
            lines[i] = new_line + '\n'
            break
    with open(file_path, 'w') as f:
        f.writelines(lines)
