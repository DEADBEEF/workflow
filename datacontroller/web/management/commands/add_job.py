from django.core.management.base import BaseCommand, CommandError
from web.models import Job, Site, TYPE_LOOKUP
from django.contrib.auth.models import User

class Command(BaseCommand):
    args="assignee site type"
    help    ="later"

    def handle(self, *args, **options):
        username = args[0]
        sitename = args[1]
        job_type = args[2]
        user = User.objects.get(username=username)
        site = Site.objects.get(name=sitename)
        ident = ":".join((username, sitename, job_type))
        j = Job(name=ident, assignee=user, site=site ,job_type=TYPE_LOOKUP[job_type],
                job_status="1",description="LOL")
        j.save()
        self.stdout.write("LOL\n")

