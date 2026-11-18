from rest_framework.throttling import SimpleRateThrottle

class ContactRateThrottle(SimpleRateThrottle):
    scope = "contact"
    rate = "5/minute"
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}
    def parse_rate(self, rate):
        return 5, 15 * 60
