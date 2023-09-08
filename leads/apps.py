from django.apps import AppConfig


class LeadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leads'


    def ready(self):
        print("ready called")
        from leads import singals  # Replace 'leads' with your app's name if it's different
