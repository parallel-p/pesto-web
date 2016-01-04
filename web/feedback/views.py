from django.shortcuts import render
from django import forms
from .models import Message
from django.contrib.admin.views.decorators import staff_member_required

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    text = forms.CharField(max_length=2016)

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        message = Message()
        message.name = form.data['name']
        message.text = form.data['text']
        message.save()

    form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})

@staff_member_required
def admin(request):
    messages = Message.objects.all()
    return render(request, 'feedback_admin.html', {'messages': messages})
