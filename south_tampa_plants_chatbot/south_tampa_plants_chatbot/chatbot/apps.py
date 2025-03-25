import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Chatbot(AppConfig):
    name = "south_tampa_plants_chatbot.chatbot"
    verbose_name = _("South Tampa Plants Chatbot")

    def ready(self):
        return
        # with contextlib.suppress(ImportError):
        #     import south_tampa_plants_chatbot.users.signals  # noqa: F401
