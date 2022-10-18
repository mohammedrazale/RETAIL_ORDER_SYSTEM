""" Custom Exceptions for Inventory Service. """


class NoSuchProductException(Exception):
    """No Product with the passed id is available."""
