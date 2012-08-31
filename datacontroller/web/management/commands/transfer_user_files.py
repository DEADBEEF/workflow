from django.core.management.base import BaseCommand, CommandError
from web.models import Task, STATUS_LOOKUP, Job, TASK_LOOKUP
from web.run_task import transfer_files
from django.contrib.auth.models import User

class Command(BaseCommand):
    args=""
    help    ="later"
    def handle(self, *args, **options):
        jobs = Job.object.filter(type=TYPE_LOOKUP["USER"])
        for job in jobs:
            tasks = Task.objects.filter(job_type=job, job_status=STATUS_LOOKUP["NOTDONE"])
            for t in tasks:
                can_execute = True
                for pred in t.predecessors.all():
                    if pred.job_status != STATUS_LOOKUP["DONE"]:
                        can_execute = False
                        break
                if can_execute:
                    print "Executing task"
                    transfer_files(t)



