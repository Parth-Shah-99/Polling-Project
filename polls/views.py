from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from .forms import UserSignupForm, CreatePollForm, UserUpdateForm
from django.contrib.auth.models import User
from polls.models import Question, Choice, UserProfile, UserVotes
from django.views import generic
from django.core.paginator import Paginator
import json

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'home.html', {})


def signup(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))

    form = UserSignupForm()

    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():

            cleaned_form = form.cleaned_data
            user = User(
                username=cleaned_form['username'],
                first_name=cleaned_form['fname'],
                last_name=cleaned_form['lname'],
                email=cleaned_form['email'],
            )
            password = cleaned_form['password1']
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user, anonymous=cleaned_form['anonymous'])

            messages.success(request, 'You are successfully registered. Please Login to create/answer the Polls.')
            return HttpResponseRedirect(reverse('login'))

    else:
        form.fields['username'].help_text += "<br><b>CAUTION !!</b> Once the account is created, you won't be able to change the Username."
        
    return render(request, 'signup.html', {'form': form})


def profile(request):
    return render(request, 'profile.html', {})


class ProfileView(generic.ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'profile.html'


class ProfilePollsView(generic.ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'pollslist.html'
    paginate_by = 5

    def get_queryset(self):

        if self.request.method == "GET":

            search_text = self.request.GET.get("search_text", None)
            if search_text:
                return Question.objects.filter(question_text__icontains=search_text).order_by("-published_on")
            else:
                return Question.objects.order_by('-published_on')

        return Question.objects.order_by('-published_on')

    def get_context_data(self, *args, **kwargs):

        context = super(ProfilePollsView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated:
            uservotes = UserVotes.objects.filter(user=self.request.user)
            questions_voted = [uservote.question for uservote in uservotes]
            context['questions_voted'] = questions_voted

        return context


class UserProfilePollsView(generic.ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'pollslist.html'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.filter(published_by=self.kwargs.get('username')).order_by('-published_on')

    def get_context_data(self, *args, **kwargs):

        context = super(UserProfilePollsView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated:
            uservotes = UserVotes.objects.filter(user=self.request.user)
            questions_voted = [uservote.question for uservote in uservotes]
            context['questions_voted'] = questions_voted

        context['specific_user'] = self.kwargs.get('username')
        context['specific_user_anonymous'] = User.objects.get(username=self.kwargs.get('username')).userprofile.anonymous
        return context


class ProfileMyPollsView(generic.ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'pollslist.html'
    paginate_by = 5

    def get_queryset(self):
        username = self.request.user.get_username()
        return Question.objects.filter(published_by=username).order_by('-published_on')

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileMyPollsView, self).get_context_data(*args, **kwargs)
        context['mypolls'] = True

        if self.request.user.is_authenticated:
            uservotes = UserVotes.objects.filter(user=self.request.user)
            questions_voted = [uservote.question for uservote in uservotes]
            context['questions_voted'] = questions_voted

        return context


class PollsDetailView(generic.DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'pollsdetail.html'

    def get_context_data(self, *args, **kwargs):

        context = super(PollsDetailView, self).get_context_data(*args, **kwargs)

        question = context['question']
        uservotes = UserVotes.objects.filter(user=self.request.user, question=question)
        if uservotes.exists():
            context['disabled'] = 'disabled'
            context['selected_choice'] = uservotes[0].choice

        return context


class PollsResultView(generic.DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'pollsresult.html'

    def post(self, request, **kwargs):
        q = get_object_or_404(Question.objects.filter(id=self.kwargs['pk']))
        try:
            choice_id = (request.POST['choice'])[6:]
            choice = q.choice_set.get(id=choice_id)
            user = self.request.user
        except (KeyError, Choice.DoesNotExist):
            return HttpResponseRedirect(reverse('pollsdetail', kwargs={'id': 'q.id'}))
        else:
            choice.votes += 1
            choice.save()
            UserVotes.objects.create(user=user, choice=choice, question=q)
                
        return HttpResponseRedirect(reverse('pollsresult', args=(q.id, )))


def profilecreatepoll(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))
        
    form = CreatePollForm()

    if request.method == "POST":

        question_text = request.POST['question_text']
        choice1 = request.POST['choice1']
        choice2 = request.POST['choice2']
        choice3 = request.POST['choice3']
        choice4 = request.POST['choice4']
        choice5 = request.POST['choice5']
        
        question = Question(question_text=question_text, published_by=request.user.username)
        question.save()
        
        Choice.objects.create(question=question, choice_text=choice1)
        Choice.objects.create(question=question, choice_text=choice2)
        if choice3:
            Choice.objects.create(question=question, choice_text=choice3)
        if choice4:
            Choice.objects.create(question=question, choice_text=choice4)
        if choice5:
            Choice.objects.create(question=question, choice_text=choice5)


        messages.success(request, 'Poll created successfully.')
        return HttpResponseRedirect(reverse('profilepolls'))

    return render(request, 'createpoll.html', {'form': form})


def profileupdate(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        form.fields['username'].disabled = True

        if form.is_valid():
            request.user.first_name = form.cleaned_data['fname']
            request.user.last_name = form.cleaned_data['lname']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            request.user.userprofile.anonymous = form.cleaned_data['anonymous']
            request.user.userprofile.save()

            messages.success(request, 'Your Profile has been Updated successfully.')
            return HttpResponseRedirect(reverse('profile'))

    else:
        form = UserUpdateForm(instance=request.user)
        form.fields['username'].disabled = True
        form.fields['username'].help_text = "You can't change your Username once the account is created."
        form.fields['fname'].initial = request.user.first_name
        form.fields['lname'].initial = request.user.last_name
        form.fields['email'].initial = request.user.email
        form.fields['anonymous'].initial = request.user.userprofile.anonymous

    return render(request, 'profile_update.html', {'form': form})


# messages.debug, info, success, warning, error