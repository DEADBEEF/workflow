from django.core.management.base import BaseCommand, CommandError
from web.models import Job, Site
from django.contrib.auth.models import User

class Command(BaseCommand):
    args="assignee site type"
    help    ="later"

    def handle(self, *args, **options):
        username = args[0]
        sitname = args[1]
        job_type = args[2]
        user = User.objects.get(username=username)
        site = S
        j = Job(name="CLEANLOL", assignee=user,job_type="1",job_status="1",description="LOL")
        j.save()
        self.stdout.write("LOL\n")

