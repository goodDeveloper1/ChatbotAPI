from django.core.cache import cache
from django.http import JsonResponse
from time import time

def rate_limit(seconds=5, max_requests=5):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            ip = get_client_ip(request)
            now = time()
            key = f"rl:{ip}"
            history = cache.get(key, [])

            # Clean up old requests
            history = [timestamp for timestamp in history if now - timestamp < seconds]

            if len(history) >= max_requests:
                return JsonResponse({'error': 'Too many requests'}, status=429)

            history.append(now)
            cache.set(key, history, timeout=seconds)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')
