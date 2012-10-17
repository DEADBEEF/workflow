from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from web.models import Task, Site, STATUS_LOOKUP, Job, TYPE_LOOKUP, Host, Category, SiteDir, File
from web.run_task import transfer_back, transfer_files,  transfer_back_files
from web.run_task import run_task as run_process_task
from web.run_task import finish_task as finish_process_task
from web.directoryIndex import Directory
from datetime import datetime
from web.forms import TaskForm, AddUserTaskForm, AddServerTaskForm, JobForm, CategoryForm, SiteForm
import json
import os

class Structure:
    def __init__(self):
      self.dirs = {}
      self.files = []
      self.process = []
    def build(self):
      for fiO, fi in self.process:
        parts = fi.split("/")
        if len(parts) == 1:
          self.files.append( (fiO, parts[0]) )
        else:
          if self.dirs.get(parts[0],None) is None:
            self.dirs[parts[0]] = Structure()
          self.dirs[parts[0]].process.append( (fiO, "/".join(parts[1:])) )
      for struc in self.dirs.values():
        struc.build()
        
    def getListInterface(self,selected):
      result = "<ul>\n"
      for key, direc in self.dirs.items():
          result += "<li><i class=\"icon-book\"></i> %s\n%s</li>\n" % (key, direc.getListInterface(selected)) 
      for fiO, fi in self.files:
          #print dir(fiO)
          if fiO in selected:
            result += "<li item-checked=\"true\"><i class=\"icon-file\" id=\"%s\"></i> %s</li>" % (fiO.id,fi)
            print "<li name=\"%s\" item-checked=\"true\"><i class=\"icon-file\"></i> %s</li>" % (fiO.id,fi)
          else:
            result += "<li><i class=\"icon-file\" id=\"%s\"></i> %s</li>" % (fiO.id,fi)
      result += "</ul>\n"
      return result
        
class FileInterface: 
  def __init__(self, task=None, specific=False,site=None):
    self.task = task
    if site == None:
      self.site = task.site
      self.selected = task.input_files.all()
      self.files= File.objects.filter(site=self.site)
    else:
      self.site = site
      self.files= File.objects.filter(site=self.site)
      self.selected = self.files

    self.root = Structure()
    if specific:
      for fi in self.selected:
        self.root.process.append((fi, fi.filename))
    else:
      for fi in self.files:
        self.root.process.append((fi, fi.filename))
    self.root.build()
  def getInterface(self):
    return self.root.getListInterface(self.selected)
    
class TaskNode:
    def __init__(self, id, x, y, task, active=False):
        self.id = id
        self.x = x
        self.y = y
        self.task = task
        self.assigned = True
        files = self.task.input_files.all()
        self.files = "%d input file%s" % (len(files), ("s", "")[len(files) == 1] )
        if active:
            self.div_class = "active_node"
        elif task.job_status == STATUS_LOOKUP["FAILED"] or \
            task.assignee == None:
            if task.assignee == None:
              self.assigned = False
            self.div_class = "failed"
        elif task.job_status == STATUS_LOOKUP["NOTDONE"]:
            self.div_class = "notdone"
        elif task.job_status == STATUS_LOOKUP["TRANSFERING"] or \
            task.job_status == STATUS_LOOKUP["TRANSFER_BACK"]:
            self.div_class = "auto"
        elif task.job_status == STATUS_LOOKUP["INPROGRESS"] or \
            task.job_status == STATUS_LOOKUP["VALIDATE"]:
            self.div_class = "busy"
        elif task.job_status == STATUS_LOOKUP["DONE"]:
            self.div_class = "done"
            
def rescan(site):
  root = SiteDir.objects.get().root_dir
  ofolder = "%s/%s/" % (root, site.folder_name) 
  while ofolder.find("//") != -1:
     ofolder = ofolder.replace("//","/")
     print ofolder
  old_files =  set( fi.filename for fi in File.objects.filter(site=site) )
  try:
      os.mkdir(ofolder)
  except OSError as exc: # Python >2.5
      pass
  filelist = Directory(ofolder).getFileList()
  for filename in filelist:
      print filename[0]
      name = filename[0][len(ofolder):]
      print name
      file_o, created = File.objects.get_or_create(site=site, filename=name)
      if not created:
        old_files.remove(file_o.filename)
      print old_files
  for file_o in old_files:
    file_lol = File.objects.get(site=site,filename=file_o)
    print file_o
    File.delete(file_lol)
  
  

    
def add_nodes(data, site, active=None):
    #import networkx as nx
    #G = nx.DiGraph()
    tasks = Task.objects.filter(site=site)
    edges = []
    for task in tasks:
        for succ in task.successors.all():
            edges.append(["task%d" % task.id, "task%d" % succ.id])
    
    #layout = nx.spring_layout(G)
    nodes = [ TaskNode(task.id, task.x_pos , task.y_pos , task, task==active)
            for task in tasks ]
    data["edges"] = edges
    data["nodes"] = nodes
    

def timesince(dt, end=None, default="instantly"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    if end == None:
        now = datetime.now().replace(tzinfo=None)
    else:
        now  = end.replace(tzinfo=None)

    diff = now - dt.replace(tzinfo=None)


    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return u"%d %s" % (period, singular if period == 1 else plural)
    return default


@login_required(login_url="/login/")
def index(request):
    user = request.user
    tasks = Task.objects.all()
    sites = Site.objects.filter(active=True)
    GET = request.GET

    data = {}
    if GET.get("site", False):
        tasks = tasks.filter(site__id=GET["site"])
        for site in sites:
            if site.id == GET["site"]:
                site.task_url_active = True
                data["site"] = site
    else:
        tasks= tasks.filter(site__active=True)
    site_param = GET.copy()
    for site in sites:
        site_param["site"] = site.id
        site.task_url = "?" + "&".join(["%s=%s" % (k,v) for k,v in site_param.items()])

    user_tasks = tasks.filter(assignee=user)
    outstanding = user_tasks.filter(job_status=STATUS_LOOKUP["INPROGRESS"])
    if  user.has_perm('web.can_edit'):
        validation_req =  tasks.filter(job_status=STATUS_LOOKUP["VALIDATE"])
    else:
        validation_req =  user_tasks.filter(job_status=STATUS_LOOKUP["VALIDATE"])
    future = user_tasks.filter(job_status=STATUS_LOOKUP["NOTDONE"])
    completed = user_tasks.filter(job_status=STATUS_LOOKUP["DONE"])
    overview = tasks.exclude(job_status=STATUS_LOOKUP["DONE"]).exclude(job_status=STATUS_LOOKUP["NOTDONE"]).exclude(assignee=user)
    data["user_task"] = user_tasks
    data["outstanding"] = outstanding
    data["validation_req"] = validation_req
    data["future"] = future
    data["completed"] = completed
    data["overview"] = overview
    data["tasks"] = tasks
    data["sites"] = sites

    return render_to_response('index.html', data, context_instance=RequestContext(request) )

def login(request):
    return render_to_response('login.html', {} )
    

@login_required(login_url="/login")
def task(request, site, task_id):
    JOB_STATUS = ((u'1', u'Either the dependencies of the task have not been met or the site has not been run yet.'),
              (u'2', u'The system is transerring files from the server to the host machine.'),
              (u'3', u'The task has been started and is awaiting completion'),
              (u'4', u'The system is transerring files from the host machine to the server.'),
              (u'5', u'Task has been completed and is awaiting validation.'),
              (u'6', u'The task has been successfully completed.'),
              (u'7', u'The task has failed. Please check the log to determine the source of failure.'))
    STATUS_DESC_LOOKUP = {}
    for k,v in JOB_STATUS: STATUS_DESC_LOOKUP[k] = v
    sites = Site.objects.filter(active=True)
    task = Task.objects.get(id=task_id)
    user = request.user
    files = task.input_files.all()
    data = {'task':task, 'files': files, 'site': site, 'sites':sites}
    interface = FileInterface(task,True)
    file_interface = interface.getInterface()
    data["file_interface"] = file_interface
    print task.job_status
    if task.job_status == STATUS_LOOKUP["INPROGRESS"]:
        data["started"] = u"Started: %s ago" % timesince(task.started)
        if task.job_type.type == TYPE_LOOKUP["USER"] and user == task.assignee:
            data["progress"] = True
    elif task.job_status == STATUS_LOOKUP["DONE"] or \
        task.job_status == STATUS_LOOKUP["VALIDATE"]:
        data["started"] = u"The task was completed in:  %s" % timesince(task.started, task.ended)
    if task.job_type.type != TYPE_LOOKUP["USER"]:
        data["server_task"] = True
        if task.job_status == STATUS_LOOKUP["FAILED"]:
            data["failed_button"] = True
    elif task.job_status == STATUS_LOOKUP["VALIDATE"] and user.has_perm('web.edit_task'):
        data["validate_button"] = True
    elif task.job_status == STATUS_LOOKUP["FAILED"]:
        data["failed_button"] = True
    if user.has_perm('web.can_edit'):
        data["edit"] = True
    #print STATUS_DESC_LOOKUP
    data["site"] = task.site
    task.status_display = STATUS_DESC_LOOKUP[task.job_status]
    if user == task.assignee or user.has_perm('web.edit_task'):
        return render_to_response('task.html', data, context_instance=RequestContext(request))
    else:
        return HttpResponse("Not your task")

@login_required(login_url="/login")
def finish_task(request):
    if request.method == "POST":
        if request.POST.get("task_id","") != "":
            user = request.user
            task_id = request.POST["task_id"]
            task = Task.objects.get(id=task_id)
            if task.assignee == user:
                transfer_back(task)
        elif request.POST.get("validate_task", "") != "":
            user= request.user
            task_id = request.POST["validate_task"]
            task = Task.objects.get(id=task_id)
            if user.has_perm('web.can_edit'):
                finish_process_task(task)
            pass
        elif request.POST.get("retry_task", "") != "":
            task_id = request.POST["retry_task"]
            task = Task.objects.get(id=task_id)
            run_process_task(task)
        return redirect('web.views.task', site=task.site.id, task_id=task.id)

@login_required(login_url="/login")
def start_transfer(request):
    if request.method == "POST":
        user = request.user
        if request.POST.get("task_id","") != "":
            print request.POST.get("task_id","")
            task_id = request.POST["task_id"]
            task = Task.objects.get(id=task_id)
            type_files = request.POST["files"]
            print type_files
            host = Host.objects.get(user=user, primary=True)
            transfer_files(task, type_files, host=host)
        elif request.POST.get("validate_task", "") != "":
            pass
        return redirect('web.views.task', site=task.site.id, task_id=task.id)

@login_required(login_url="/login")
def upload(request):
    if request.method == "POST":
        user = request.user
        task_id = request.POST["task_id"]
        task = Task.objects.get(id=task_id)
        host = Host.objects.get(user=user, primary=True)
        transfer_back_files(task,host=host )
        return redirect('web.views.task', site=task.site.id, task_id=task.id)


@permission_required('web.edit_task', login_url="/login/")
def edit_task(request, site, task_id):
    sites = Site.objects.filter(active=True)
    task = Task.objects.get(id=task_id)
    #print task.site
    if request.method =="GET":
        form = TaskForm(instance=task)
        interface = FileInterface(task)
        file_interface = interface.getInterface()
        data = {'form':form, 'task': task, 'sites': sites, "file_interface": file_interface, "site":task.site }
        add_nodes(data, task.site, task)   
        return render_to_response('edit.html', data ,
                context_instance=RequestContext(request) )
    elif request.method == "POST":
        #print request.POST
        form = TaskForm(request.POST,instance=task )
        if form.is_valid():
            form.save()
            tasks = Task.objects.filter(successors=task)
            for old in tasks:
                old.successors.remove(task)
            tasks = task.predecessors.all()
            for pred in tasks:
                pred.successors.add(task)
                pred.save()
            return redirect('web.views.view_site', site=site)
    interface = FileInterface(task)
    file_interface = interface.getInterface()
    data = {'form':form, 'task': task, 'sites': sites, "file_interface": file_interface, "site":task.site }
    add_nodes(data, task.site, task)   
    return render_to_response('edit.html',data,
        context_instance=RequestContext(request) )
        
@permission_required('web.edit_task', login_url="/login/")
def delete_task(request):
    if request.method =="POST":
        task = Task.objects.get(id=request.POST["task_id"])
        site = task.site
        task.delete()
        return redirect('web.views.view_site', site=site.id)


@permission_required("web.edit_task", login_url="/login/")
def start_file_scan(request):
    if request.method == "POST":
      site_id = request.POST["site"]
      site = Site.objects.get(id=site_id)
      rescan(site)
      return redirect('web.views.view_site', site=site.id)

@login_required(login_url="/login/") 
def place_node(request):
    if request.method == "POST":
      task_id = int(request.POST["task"][4:])
      print task_id
      x = int(float(request.POST["x_pos"]))
      y = int(float(request.POST["y_pos"]))
      task = Task.objects.get(id=task_id)
      task.x_pos = x
      task.y_pos = y
      task.save()
      return HttpResponse('good')

@login_required(login_url="/login/")
def view_site(request, site):
    sites = Site.objects.filter(active=True)
    site = Site.objects.get(id=site)
    tasks = Task.objects.filter(site=site)
    
    interface = FileInterface(site=site)
    file_interface = interface.getInterface()

    categories = Category.objects.all()
    user_form = AddUserTaskForm()
    server_form = AddServerTaskForm()
    job_form = JobForm()
    category_form = CategoryForm()
    jobs = Job.objects.all()
    data = {'tasks':tasks, 'user_form': user_form,
        'server_form':server_form, 'site_id':site.id, 'job_form': job_form, 'jobs':jobs,
        'categories': categories, 'category_form': category_form,
        'site':site, 'sites': sites, 'file_interface': file_interface}
    add_nodes(data, site )   
    return render_to_response('site.html', data 
        ,context_instance=RequestContext(request) )

def detectCycles(nodes, edges, start, current):
    if nodes[current] and current == start:
      return False
    if nodes[current]:
      return True
    nodes[current] = True
    for id in edges[current]:
        if not detectCycles(nodes, edges,start, id):
          return False
    return True
          
        
@permission_required('web.edit_task', login_url="/login/")
def add_dependency(request):
    if request.method == "POST":
        site_id= request.POST["site"]
        sourceId = int(request.POST["sourceId"][4:])
        targetId = int(request.POST["targetId"][4:])
        
        site = Site.objects.get(id=site_id)
        
        visited = {}
        edges = {}
        for task in Task.objects.filter(site=site):
            visited[task.id] = False
            edges[task.id] = []
            for task2 in task.successors.all():
                edges[task.id].append(task2.id)
        edges[sourceId].append(targetId)
        if detectCycles(visited, edges, sourceId, sourceId):
          source = Task.objects.get(site=site,id=sourceId)
          target = Task.objects.get(site=site,id=targetId)
          source.successors.add(target)
          target.predecessors.add(source)
          return HttpResponse("good")
    return HttpResponse("bad")
       


@permission_required('web.edit_task', login_url="/login/")
def remove_dependency(request):
    if request.method == "POST":
        site_id= request.POST["site"]
        sourceId = int(request.POST["sourceId"][4:])
        targetId = int(request.POST["targetId"][4:])
        site = Site.objects.get(id=site_id)
        source = Task.objects.get(site=site,id=sourceId)
        target = Task.objects.get(site=site,id=targetId)
        source.successors.remove(target)
        target.predecessors.remove(source)
    return HttpResponse("good")


@permission_required('web.edit_task', login_url="/login/")
def add_task(request):
    if request.method == 'POST':
        type = request.POST["job_type"]
        site = Site.objects.get(id=request.POST["site_id"])
        try:
            job_type = Job.objects.get(id=type)
        except:
            return redirect('web.views.view_site', site=site.id)
        task = Task.objects.create(job_type=job_type, site=site)
        if job_type.type != TYPE_LOOKUP["USER"]:
            print User.objects.get(username='server')

            task.assignee = User.objects.get(username='server')
        task.save()
        id = task.id
        return redirect('web.views.edit_task', site=request.POST["site_id"], task_id=task.id)

@permission_required('web.edit_task', login_url="/login")
def run_task(request):
    if request.method == "POST":
        tasks = Task.objects.filter(job_status=STATUS_LOOKUP["NOTDONE"])
        if request.POST.get("site", "") != "":
            tasks = tasks.filter(site__id=request.POST["site"])
        for t in tasks:
            can_execute = True
            for pred in t.predecessors.all():
                if pred.job_status != STATUS_LOOKUP["DONE"]:
                    can_execute = False
                    break
            if can_execute:
                print "Executing task"
                run_process_task(t)

        tasks = Task.objects.filter(job_status=STATUS_LOOKUP["TRANSFER_BACK"])
        for t in tasks:
            print "Executing task"
            run_process_task(t)
        return redirect(request.POST["next"])

@permission_required('web.edit_task')
def add_job(request):
    job_dict = {}
    if request.method == "GET":
        job_type = request.GET["job_type"]
        if job_type == TYPE_LOOKUP["USER"]:
            job = Job.objects.create(name="User Job", type=job_type)
            job.save()
            job_dict['name'] = 'User Job'
            job_dict['type'] = job_type
            job_dict['id'] = job.id
        else:
            job = Job.objects.create(name="Server Job", type=TYPE_LOOKUP["SERVER-1-1"])
            job.save()
            job_dict['name'] = 'Server Job'
            job_dict['type'] = '2'
            job_dict['id'] = job.id
        return HttpResponse(json.dumps(job_dict), mimetype="application/json")

@permission_required('web.edit_task')
def get_job(request):
    job_dict = {}
    if request.method == "GET":
        job_id = request.GET["job_id"]
        job = Job.objects.get(id=job_id)
        job_dict['name'] = job.name
        job_dict['type'] = job.type
        job_dict['id'] = job.id
        job_dict['category'] = job.category.id
        job_dict['description'] = job.description
        job_dict['script'] = job.script


        return HttpResponse(json.dumps(job_dict), mimetype="application/json")


@permission_required('web.edit_task')
def update_job(request):
    if request.method == 'POST':
        id = request.POST["id"]
        form = JobForm(request.POST, instance=Job.objects.get(id=id))
        if form.is_valid():
            form.save()
        return redirect(request.META['HTTP_REFERER'])

@permission_required('web.edit_task')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            Category.objects.get_or_create(**form.cleaned_data)

        return redirect(request.META['HTTP_REFERER'])

@login_required(login_url="/login")
def sites(request):
    sites = Site.objects.filter(active=True)
    inactive = Site.objects.filter(active=False)
    form = SiteForm()
    return render_to_response('sites.html', {'sites':sites,'inactive': inactive, 'form':form  },
        context_instance=RequestContext(request) )

@permission_required('web.edit_task', login_url="/login")
def add_site(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            template_site = form.cleaned_data["template"]
            site_id = form.cleaned_data["id"]
            form.save()
            site = Site.objects.get(id=site_id)
            task_map = {}
            id_map = {}
            server_user = User.objects.get(username="server")
            if template_site != None:
                template_tasks = Task.objects.filter(site=template_site)
                for t_task in template_tasks:
                    new_task = Task.objects.create(priority=t_task.priority,
                            site=site, job_type=t_task.job_type,
                            output_folder=t_task.output_folder,
                            job_status=STATUS_LOOKUP["NOTDONE"])
                    if t_task.assignee == server_user:
                        new_task.assignee = server_user
                        new_task.save()
                    id_map[t_task.id] = new_task.id
                    task_map[t_task.id] = t_task
                    task_map[new_task.id] = new_task

                for t_task in template_tasks:
                    for succ in t_task.successors.all():
                        task_map[id_map[t_task.id]].successors.add(task_map[id_map[succ.id]])
                        task_map[id_map[succ.id]].predecessors.add(task_map[id_map[t_task.id]])
                #ADD FILES
                root = SiteDir.objects.get().root_dir
                ofolder = "%s/%s/" % (root, site.folder_name)
                try:
                    os.mkdir(ofolder)
                except OSError as exc: # Python >2.5
                    pass
                filelist = Directory(ofolder).getFileList()
                for filename in filelist:
                    name = filename[0][len(ofolder)+1:]
                    file_o, created = File.objects.get_or_create(site=site, filename=name)
            return redirect('web.views.view_site', site=form.cleaned_data["id"])







