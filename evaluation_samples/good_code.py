def get_file_extension(filename: str) -> str:
    """
    Returns the extension of a file.

    Args:
        filename: The name of the file.

    Returns:
        The file extension (e.g., "txt", "py") or an empty string if
        the file has no extension.
    """
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string.")
    
    parts = filename.split('.')
    if len(parts) > 1:
        return parts[-1]
    return ""
