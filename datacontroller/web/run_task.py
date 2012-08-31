from web.models import TYPE_LOOKUP, STATUS_LOOKUP
from threading import Thread
from subprocess import call
import os


def finish_task(task):
    task.job_status = STATUS_LOOKUP["DONE"]
    task.save()
    tasks = task.successors.all()
    for t in tasks:
        can_execute = True
        for pred in t.predecessors.all():
            if pred.job_status != STATUS_LOOKUP["DONE"]:
                can_execute = False
                break
        if can_execute:
            print "Executing task"
            run_task(t)


class AsyncTask11(Thread):
    def __init__(self, task):
        Thread.__init__(self)
        self.task = task
    def run(self):
        task = self.task
        script = str(task.job_type.script)
        files = task.input_files.all()
        ofolder = str(task.site.root) + str(task.output_folder)
        try:
            os.mkdir(ofolder)
        except OSError as exc: # Python >2.5
            pass
        for f in files:
            fname = str(task.site.root)+ str(f.filename)
            call([script, fname, ofolder])
        finish_task(task)

class AsyncTask1M(Thread):
    def __init__(self, task):
        Thread.__init__(self)
        self.task = task
    def run(self):
        task = self.task
        script = str(task.job_type.script)
        files = task.input_files.all()
        ofolder = str(task.site.root) + str(task.output_folder)
        print ofolder
        try:
            os.mkdir(ofolder)
        except OSError as exc: # Python >2.5
            pass
        call([script, ofolder] + map(lambda x: str(task.site.root) +  str(x.filename), files))
        finish_task(task)

def run_task(task):
    if task.job_type.type == TYPE_LOOKUP['SERVER-1-1']:
        AsyncTask11(task).start()
    elif task.job_type.type == TYPE_LOOKUP['SERVER-M-1']:
        AsyncTask1M(task).start()
    pass

