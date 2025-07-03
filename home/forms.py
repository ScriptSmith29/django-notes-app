from django import forms
from .models import Note, Tag
from tinymce.widgets import TinyMCE

class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),  # Overridden in __init__
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2 text-gray-900 dark:text-white'
        })
    )

    new_tags = forms.CharField(
        required=False,
        label="Add new tags (comma-separated)",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded bg-white text-gray-900 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'e.g. Django, React'
        })
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'attachment', 'is_important', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded bg-white text-gray-900 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded bg-white text-gray-900 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter content'
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700 dark:text-white border rounded p-2 dark:bg-gray-700 dark:border-gray-600'
            }),
            'is_important': forms.CheckboxInput(attrs={
                'class': 'ml-2 accent-blue-600 dark:accent-blue-400'  # ✅ Fix for checkbox color
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['tags'].queryset = Tag.objects.filter(user=self.user)

    def save(self, commit=True):
        note = super().save(commit=False)
        if self.user:
            note.user = self.user
        if commit:
            note.save()
        self.save_m2m()
        note.tags.set(self.cleaned_data['tags'])
        new_tags = self.cleaned_data.get('new_tags', '')
        tag_names = [name.strip() for name in new_tags.split(',') if name.strip()]
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name, user=self.user)
            note.tags.add(tag_obj)
        return note
