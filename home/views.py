from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .forms import NoteForm
from .models import Note
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import uuid
import os
from django.core.files.storage import default_storage


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log user in after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})

@login_required
def home(request):
    query = request.GET.get('q', '')
    notes = Note.objects.filter(user=request.user).prefetch_related('tags')

    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    notes = notes.order_by('-is_important', '-updated')

    # PAGINATION: 5 notes per page
    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/home.html', {
        'notes': page_obj,
        'query': query,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'home/note_detail.html', {'note': note})


def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Note added successfully!")
            return redirect('home')
    else:
        form = NoteForm(user=request.user)

    return render(request, 'home/note_form.html', {'form': form})



@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm(instance=note, user=request.user)

    return render(request, 'home/note_form.html', {'form': form})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'home/delete_confirm.html', {'note': note})

@login_required
def toggle_important(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.is_important = not note.is_important
    note.save()
    return redirect('home')

@csrf_exempt
def tinymce_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        upload = request.FILES['file']
        ext = os.path.splitext(upload.name)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = default_storage.save(f'uploads/{filename}', upload)
        file_url = default_storage.url(filepath)
        return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

"""
messages.success(request, "Note created!")
messages.error(request, "Something went wrong.")
"""