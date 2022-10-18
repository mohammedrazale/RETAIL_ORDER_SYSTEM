""" Helper functions common to all services. """


def send_success_response(result: dict):
    """Send a 200 success response"""
    return {"success": True, "result": result}, 200


def send_bad_request_response(error_message):
    """Send bad request response"""
    return {"success": True, "message": error_message}, 400


def send_server_error_response(error_message):
    """Send sever error response"""
    return {"success": True, "message": error_message}, 500
