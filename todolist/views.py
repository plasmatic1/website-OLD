from datetime import timedelta, date

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Field
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from todolist.models import Problem, VALID_PROBLEM_TYPES, Subject, Homework, Project
from todolist.util.parse_problem_url import parse_problem_url, InvalidURLDomain
from todolist.util.remove_items import remove_item_view


def index(_):
    """
    Index page.  Just redirects to the problem list
    :param _: Request object
    :return:
    """
    # context = {}
    #
    # return render(req, 'todolist/index.html', context)
    return redirect('todolist:problems')


# OJ PROBLEMS

PROBLEM_TYPE_FIELD_CHOICES = (('auto', 'auto'),) + tuple(zip(VALID_PROBLEM_TYPES, VALID_PROBLEM_TYPES))


class ProblemForm(forms.Form):
    """
    Form for adding todo problems
    """
    link = forms.CharField(max_length=128, label='Link', widget=forms.TextInput(attrs={'size': 25}), required=True)
    name = forms.CharField(max_length=64, label='Name (generated if type is "auto")', required=False)
    type = forms.ChoiceField(choices=PROBLEM_TYPE_FIELD_CHOICES, initial='auto', label='Type:', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('link'),
            Row('name'),
            Row('type'),
            Row(Submit('submit', 'Add'))
        )

    def clean(self):
        """
        Clean method override.  This override primarily deals with the "auto" type option
        :return:
        """

        cleaned_data = super().clean()

        if cleaned_data.get('type') == 'auto':
            problem_link = cleaned_data.get('link')
            try:
                problem_type, problem_name = parse_problem_url(problem_link)
                cleaned_data['type'] = problem_type
                cleaned_data['name'] = problem_name
            except InvalidURLDomain as e:
                if problem_link:
                    self.add_error('link', str(e))

        return cleaned_data


def problems(req):
    """
    Deals with requests to the "problems" path
    :param req: Request object
    :return:
    """

    form = ProblemForm(req.POST or None)

    if req.user.is_authenticated and form.is_valid():
        problem = Problem(**form.cleaned_data, user=req.user)
        problem.save()
        form = ProblemForm()
        messages.success(req, 'Added problem!')

    context = {'form': form,
               'problems': Problem.objects.filter(user=req.user).order_by('type').order_by(
                   'link') if req.user.is_authenticated else []}
    return render(req, 'todolist/problems.html', context)


remove_problem = remove_item_view(Problem, 'todolist:problems')


# HOMEWORK

class SubjectForm(forms.Form):
    """
    Form for adding subjects
    """
    name = forms.CharField(max_length=64, label='Name', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('name'),
            Row(Submit('submit', 'Add Subject'))
        )


ONE_DAY = timedelta(days=1)


def tommorow():
    """
    Tommorow's date
    :return: Tommorow's date
    """
    return date.today() + ONE_DAY


class HomeworkForm(forms.Form):
    name = forms.CharField(max_length=256, label='Name')
    subject = None
    due_date = forms.DateField(label='Due Date', required=True, initial=tommorow, widget=DatePickerInput())
    comments = forms.CharField(max_length=1024, label='Comments', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('req').user
        super().__init__(*args, **kwargs)

        if user.is_authenticated:
            choices = [(subject.id, subject.name) for subject in
                       Subject.objects.filter(user=user).order_by('name').all()]
        else:
            choices = []

        self.fields['subject'] = forms.ChoiceField(
            choices=choices, label='Subject',
            required=True, widget=forms.Select(attrs={'size': len(choices)}))

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('name'),
            Row('subject'),
            Row('due_date'),
            Row(Field('comments', rows='2', style='resize: none;')),
            Row(Submit('submit', 'Add Homework'))
        )

    def clean(self):
        """
        Validates "add homework" form.  Currently it just checks that the subject is valid and then sets it
        :return: Cleaned data
        """

        cleaned_data = super().clean()

        try:
            subject_id = int(cleaned_data.get('subject'))
            subject = Subject.objects.get(pk=subject_id)
            cleaned_data['subject'] = subject
        except TypeError:
            pass  # Assume the homework was not added using the proper form stuffs
        except ValueError:
            self.add_error('subject', 'Subject ID must be int!')
        except Subject.DoesNotExist:
            self.add_error('subject', f'Subject with id {subject_id} does not exist!')

        return cleaned_data


def homework(req):
    """
    Handles requests to the "homework" page
    :param req: The request
    :return:
    """

    homework_form = HomeworkForm(req=req)
    subject_form = SubjectForm()

    if req.user.is_authenticated:
        submit = req.POST.get('submit')
        if submit == 'Add Homework':
            homework_form = HomeworkForm(req.POST or None, req=req)
            if homework_form.is_valid():
                homework = Homework(**homework_form.cleaned_data, user=req.user)
                homework.save()
                messages.success(req, 'Added Homework!')

                homework_form = HomeworkForm(req=req)

        if submit == 'Add Subject':
            subject_form = SubjectForm(req.POST or None)
            if subject_form.is_valid():
                subject = Subject(**subject_form.cleaned_data, user=req.user)
                subject.save()
                messages.success(req, 'Added subject!')

                subject_form = SubjectForm()
                homework_form = HomeworkForm(req=req)  # Reload

    context = {'subject_form': subject_form, 'homework_form': homework_form,
               'subjects': Subject.objects.all().filter(user=req.user).order_by(
                   'name') if req.user.is_authenticated else [],
               'homeworks': Homework.objects.all().filter(user=req.user).order_by(
                   'due_date') if req.user.is_authenticated else []}
    return render(req, 'todolist/homework.html', context)


remove_subject = remove_item_view(Subject, 'todolist:homework')
remove_homework = remove_item_view(Homework, 'todolist:homework')


# PROJECTS


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=256, label='Name')
    description = forms.CharField(max_length=1024, label='Description', widget=forms.Textarea, initial='',
                                  required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('name'),
            Row(Field('description', rows='4', style='resize: none;')),
            Row(Submit('submit', 'Add Project'))
        )


def projects(req):
    project_form = ProjectForm(req.POST or None)
    if project_form.is_valid():
        project = Project(**project_form.cleaned_data, user=req.user)
        project.save()
        messages.success(req, 'Added project!')
        project_form = ProjectForm()

    context = {
        'projects': Project.objects.filter(user=req.user).order_by('name').all() if req.user.is_authenticated else [],
        'form': project_form
    }

    return render(req, 'todolist/projects.html', context)


remove_project = remove_item_view(Project, 'todolist:projects')
