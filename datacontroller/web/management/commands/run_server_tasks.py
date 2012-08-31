from django.core.management.base import BaseCommand, CommandError
from web.models import Task, STATUS_LOOKUP
from web.run_task import run_task
from django.contrib.auth.models import User

class Command(BaseCommand):
    args=""
    help    ="later"
    def handle(self, *args, **options):
        server_user = User.objects.get(username='server')
        tasks = Task.objects.filter(job_status=STATUS_LOOKUP["NOTDONE"])
        for t in tasks:
            can_execute = True
            for pred in t.predecessors.all():
                if pred.job_status != STATUS_LOOKUP["DONE"]:
                    can_execute = False
                    break
            if can_execute:
                print "Executing task"
                run_task(t)

        tasks = Task.objects.filter(job_status=STATUS_LOOKUP["TRANSFER_BACK"])
        for t in tasks:
            print "Executing task"
            run_task(t)



