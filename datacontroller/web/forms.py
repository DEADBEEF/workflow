from django import forms
from django.contrib.auth.models import User
from web.models import Job, Task, TYPE_LOOKUP, Category, Site, File

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('assignee', 'priority', 'input_files', 'output_folder')
        #        'predecessors')
        widgets = {
                    'input_files': forms.CheckboxSelectMultiple(),
        #            'predecessors': forms.CheckboxSelectMultiple()
                }
        required = {'assignee': False }
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        site = instance.site
        print site
        self.fields['input_files'].queryset = File.objects.filter(site=site)
        if instance.job_type.type != TYPE_LOOKUP['USER']:
            self.fields['assignee'].widget = forms.HiddenInput()
        else:
            self.fields['assignee'].queryset = User.objects.exclude(username='server')
        #self.fields['predecessors'].queryset = Task.objects.filter(site=site).exclude(id=instance.id)


class AddUserTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('job_type',)
    def __init__(self, **kwargs):
        super(AddUserTaskForm, self).__init__(**kwargs)
        self.fields['job_type'].queryset = Job.objects.filter(type=TYPE_LOOKUP['USER'])

class AddServerTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('job_type',)
    def __init__(self, **kwargs):
        super(AddServerTaskForm, self).__init__(**kwargs)
        self.fields['job_type'].queryset = Job.objects.exclude(type=TYPE_LOOKUP['USER'])

class JobForm(forms.ModelForm):
    class Meta:
        model = Job

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

class SiteForm(forms.ModelForm):
    template = forms.ModelChoiceField(queryset=Site.objects.all(), empty_label="New workflow",
                            required=False)
    class Meta:
        model = Site

