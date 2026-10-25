import requests


BASE_URL = "https://api-wlzt.onrender.com"
_session = requests.Session()


def fetch(path, method="GET", body=None, **kwargs):
    """Send a request to ScriptB IoT and return its decoded response."""
    url = path if path.startswith(("http://", "https://")) else f"{BASE_URL}{path}"
    response = _session.request(method, url, json=body, timeout=30, **kwargs)
    response.raise_for_status()

    if not response.content:
        return None

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return response.json()
    return response.text


def init(email, password):
    """
    Initializes the IoT system with the provided email and password.
    
    Args:
        email (str): The user's email address.
        password (str): The user's password.
    
    Raises:
        Exception: If there is an error during initialization.
    """
    if not isinstance(email, str) or not email.strip():
        raise ValueError("email must be a non-empty string")
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")

    global email2, password2
    email2 = email
    password2 = password

    try:
        print(f"Initializing IoT with email: {email}")
        return fetch(
            "/api/login",
            method="POST",
            body={"email": email, "password": password},
        )
    except requests.RequestException as error:
        raise RuntimeError(f"Failed to log in to ScriptB IoT: {error}") from error


def senddata(data, email=None, password=None):
    """
    Sends data to the ScriptB IoT system.
    
    Args:
        data (dict): The data to be sent.
    
    Raises:
        Exception: If there is an error during data transmission.
    """
    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

    return savedata(data, email=email, password=password)


def savedata(data, email=None, password=None):
    """Save data for a specific ScriptB IoT user."""
    email = email if email is not None else globals().get("email2")
    password = password if password is not None else globals().get("password2")

    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")
    if not isinstance(email, str) or not email.strip():
        raise ValueError("email must be a non-empty string")
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")

    try:
        response = fetch(
            "/api/savedata",
            method="POST",
            body={"email": email, "password": password, "data": data},
        )
        return response.get("data") if isinstance(response, dict) else response
    except requests.RequestException as error:
        raise RuntimeError(f"Failed to save data to ScriptB IoT: {error}") from error


def getdata(email=None, password=None):
    """Retrieve data for a specific ScriptB IoT user."""
    email = email if email is not None else globals().get("email2")
    password = password if password is not None else globals().get("password2")

    if not isinstance(email, str) or not email.strip():
        raise ValueError("email must be a non-empty string")
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")

    try:
        response = fetch(
            "/api/getdata",
            method="POST",
            body={"email": email, "password": password},
        )
        return response.get("data") if isinstance(response, dict) else response
    except requests.RequestException as error:
        raise RuntimeError(f"Failed to retrieve data from ScriptB IoT: {error}") from error