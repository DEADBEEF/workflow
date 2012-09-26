from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from web.models import Task, Site, STATUS_LOOKUP, Job, TYPE_LOOKUP, Host, Category, SiteDir
from web.run_task import transfer_back, transfer_files,  transfer_back_files
from web.run_task import run_task as run_process_task
from web.run_task import finish_task as finish_process_task
from web.directoryIndex import Directory
from datetime import datetime
from web.forms import TaskForm, AddUserTaskForm, AddServerTaskForm, JobForm, CategoryForm, SiteForm
import json
import os


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
    tasks = Task.objects.filter(site__active=True) #Active sites

    sites = Site.objects.filter(active=True)
    GET = request.GET
    exclude = GET.get('exclude', '').split(',')
    for i in xrange(len(sites)):
        if sites[i].id in exclude:
            sites[i].filtered = True
            sites[i].url = ",".join([ x for x in exclude if x != sites[i].id and x != "" ])
        else:
            sites[i].url = ",".join(exclude + [sites[i].id])
    for ex in exclude:
        tasks = tasks.exclude(site__id=ex)
    user_tasks = tasks.filter(assignee=user)
    return render_to_response('index.html', {'user_tasks':user_tasks,
        'sites': sites, 'tasks': tasks} )

def login(request):
    return render_to_response('login.html', {} )

@login_required(login_url="/login")
def task(request, site, task_id):
    sites = Site.objects.filter(active=True)
    task = Task.objects.get(id=task_id)
    user = request.user
    files = task.input_files.all()
    data = {'task':task, 'files': files, 'site': site, 'sites':sites}
    if task.job_status == STATUS_LOOKUP["INPROGRESS"]:
        data["started"] = u"Started: %s ago" % timesince(task.started)
        data["progress"] = True
    elif task.job_status == STATUS_LOOKUP["DONE"] or \
        task.job_status == STATUS_LOOKUP["VALIDATE"]:
        data["started"] = u"Finished: %s" % timesince(task.started, task.ended)
    if task.job_type.type != TYPE_LOOKUP["USER"]:
        data["server_task"] = True
    elif task.job_status == STATUS_LOOKUP["VALIDATE"] and user.has_perm('web.can_edit'):
        data["validate_button"] = True
    if user.has_perm('web.can_edit'):
        data["edit"] = True
    if user != task.assignee or user.has_perm('web.can_edit'):
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
    if request.method =="GET":
        form = TaskForm(instance=task)
        print dir(form)
        return render_to_response('edit.html', {'form':form, 'task': task, 'sites': sites },
                context_instance=RequestContext(request) )
    elif request.method == "POST":
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
    return render_to_response('edit.html', {'form':form, 'task': task, 'sites':sites },
        context_instance=RequestContext(request) )

class TaskNode:
    def __init__(self, id, x, y, task):
        self.id = id
        self.x = x
        self.y = y
        self.task = task
        self.assigned = True
        files = self.task.input_files.all()
        self.files = "%d input file%s" % (len(files), ("s", "")[len(files) == 1] )
        if task.job_status == STATUS_LOOKUP["FAILED"] or \
            task.assignee == None:
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



@login_required(login_url="/login/")
def view_site(request, site):
    sites = Site.objects.filter(active=True)
    site = Site.objects.get(id=site)
    tasks = Task.objects.filter(site=site) #Active sites
    import networkx as nx
    G = nx.DiGraph()
    for task in tasks:
        G.add_node(task.id, size=200)
    for task in tasks:
        for succ in task.successors.all():
            G.add_edge("task%d" % task.id, "task%d" % succ.id)
    edges = json.dumps(G.edges())
    layout = nx.spring_layout(G)
    print layout
    nodes = [ TaskNode(task.id, layout[task.id][0]*600 + 10, (layout[task.id][1])*250 +10, task)
            for task in tasks ]

    x,y = 650,0
    for node in layout.values():
        x, y = max(x, int(node[0]*600)+50), max(y, int(node[1]*250)+50)
    x += 70
    y += 70
    categories = Category.objects.all()
    user_form = AddUserTaskForm()
    server_form = AddServerTaskForm()
    job_form = JobForm()
    category_form = CategoryForm()
    jobs = Job.objects.all()
    return render_to_response('site.html', {'tasks':tasks, 'user_form': user_form,
        'server_form':server_form, 'site_id':site.id, 'job_form': job_form, 'jobs':jobs,
        'categories': categories, 'category_form': category_form,
        'site':site, 'sites': sites, 'width': x,  'height': y, 'nodes':nodes,
        'edges':edges}
        ,context_instance=RequestContext(request) )

@permission_required('web.edit_task', login_url="/login/")
def add_dependency(request):
    if request.method == "POST":
        site_id= request.POST["site"]
        sourceId = int(request.POST["sourceId"][4:])
        targetId = int(request.POST["targetId"][4:])
        site = Site.objects.get(id=site_id)
        source = Task.objects.get(site=site,id=sourceId)
        target = Task.objects.get(site=site,id=targetId)
        source.successors.add(target)
        target.predecessors.add(source)
    return HttpResponse("good")


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
        job_type = Job.objects.get(id=type)
        site = Site.objects.get(id=request.POST["site_id"])
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







