from django.shortcuts import render,get_object_or_404,redirect
from .models import ChatGroup,GroupMessage
from django.contrib.auth.decorators import login_required
from .forms import ChatmessageCreateForm
# Create your views here.
@login_required
def chat_view(request):
    chat_group=get_object_or_404(ChatGroup,group_name='public_test_chat')
    chat_messages=GroupMessage.objects.filter(group=chat_group)
    form=ChatmessageCreateForm()
    if request.htmx:
        form=ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.author=request.user
            message.group=chat_group
            message.save()
            context={
                'message':message,
                'user':request.user,
            }
            return render(request,'a_rtchat/partials/chat_message_p.html',context)
    return render(request,'a_rtchat/chat.html',{'chat_messages':chat_messages,'form':form})
