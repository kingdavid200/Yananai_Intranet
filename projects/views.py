from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project, Task
from .forms import ProjectForm, TaskForm


@login_required
def project_list(request):
    user = request.user
    projects = Project.objects.select_related('affiliate', 'owner')

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)

    # Search
    query = request.GET.get('q', '')
    if query:
        projects = projects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'projects': projects,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Project.STATUS_CHOICES,
    }
    return render(request, 'projects/list.html', context)


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.select_related('assigned_to').order_by('status', '-priority')
    return render(request, 'projects/detail.html', {'project': project, 'tasks': tasks})


@login_required
def project_create(request):
    if not request.user.is_staff_member:
        messages.error(request, "You do not have permission to create projects.")
        return redirect('projects:list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            if not project.owner:
                project.owner = request.user
            project.save()
            messages.success(request, f"Project '{project.name}' created.")
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm(initial={'owner': request.user})

    return render(request, 'projects/form.html', {'form': form, 'action': 'Create Project'})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_admin and project.owner != request.user:
        messages.error(request, "You do not have permission to edit this project.")
        return redirect('projects:detail', pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated.")
            return redirect('projects:detail', pk=pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/form.html', {'form': form, 'action': 'Edit Project', 'project': project})


@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if not request.user.is_staff_member:
        messages.error(request, "You do not have permission to add tasks.")
        return redirect('projects:detail', pk=project_pk)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, f"Task '{task.title}' added.")
            return redirect('projects:detail', pk=project_pk)
    else:
        form = TaskForm(initial={'assigned_to': request.user})

    return render(request, 'projects/task_form.html', {'form': form, 'project': project, 'action': 'Add Task'})


@login_required
def task_edit(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(Task, pk=task_pk, project=project)

    if not request.user.is_staff_member:
        messages.error(request, "You do not have permission to edit tasks.")
        return redirect('projects:detail', pk=project_pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated.")
            return redirect('projects:detail', pk=project_pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'projects/task_form.html', {'form': form, 'project': project, 'task': task, 'action': 'Edit Task'})


@login_required
def task_update_status(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(Task, pk=task_pk, project=project)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            messages.success(request, f"Task '{task.title}' moved to {task.get_status_display()}.")

    return redirect('projects:detail', pk=project_pk)
