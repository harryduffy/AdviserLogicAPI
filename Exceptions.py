class APIHealthFail(Exception):
    def __init__(self):
        super().__init__(f"The API is not healthy.")

class AuthenticationFail(Exception):
    def __init__(self):
        super().__init__(f"The user cannot be authenticated.")

class ResourceNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"The resource cannot be found.")