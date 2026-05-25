class NotFoundError(Exception):
    """Entity not found"""
    pass

class ConflictError(Exception):
    """Resource conflict (e.g., booking overlap)"""
    pass

class ValidationError(Exception):
    """Business logic validation failed"""
    pass