import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete expired directories in media/temp'

    def handle(self, *args, **kwargs):
        media_temp_path = os.path.join('media', 'temp')
        current_time = datetime.now()

        for dir_name in os.listdir(media_temp_path):
            dir_path = os.path.join(media_temp_path, dir_name)

            # Check if it is a directory
            if os.path.isdir(dir_path):
                try:
                    # Extract the expiration date from the directory name
                    expiration_date_str = dir_name.split('___')[0]
                    expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d-%H-%M-%S")

                    # Check if the directory has expired
                    if expiration_date < current_time:
                        shutil.rmtree(dir_path)
                        self.stdout.write(self.style.SUCCESS(f'Deleted expired directory: {dir_name}'))

                except ValueError:
                    self.stderr.write(self.style.ERROR(f'Invalid date format in directory name: {dir_name}'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error deleting directory {dir_name}: {str(e)}'))
