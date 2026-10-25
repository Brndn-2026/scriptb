import json
import os

def handle_json(file_path, data=None):
    """
    Reads or writes JSON data to a file.
    
    Parameters:
        file_path (str): Path to the JSON file.
        data (dict | list | None): 
            - If None: Reads and returns JSON content from the file.
            - If dict or list: Writes it as JSON to the file.
    
    Returns:
        dict | list | None: 
            - Returns parsed JSON data when reading.
            - Returns None when writing.
    
    Raises:
        ValueError: If data is not serializable to JSON.
        FileNotFoundError: If reading and file does not exist.
        json.JSONDecodeError: If file content is not valid JSON.
    """
    if data is None:
        # READ JSON
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # WRITE JSON
        if not isinstance(data, (dict, list)):
            raise ValueError("Data must be a dictionary or list to be saved as JSON.")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return None