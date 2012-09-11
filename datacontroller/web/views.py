from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from web.models import Task, Site, STATUS_LOOKUP
from web.run_task import transfer_back, transfer_files,  transfer_back_files
from datetime import datetime

def timesince(dt, end=None, default="just now"):
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

login_required(login_url="/login/")
def index(request):
    user = request.user
    tasks = Task.objects.filter(site__active=True) #Active sites

    sites = Site.objects.filter(active=True)
    GET = request.GET
    exclude = GET.get('exclude', '').split(',')
    for i in xrange(len(sites)):
        if sites[i].id in exclude:
            sites[i].filtered = True
    for ex in exclude:
        tasks = tasks.exclude(site__id=ex)
    user_tasks = tasks.filter(assignee=user)
    return render_to_response('index.html', {'user_tasks':user_tasks,
        'sites': sites, 'tasks': tasks} )

def login(request):
    return render_to_response('login.html', {} )

@login_required(login_url="/login")
def task(request, site, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    files = task.input_files.all()
    data = {'task':task, 'files': files}
    if task.job_status == STATUS_LOOKUP["INPROGRESS"]:
        data["started"] = u"Started: %s ago" % timesince(task.started)
        data["progress"] = True
    elif task.job_status == STATUS_LOOKUP["DONE"] or \
        task.job_status == STATUS_LOOKUP["VALIDATE"]:
        data["started"] = u"Finished: %s" % timesince(task.started, task.ended)

    if user != task.assignee:
        return HttpResponse("Not your task")
    else:
        return render_to_response('task.html', data, context_instance=RequestContext(request))

@login_required(login_url="/login")
def finish_task(request):
    if request.method == "POST":
        user = request.user
        task_id = request.POST["task_id"]
        task = Task.objects.get(id=task_id)
        if task.assignee == user:
            transfer_back(task)
        return redirect('web.views.task', site=task.site.id, task_id=task.id)

@login_required(login_url="/login")
def start_transfer(request):
    if request.method == "POST":
        user = request.user
        task_id = request.POST["task_id"]
        task = Task.objects.get(id=task_id)
        type_files = request.POST["files"]
        print type_files
        transfer_files(task, type_files)
        return redirect('web.views.task', site=task.site.id, task_id=task.id)

@login_required(login_url="/login")
def upload(request):
    if request.method == "POST":
        user = request.user
        task_id = request.POST["task_id"]
        task = Task.objects.get(id=task_id)
        transfer_back_files(task)
        return redirect('web.views.task', site=task.site.id, task_id=task.id)





# Create your views here.
