"""
Custom middleware for MIC Radiology Management System
"""

class NoCacheMiddleware:
    """
    Middleware to prevent caching of sensitive pages and authentication-related responses
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add no-cache headers to all responses to prevent authentication caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['Vary'] = 'Accept-Encoding, Authorization'
        
        return response
