class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("path:", request.path)
        print("path_info:", request.path_info)
        print("method", request.method)
        return self.get_response(request)