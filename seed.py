import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduling.settings")
django.setup()


from deploy.data_seeder import seed_data

seed_data()
