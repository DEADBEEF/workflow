from web.models import TYPE_LOOKUP, STATUS_LOOKUP, Host, SiteDir
from threading import Thread
from subprocess import call
import random
import string
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
        self.root = str(SiteDir.objects.get().root_dir)
    def run(self):
        task = self.task
        script = str(task.job_type.script)
        files = task.input_files.all()
        ofolder = "%s/%s/%s/" % (self.root, task.site.folder_name, task.output_folder)
        try:
            os.mkdir(ofolder)
        except OSError as exc: # Python >2.5
            pass
        for f in files:
            fname = "%s/%s/%s" % (self.root, task.site.folder_name, f.filename)
            call([script, fname, ofolder])
        finish_task(task)

class AsyncTask1M(Thread):
    def __init__(self, task):
        Thread.__init__(self)
        self.task = task
        self.root = str(SiteDir.objects.get().root_dir)
    def run(self):
        task = self.task
        script = str(task.job_type.script)
        files = task.input_files.all()
        ofolder = "%s/%s/%s/" % (self.root, task.site.folder_name, task.output_folder)
        try:
            os.mkdir(ofolder)
        except OSError as exc: # Python >2.5
            pass
        call([script, ofolder] + map(lambda x:
            "%s/%s/%s" % (self.root, task.site.folder_name, x.filename), files))
        finish_task(task)

class AsyncTaskUserStart(Thread):
    def __init__(self, task, host=None):
        Thread.__init__(self)
        self.task = task
        self.host = None
        self.root = str(SiteDir.objects.get().root_dir)

    def run(self):
        task = self.task
        user = task.assignee
        site = task.site
        if self.host is None:
            self.host = Host.objects.get(user=user,primary=True)
        tmp_list = ''.join(random.choice(string.ascii_uppercase) for i in xrange(10))
        fo = file("/tmp/%s" % tmp_list, "w")
        site_dir = "%s/%s/" % (self.root, site.folder_name)
        out_dir = "%s/%s/" % (site_dir, task.output_folder)
        fo.write("%s/%s/\n" % (site.folder_name, task.output_folder))
        try:
            os.mkdir(out_dir)
        except OSError as exc: # Python >2.5
            pass
        dest_site_dir = "%s/%s/" % (self.host.root_dir, site.folder_name)
        hostname = str(self.host.hostname)

        # File sync
        files = task.input_files.all()
        for fi in files:
            fo.write("%s/%s\n" % (site.folder_name, fi.filename))
        fo.close()
        call(["rsync", "-avz", "--files-from=/tmp/%s" % (tmp_list) ,
            self.root, "%s:%s" % (hostname, self.host.root_dir) ])
        os.remove("/tmp/%s" % tmp_list)
        task.job_status = STATUS_LOOKUP['INPROGRESS']
        task.save()

class AsyncTaskTransferBack(Thread):
    def __init__(self, task, host=None):
        Thread.__init__(self)
        self.task = task
        self.host = None
        self.root = str(SiteDir.objects.get().root_dir)

    def run(self):
        task = self.task
        user = task.assignee
        site = task.site
        if self.host is None:
            self.host = Host.objects.get(user=user,primary=True)
        site_dir = "%s/%s/" % (self.root, site.folder_name)
        out_dir = "%s/%s/" % (site_dir, task.output_folder)
        try:
            os.mkdir(out_dir)
        except OSError as exc: # Python >2.5
            pass
        dest_out_dir = "%s/%s/%s/" % (self.host.root_dir, site.folder_name, task.output_folder)
        hostname = str(self.host.hostname)

        call(["rsync", "-ravz", "%s:%s" % (hostname, dest_out_dir), out_dir])
        finish_task(task)



def run_task(task):
    if task.job_type.type == TYPE_LOOKUP['SERVER-1-1']:
        AsyncTask11(task).start()
    elif task.job_type.type == TYPE_LOOKUP['SERVER-M-1']:
        AsyncTask1M(task).start()
    elif task.job_type.type == TYPE_LOOKUP['USER']:
        if task.job_status == STATUS_LOOKUP["NOTDONE"]:
            AsyncTaskUserStart(task).start()
        elif task.job_status == STATUS_LOOKUP["TRANSFER_BACK"]:
            AsyncTaskTransferBack(task).start()

