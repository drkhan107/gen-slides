from typing import List, Union

def parse_page_ranges(page_string: str, max_pages: int) -> List[int]:
    """
    Parse a string of page ranges and return a list of valid page numbers.

    Args:
        page_string (str): A string containing page ranges (e.g., "1-3,5,7-9").
        max_pages (int): The maximum number of pages allowed.

    Returns:
        List[int]: A sorted list of unique, valid page numbers.

    Raises:
        TypeError: If page_string is not a string or max_pages is not an integer.
        ValueError: If max_pages is not positive or if the input string is invalid.
    """

    def validate_and_parse_range(range_str: str) -> List[int]:
        """
        Validate and parse a single range string.

        Args:
            range_str (str): A string representing a single range (e.g., "1-3" or "5").

        Returns:
            List[int]: A list of page numbers in the range.

        Raises:
            ValueError: If the range string is invalid.
        """
        try:
            if '-' in range_str:
                start, end = map(int, range_str.split('-'))
                if start > end:
                    raise ValueError(f"Invalid range: {range_str}")
                return list(range(max(1, start), min(end, max_pages) + 1))
            else:
                page = int(range_str)
                if page < 1 or page > max_pages:
                    raise ValueError(f"Page number out of range: {page}")
                return [page]
        except ValueError as e:
            raise ValueError(f"Invalid input: {range_str}") from e

    try:
        # Input validation
        if not isinstance(page_string, str):
            raise TypeError("page_string must be a string")
        
        if not isinstance(max_pages, int):
            raise TypeError("max_pages must be an integer")
        
        if max_pages <= 0:
            raise ValueError("max_pages must be a positive integer")

        # Remove whitespace and split into individual ranges
        page_ranges = page_string.replace(' ', '').split(',')
        result = []

        for page_range in page_ranges:
            pages = validate_and_parse_range(page_range)
            for page in pages:
                if page not in result:
                    result.append(page)

        # If no valid pages were found, return the default range
        return sorted(result) if result else list(range(1, max_pages + 1))

    except (TypeError, ValueError) as e:
        # Log the error (you might want to use a proper logging system here)
        print(f"Error parsing page ranges: {str(e)}")
        # Return default list in case of any exception
        return list(range(1, max_pages + 1))