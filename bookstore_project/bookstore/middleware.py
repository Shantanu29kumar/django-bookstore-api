import time

class APILogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        print("Incoming Request:", request.method, request.path)

        response = self.get_response(request)

        duration = time.time() - start_time

        print("Response Status:", response.status_code)
        print("Time Taken:", duration)

        return response