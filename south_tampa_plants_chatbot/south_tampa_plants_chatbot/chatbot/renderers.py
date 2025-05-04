from rest_framework.renderers import BaseRenderer

class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset) if isinstance(data, str) else str(data).encode(self.charset)