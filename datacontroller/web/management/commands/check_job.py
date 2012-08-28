from django.core.management.base import BaseCommand, CommandError
from web.models import Job
from django.contrib.auth.models import User

class Command(BaseCommand):
    args="user assignee type"
    help="later"

    def handle(self, *args, **options):
        username = args[0]
        sitename = args[1]
        job_type = args[2]
        ident = ":".join((username, sitename, job_type))
        try:
            j = Job.objects.get(name=ident)
        except:
            self.stdout.write("BUSY")
            return
        status = j.get_job_status_display()
        if status == "DONE":
            self.stdout.write("DONE")
        else:
            self.stdout.write("BUSY")

