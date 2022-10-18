""" Custom Exceptions for Order Service. """


class NoSuchOrderException(Exception):
    """No Order with the passed id is available."""
