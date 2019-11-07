from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Field
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from todolist.models import Problem, VALID_PROBLEM_TYPES, Subject, Homework


def index(_):
    # context = {}
    #
    # return render(req, 'todolist/index.html', context)
    return redirect('todolist:problems')


# OJ PROBLEMS

class ProblemForm(forms.Form):
    """
    Form for adding todo problems
    """
    link = forms.CharField(max_length=128, label='Link', required=True)
    name = forms.CharField(max_length=64, label='Name', required=False)
    type = forms.ChoiceField(choices=tuple(zip(VALID_PROBLEM_TYPES, VALID_PROBLEM_TYPES)), label='Type:', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('link'),
            Row('name'),
            Row('type'),
            Row(Submit('submit', 'Add'))
        )


def problems(req):
    form = ProblemForm(req.POST or None)

    if form.is_valid() and req.user.is_authenticated:
        problem = Problem(**form.cleaned_data)
        problem.save()
        form = ProblemForm()
        messages.success(req, 'Added problem!')

    context = {'form': form,
               'problems': Problem.objects.order_by('type').order_by('link')}
    return render(req, 'todolist/problems.html', context)


@login_required(login_url='/login')
def remove_problem(req, problem_id):
    if req.user.is_authenticated:
        Problem.objects.filter(pk=problem_id).delete()
        messages.success(req, 'Removed problem!')
    else:
        messages.error(req, 'Insufficient permissions!')

    return redirect('todolist:problems')


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


class HomeworkForm(forms.Form):
    name = forms.CharField(max_length=256, label='Name')
    subject = None
    due_date = forms.DateField(label='Due Date', required=True, widget=forms.SelectDateWidget)
    comments = forms.CharField(max_length=1024, label='Comments', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subject'] = forms.ChoiceField(
            choices=[(subject.id, subject.name) for subject in Subject.objects.all()], label='Subject',
            required=True)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('name'),
            Row('subject'),
            Row('due_date'),
            Row(Field('comments', rows='2')),
            Row(Submit('submit', 'Add Homework'))
        )

    def clean(self):
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
    subject_form = SubjectForm(req.POST or None)
    homework_form = HomeworkForm(req.POST or None)

    if req.user.is_authenticated:
        submit = req.POST.get('submit')
        if submit == 'Add Homework' and homework_form.is_valid():
            homework = Homework(**homework_form.cleaned_data)
            homework.save()
            messages.success(req, 'Added Homework!')
            homework_form = HomeworkForm()
        if submit == 'Add Subject' and subject_form.is_valid():
            subject = Subject(**subject_form.cleaned_data)
            subject.save()
            messages.success(req, 'Added subject!')
            subject_form = SubjectForm()

    context = {'subject_form': subject_form, 'homework_form': homework_form,
               'subjects': Subject.objects.all().order_by('name'),
               'homeworks': Homework.objects.all().order_by('due_date')}
    return render(req, 'todolist/homework.html', context)


@login_required(login_url='login/')
def remove_subject(req, subject_id):
    Subject.objects.filter(pk=subject_id).delete()
    messages.success(req, 'Removed subject!')
    return redirect('todolist:homework')


@login_required(login_url='login/')
def remove_homework(req, homework_id):
    Homework.objects.filter(pk=homework_id).delete()
    messages.success(req, 'Removed homework!')
    return redirect('todolist:homework')


def projects(req):
    context = {}

    return render(req, 'todolist/projects.html', context)
