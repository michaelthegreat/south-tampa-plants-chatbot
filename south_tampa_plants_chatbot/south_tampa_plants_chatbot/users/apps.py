import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "south_tampa_plants_chatbot.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import south_tampa_plants_chatbot.users.signals  # noqa: F401
