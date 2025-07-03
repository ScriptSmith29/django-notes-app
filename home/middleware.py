class ThemeCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        theme = request.COOKIES.get('theme')
        if theme:
            request.theme = theme
        else:
            request.theme = 'light'
        response = self.get_response(request)
        return response
