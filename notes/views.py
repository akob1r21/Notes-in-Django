from django.shortcuts import render, redirect
from .models import Notes
from django.contrib.auth.decorators import login_required



@login_required
def notes_list(request):
    notes = Notes.objects.filter(user=request.user)

    return render(request, 'notes/notes_list.html', {'notes': notes})

@login_required
def create_notes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if not title or not description:
            return render(request, 'notes/create_notes.html', {'error':'all fields necessary'})
        
        note = Notes.objects.create(
            title=title,
            description=description,
            user = request.user
        )

        return redirect('notes')
    
    return render(request, 'notes/create_notes.html', {'title':'Create Notes'})


@login_required
def update_note(request, pk):
    note = Notes.objects.get(pk=pk)
    if request.user!=note.user:
        return render(request, 'notes/create_notes.html', {'error':'You dont have permession'})

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if not title or not description:
            return render(request, 'notes/create_notes.html', {'error':'all fields necessary'})
        
        if request.user==note.user:
            note.title = title
            note.description = description
            note.save()

            return redirect('notes')
    
    return render(request, 'notes/create_notes.html', {'title':'Update Notes', 'note':note})


@login_required
def delete_note(request, pk):
    
    note = Notes.objects.get(pk=pk)
    if request.user!=note.user:
        return render(request, 'notes/delete.html', {'error':'You dont have permession'})
    
    if request.method=='POST':
        if request.user == note.user:
            note.delete()
            return redirect('notes')
    
    return render(request, 'notes/delete.html', {'note': note})

