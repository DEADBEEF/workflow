from web.models import TYPE_LOOKUP, STATUS_LOOKUP, Host, SiteDir, File
from web.directoryIndex import Directory
from threading import Thread
from subprocess import call
from cStringIO import StringIO
from datetime import datetime
import random
import string
import os

def finish_task(task):
    task.job_status = STATUS_LOOKUP["DONE"]
    task.save()
    #Update File list
    root = SiteDir.objects.get().root_dir
    site = task.site.folder_name
    directory = task.output_folder
    out_dir = "%s%s/%s"  % (root, site, directory)
    remove = "%s%s/"  % (root, site)
    remove_dir = os.path.abspath(remove)
    filelist = Directory(out_dir).getFileList()
    site = task.site
    add_files = []
    for filename in filelist:
        name = filename[0][len(remove_dir)+1:]
        file_o, created = File.objects.get_or_create(site=site, filename=name)
        if created:
            add_files.append(file_o)
        print name



    tasks = task.successors.all()
    for t in tasks:
        for f in add_files:
            t.input_files.add(f)
        if t.job_status != STATUS_LOOKUP["NOTDONE"]:
            continue
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
        task.started = datetime.now()
        task.job_status = STATUS_LOOKUP["INPROGRESS"]
        task.save()
        script = str(task.job_type.script)
        files = task.input_files.all()
        ofolder = "%s/%s/%s/" % (self.root, task.site.folder_name, task.output_folder)
        try:
            os.mkdir(ofolder)
        except OSError as exc: # Python >2.5
            pass
        read, write = os.pipe()
        os.write(write, datetime.now().strftime("[%Y-%m-%d %H:%M:%s Starting Task]\n"))
        passed = True
        for f in files:
            fname = "%s/%s/%s" % (self.root, task.site.folder_name, f.filename)
            callscript = [script, fname, ofolder]
            os.write(write, ("[ Caling file - %s: %s ]\n" % (f.filename, " ".join(callscript))) )
            try:
                a = call(callscript, stdout=write, stderr=write)
            except:
                os.write(write, ("[ FAILED No Script: The script was not found ]\n\n") )
                task.job_status = STATUS_LOOKUP["FAILED"]
                os.close(write)
                fi = os.fdopen(read, "r")
                log =  fi.read()
                task.log += log
                task.save()
                return
            if a != 0:
                os.write(write, ("[ FAILED ERROR: %d ]\n\n" % a) )
                passed = False
            else:
                os.write(write, ("[ SUCCESS ]\n\n") )
        os.close(write)
        fi = os.fdopen(read, "r")
        log =  fi.read()
        task.log += log
        task.save()
        if passed:
            task.ended = datetime.now()
            finish_task(task)
        else:
            task.job_status = STATUS_LOOKUP["FAILED"]
            task.save()



class AsyncTask1M(Thread):
    def __init__(self, task):
        Thread.__init__(self)
        self.task = task
        self.root = str(SiteDir.objects.get().root_dir)
    def run(self):
        task = self.task
        task.started = datetime.now()
        task.job_status = STATUS_LOOKUP["INPROGRESS"]
        task.save()
        script = str(task.job_type.script)
        files = task.input_files.all()
        ofolder = "%s/%s/%s/" % (self.root, task.site.folder_name, task.output_folder)
        try:
            os.mkdir(ofolder)
        except OSError as exc: # Python >2.5
            pass
        callscript = [script, ofolder] + map(lambda x:
            "%s/%s/%s" % (self.root, task.site.folder_name, x.filename), files)
        read, write = os.pipe()
        os.write(write, datetime.now().strftime("[%Y-%m-%d %H:%M:%s Starting Task]\n"))
        os.write(write, ("[ %s ]\n" %  " ".join(callscript)))
        try:
            result = call(callscript, stdout=write, stderr=write)
        except:
            os.write(write, ("[ FAILED No Script: The script was not found ]\n\n") )
            task.job_status = STATUS_LOOKUP["FAILED"]
            os.close(write)
            fi = os.fdopen(read, "r")
            log =  fi.read()
            task.log += log
            task.save()
            return
        if result != 0:
            os.write(write, ("[ FAILED ERROR: %d ]\n\n" % result) )
        else:
            os.write(write, ("[ SUCCESS ]\n\n") )
        os.close(write)
        fi = os.fdopen(read, "r")
        log =  fi.read()
        task.log += log
        task.save()
        if result != 0:
            task.job_status = STATUS_LOOKUP["FAILED"]
            task.save()
        else:
            task.ended = datetime.now()
            finish_task(task)

class AsyncTaskUserStart(Thread):
    def __init__(self, task, host=None):
        Thread.__init__(self)
        self.task = task
        self.host = None
        self.root = str(SiteDir.objects.get().root_dir)

    def run(self):
        task = self.task
        task.job_status = STATUS_LOOKUP["TRANSFERING"]
        task.started = datetime.now()
        task.save()
        user = task.assignee
        site = task.site

        read, write = os.pipe()
        os.write(write, "[ Starting User Task ]\n")
        if self.host is None:
            self.host = Host.objects.get(user=user,primary=True)
        os.write(write, "[ Host: %s ]\n" % self.host)
        tmp_list = ''.join(random.choice(string.ascii_uppercase) for i in xrange(10))
        os.write(write, "[ Tempfile: %s,  Filelist ]\n" % tmp_list)
        fo = file("/tmp/%s" % tmp_list, "w")
        site_dir = "%s/%s/" % (self.root, site.folder_name)
        out_dir = "%s/%s/" % (site_dir, task.output_folder)
        fo.write("%s/%s/\n" % (site.folder_name, task.output_folder))
        os.write(write, "%s/%s/\n" % (site.folder_name, task.output_folder))
        try:
            os.mkdir(out_dir)
        except OSError as exc: # Python >2.5
            pass
        dest_site_dir = "%s/%s/" % (self.host.root_dir, site.folder_name)
        hostname = str(self.host.hostname)

        # File sync
        files = task.input_files.all()
        for fi in files:
            os.write(write, "%s\n" % fi.filename)
            fo.write("%s/%s\n" % (site.folder_name, fi.filename))
        fo.close()
        os.write(write, "[ Transfering ]\n")
        result = call(["rsync", "-avz", "--files-from=/tmp/%s" % (tmp_list) ,
            self.root, "%s:%s" % (hostname, self.host.root_dir) ], stdout=write, stderr=write)
        if result != 0:
            os.write(write, ("[ FAILED ERROR: %d ]\n\n" % result) )
            task.job_status = STATUS_LOOKUP["FAILED"]
        else:
            os.write(write, ("[ SUCCESSFUL ]\n\n") )
        os.close(write)
        fi = os.fdopen(read, "r")
        log =  fi.read()
        task.log += log
        os.remove("/tmp/%s" % tmp_list)
        if result != 0:
            task.job_status = STATUS_LOOKUP["FAILED"]
            task.save()
        else:
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
        read, write = os.pipe()
        os.write(write, "[ Transfering back ]\n")
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

        result = call(["rsync", "-ravz", "%s:%s" % (hostname, dest_out_dir), out_dir], stdout=write,
                stderr=write)
        if result != 0:
            os.write(write, ("[ FAILED ERROR: %d ]\n\n" % result) )
            task.job_status = STATUS_LOOKUP["FAILED"]
        else:
            os.write(write, ("[ SUCCESSFUL ]\n\n") )
        os.close(write)
        fi = os.fdopen(read, "r")
        log =  fi.read()
        task.log += log
        if result != 0:
            task.job_status = STATUS_LOOKUP["FAILED"]
            task.save()
        else:
            task.ended = datetime.now()
            task.job_status = STATUS_LOOKUP['VALIDATE']
            task.save()

class AsyncTaskTransferFiles(Thread):
    def __init__(self, task, host=None, file_type=None):
        Thread.__init__(self)
        self.task = task
        self.host = None
        self.ftype = file_type
        self.root = str(SiteDir.objects.get().root_dir)

    def run(self):
        task = self.task
        if task.job_status == STATUS_LOOKUP["TRANSFERING"] or \
           task.job_status == STATUS_LOOKUP["TRANSFER_BACK"]:
            return
        old_status = task.job_status
        task.job_status = STATUS_LOOKUP["TRANSFERING"]
        task.save()
        user = task.assignee
        site = task.site

        read, write = os.pipe()
        os.write(write, "[ Starting File Transfer ]\n")
        if self.host is None:
            self.host = Host.objects.get(user=user,primary=True)
        os.write(write, "[ Host: %s ]\n" % self.host)
        site_dir = "%s/%s/" % (self.root, site.folder_name)
        out_dir = "%s/%s/" % (site_dir, task.output_folder)
        try:
            os.mkdir(out_dir)
        except OSError as exc: # Python >2.5
            pass
        dest_site_dir = "%s/%s/" % (self.host.root_dir, site.folder_name)
        hostname = str(self.host.hostname)

        # File sync
        if self.ftype == "in":
            input_f = True
            output_f = False
        elif self.ftype == "out":
            input_f = False
            output_f = True
        elif self.ftype == "all":
            input_f = True
            output_f = True

        if input_f:
            tmp_list = ''.join(random.choice(string.ascii_uppercase) for i in xrange(10))
            os.write(write, "[ Tempfile: %s,  Filelist ]\n" % tmp_list)
            fo = file("/tmp/%s" % tmp_list, "w")
            files = task.input_files.all()
            for fi in files:
                os.write(write, "%s/%s\n" % (site.folder_name, fi.filename))
                fo.write("%s/%s\n" % (site.folder_name, fi.filename))
            fo.close()
            os.write(write, "[ Transfering ]\n")
            result = call(["rsync", "-avz", "--files-from=/tmp/%s" % (tmp_list) ,
                self.root, "%s:%s" % (hostname, self.host.root_dir) ], stdout=write, stderr=write)
            os.remove("/tmp/%s" % tmp_list)

        if output_f:
            dest_out_dir = "%s/%s/%s/" % (self.host.root_dir, site.folder_name, task.output_folder)
            os.write(write, "%s/%s/*\n" % (site.folder_name, task.output_folder))
            result = call(["rsync", "-ravz", out_dir,  "%s:%s" % (hostname, dest_out_dir)],
                    stdout=write, stderr=write)

        os.close(write)
        fi = os.fdopen(read, "r")
        log =  fi.read()
        task.log += log
        task.job_status = old_status
        task.save()

class AsyncTaskTransferBackFiles(Thread):
    def __init__(self, task, host=None):
        Thread.__init__(self)
        self.task = task
        self.host = None
        self.root = str(SiteDir.objects.get().root_dir)

    def run(self):
        task = self.task
        user = task.assignee
        site = task.site
        old_status = task.job_status
        task.job_status = STATUS_LOOKUP["TRANSFER_BACK"]
        task.save()
        read, write = os.pipe()
        os.write(write, "[ Transfering back ]\n")
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

        result = call(["rsync", "-ravz", "%s:%s" % (hostname, dest_out_dir), out_dir], stdout=write,
                stderr=write)

        os.close(write)
        fi = os.fdopen(read, "r")
        log =  fi.read()
        task.log += log
        task.job_status = old_status
        task.save()


def transfer_back(task):
    if task.job_status == STATUS_LOOKUP["INPROGRESS"]:
        task.job_status = STATUS_LOOKUP["TRANSFER_BACK"]
        task.save()
        AsyncTaskTransferBack(task).start()

def transfer_files(task, ftype, host=None):
    AsyncTaskTransferFiles(task, host, ftype).start()


def transfer_back_files(task, host=None):
    AsyncTaskTransferBackFiles(task, host).start()

def run_task(task):
    if task.assignee == None:
        return
    if task.job_type.type == TYPE_LOOKUP['SERVER-1-1']:
        AsyncTask11(task).start()
    elif task.job_type.type == TYPE_LOOKUP['SERVER-M-1']:
        AsyncTask1M(task).start()
    elif task.job_type.type == TYPE_LOOKUP['USER']:
        if task.job_status == STATUS_LOOKUP["NOTDONE"]:
            AsyncTaskUserStart(task).start()
        elif task.job_status == STATUS_LOOKUP["VALIDATE"]:
            AsyncTaskTransferBack(task).start()

