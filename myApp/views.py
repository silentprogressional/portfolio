from django.shortcuts import render
from myApp.models import Users, Contacts
from . import forms
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.


def index(request):
    return render(request, 'myApp/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class userLogin(TemplateView):

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('Someone tried to login and failed')
            print(f'username: {username}')
            return HttpResponse('invalid login credentials')

    def get(self, request, *args, **kwargs):
        return render(request, 'myApp/user_login.html')

@method_decorator(login_required, name='dispatch')
class formView(View):
    form = forms.UserForm

    def post(self, request, *args, **kwargs):
        form = forms.UserForm(request.POST)

        if form.is_valid():
            try:
                cli_addr = request.META.get('REMOTE_ADDR')

                try:
                    record = Users.objects.get(email=form.cleaned_data['email'])
                    record = "This email address already exist"
                    return render(request, 'myApp/errorpage.html', context={'error': record})
                except Users.DoesNotExist:
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.save()
                    return render(request, 'myApp/successpage.html', context={'username': form.cleaned_data['username']})
            except Exception as a:
                return render(request, 'myApp/errorpage.html', context={'error': a})
        else:
            return render(request, 'myApp/errorpage.html', context={'error': form.errors})

    def get(self, request, *args, **kwargs):
        form = self.form
        return render(request, 'myApp/register.html', context={'form': form})


#to disable csrf token
@method_decorator(csrf_exempt, name='dispatch')
class contactView(View):

    def post(self, request, *args, **kwargs):

        contact = Contacts.objects.create(username=request.POST.get('name'), email=request.POST.get('email'),
                                          phoneNumber=request.POST.get('phone'), message=request.POST.get('message'))

        try:
            contact.save()
            return render(request, 'myApp/successpage.html')
        except Exception as A:
            print(A)








