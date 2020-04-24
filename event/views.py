from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.mail import send_mail
from .models import Events
from .forms import EventPostForm


class EventListView(ListView):
    model=Events
    context_object_name='events'
    template_name='event/home.html'
    ordering=['-date_posted']
    paginate_by=12

    def get_context_data(self, *args, **kwargs):
        data = super(EventListView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Home'
        return data

class UserPostedEventView(ListView):
    model=Events
    context_object_name='events'
    template_name='event/home.html'
    ordering=['-date_posted']
    paginate_by=12

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Events.objects.filter(author=user).order_by('-date_posted')
    def get_context_data(self, *args, **kwargs):
        data = super(UserPostedEventView, self).get_context_data(*args, **kwargs)
        data['title'] = 'UserPosted'
        return data

class EventDetailView(DetailView):
    model=Events
'''
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Events
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Events
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False'''

def about(request):
    return render(request,'event/about.html',{'title':'about'})

@login_required
def post_event(request):
    if request.method == 'POST':
        form=EventPostForm(request.POST,request.FILES)
        if form.is_valid():
            title=request.POST['title']
            description=request.POST['description']
            organizer=request.POST['organizer']
            event_date=request.POST['event_date']
            email=request.POST['email']
            phone=request.POST['phone']
            department=request.POST['department']
            url=request.POST['url']
            poster=request.FILES['poster']
            requested_time=request.POST['requested_time']
            purpose=request.POST['purpose']

            current_user=request.user.id
            author=User.objects.get(id=current_user)


            event=Events(department=department,author=author,title=title,description=description,organizer=organizer,event_date=event_date,email=email,phone=phone,url=url,poster=poster,requested_time=requested_time,purpose=purpose)
            event.save()

            principal=User.objects.get(username='principal')
            send_mail("Subject - New Event Posted", f"Title : {title} \nDescription : {description} \nEventDate : {event_date} \nRequestedTime : {requested_time}", "gokulraj.g103@gmail.com", [principal.email])

            messages.success(request, f'Your form has been updated!')
            return redirect('profile-page')

    else:
        form=EventPostForm()

    context = {
        'form': form,
        'title':'PostEvent',
    }

    return render(request, 'event/events_form.html', context)

@login_required
def principal_decision(request,id):
    if request.user.username=='principal':
        if request.method == 'POST':
            id  = request.POST['id']
            principal_comments=request.POST['principal_comments']
            options=request.POST['options']
            if options=='yes':
                e=Events(id=int(id),is_principal_accepted=1,principal_comments=principal_comments)
                e.save(update_fields=['is_principal_accepted','principal_comments'])

                event=Events.objects.get(id=id)
                send_mail("Subject - New Event Posted", f"Title : {event.title} \nDescription : {event.description} \nEventDate : {event.event_date} \
                 \n Principal accepted : yes \nPrincipal Comments: {event.principal_comments}", "gokulraj.g103@gmail.com", [event.author.email])

                messages.success(request, f'Your decision has been updated!')
                return redirect('requests-page')
            else:
                e=Events(id=int(id),is_principal_accepted=-1,principal_comments=principal_comments)
                e.save(update_fields=['is_principal_accepted','principal_comments'])

                event=Events.objects.get(id=id)
                send_mail("Subject - New Event Posted", f"Title : {event.title} \nDescription : {event.description} \nEventDate : {event.event_date} \
                 \n Principal accepted : no \nPrincipal Comments: {event.principal_comments}", "gokulraj.g103@gmail.com", [event.author.email])


                messages.warning(request, f'Your decision has been updated!')
                return redirect('requests-page')
        object=Events.objects.get(id=id)
        context={
            'object':object,
            'title':'Decision',
        }
        return render(request, 'event/principal_decision.html',context)
    else:
        messages.warning(request, f'Your are not allowed to visit!')
        return redirect('home-page')
@login_required
def requests(request):
    if request.user.username=='principal':
        accepted=[]
        events=Events.objects.all()
        for i in events:
            if i.is_principal_accepted==0:
                accepted.append(i)

        context={
            'events':accepted,
            'title':'request',
        }
        
        return render(request,'event/requests.html',context)
    else:
        messages.warning(request, f'Your not allowed to view this page!')
        return redirect('home-page')
@login_required
def accepted(request):
    accepted=[]
    events=Events.objects.all()
    for i in events:
        if i.is_principal_accepted==1:
            accepted.append(i)

    context={
        'events':accepted,
        'title':'accepted',
    }
    
    return render(request,'event/accepted.html',context)
@login_required
def declined(request):
    accepted=[]
    events=Events.objects.all()
    for i in events:
        if i.is_principal_accepted==-1:
            accepted.append(i)

    context={
        'events':accepted,
        'title':'declined',
    }
    
    return render(request,'event/declined.html',context)



@login_required
def edit_event(request,id):
    if request.method == 'POST':
        form=EventPostForm(request.POST,request.FILES)
        if form.is_valid():
            title=request.POST['title']
            description=request.POST['description']
            organizer=request.POST['organizer']
            event_date=request.POST['event_date']
            email=request.POST['email']
            phone=request.POST['phone']
            department=request.POST['department']
            url=request.POST['url']
            poster=request.FILES['poster']
            requested_time=request.POST['requested_time']
            purpose=request.POST['purpose']

            current_user=request.user.id
            author=User.objects.get(id=current_user)


            event=Events(is_principal_accepted=0,department=department,author=author,title=title,description=description,organizer=organizer,event_date=event_date,email=email,phone=phone,url=url,poster=poster,requested_time=requested_time,purpose=purpose)
            event.save()

            messages.success(request, f'Your form has been updated!')
            return redirect('profile-page')

    else:
        form=EventPostForm(instance=Events.objects.get(id=int(id)))

    context = {
        'form': form,
        'title':'EditEvent',
    }

    return render(request, 'event/events_form.html', context)

@login_required
def change_time(request,id):
    if not request.user.username=='principal':
        if request.method == 'POST':
            id  = request.POST['id']
            requested_time=request.POST['requested_time']
            purpose=request.POST['purpose']

            e=Events(id=int(id),requested_time=requested_time,purpose=purpose,principal_comments='None ',is_principal_accepted=0)
            e.save(update_fields=['is_principal_accepted','principal_comments','requested_time','purpose'])

            principal=User.objects.get(username='principal')
            send_mail("Subject - New Event Posted", f"Title : {title} \nDescription : {description} \nEventDate : {event_date} \n \
                RequestedTime : {requested_time}", "gokulraj.g103@gmail.com", [principal.email])

            messages.success(request, f'Your decision has been updated!')
            return redirect('requests-page')
        object=Events.objects.get(id=id)
        context={
            'object':object,
            'title':'change-timting',
        }
        return render(request, 'event/change_timings.html',context)
    else:
        messages.warning(request, f'Your are not allowed to visit!')
        return redirect('home-page')