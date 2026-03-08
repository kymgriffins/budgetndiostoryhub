from django.apps import AppConfig


class NextjsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.nextjs'
    verbose_name = 'Next.js Integration'
    
    def ready(self):
        """Import signals when app is ready."""
        pass
