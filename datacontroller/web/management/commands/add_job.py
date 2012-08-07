from django.core.management.base import BaseCommand, CommandError
from web.models import Job
from django.contrib.auth.models import User

class Command(BaseCommand):
    args="job_file"
    help="later"

    def handle(self, *args, **options):
        user = User.objects.get(username="michiel")
        j = Job(name="CLEANLOL", assignee=user,job_type="1",job_status="1",description="LOL")
        j.save()
        self.stdout.write("LOL\n")

