from importlib import import_module

from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class LIMITARUSER(MiddlewareMixin):
    def process_request(self, request):
        """Limita una sesión activa por usuario."""
        if request.user.is_authenticated:
            cache_timeout = 86400
            cache_key = "user_pk_%s_restrict" % request.user.pk
            cache_value = cache.get(cache_key)
            if cache_value is not None and request.session.session_key != cache_value:
                engine = import_module(settings.SESSION_ENGINE)
                session = engine.SessionStore(session_key=cache_value)
                session.delete()
            cache.set(cache_key, request.session.session_key, cache_timeout)
        return None
