from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Message, Comment
from ..login_registration.models import User
import types

# displays login and registration page
def index(request):
    return render(request, 'user_dashboard/index.html')

# displays page containing info about this app
def about(request):
    return render(request, 'user_dashboard/about.html')

# displays a dashboard containing user info
# if current user is an admin, allows user to edit other user info or remove another user altogether
def dashboard(request):
    context = {
        'users': User.objects.all()
    }
    if request.session['user_level'] == 9:
        return render(request, 'user_dashboard/admin_dashboard.html', context)
    else:
        return render(request, 'user_dashboard/user_dashboard.html', context)

# displays form page that allows admin user to create a new User object
def new(request):
    return render(request, 'user_dashboard/add.html')

# displays page containing user information, messages, and comments
def show(request, id):
    context = {
        'user': User.objects.get(id=id),
        'user_messages': Message.objects.filter(written_to=id),
        'user_comments': Comment.objects.all()
    }
    return render(request, 'user_dashboard/show.html', context)

# displays form page that allows user to edit information
# if current user is an admin, allows user to change user level
def edit(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'user_dashboard/edit.html', context)

# posts messsages to another user's profile page
def post_message(request, id):
    if request.method != 'POST':
        return redirect(reverse('user_dashboard:show', kwargs={'id': id}))
    else:
        message = Message.objects.post_message(request.POST, id, request.session['user_id'])
        if isinstance(message, types.ListType):
            for error in message:
                messages.error(request, error)
        return redirect(reverse('user_dashboard:show', kwargs={'id': id}))

# posts comments connected to another user's message
def post_comment(request, id):
    if request.method != 'POST':
        return redirect(reverse('user_dashboard:show', kwargs={'id': id}))
    else:
        comment = Message.objects.post_comment(request.POST, id, request.session['user_id'])
        message = Message.objects.get(id=id)
        user = User.objects.get(id=message.written_to.id)
        if isinstance(comment, types.ListType):
            for error in comment:
                messages.error(request, error)
        return redirect(reverse('user_dashboard:show', kwargs={'id': user.id}))
