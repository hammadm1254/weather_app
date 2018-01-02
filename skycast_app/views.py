## for redirection and rendering
from django.shortcuts import render, get_object_or_404, redirect

## for user authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# for getting current time
from django.utils import timezone

## my own functions in modules directory
from modules import getWeather, locationInfo

## The forms and models
from django.contrib.auth.forms import UserCreationForm
from .forms import SearchForm, UserLoginForm
from .models import Search


def get_redirectURL(the_request):
    redirect_url = the_request.get_full_path().split('/?next=')
    return str(redirect_url[-1])

@login_required
def search_list(request):
    searches = Search.objects.filter(user=request.user).order_by('search_date').reverse()
    return render(request, 'skycast_app/search_list.html', {'searches': searches})

def login_view(request):
    if request.user.is_authenticated():
        return redirect('search_list') ## Was 'search list' before. will later redirect to user detail page
        #return redirect('search_list')
    else:
        if request.method == "POST":
            loginForm = UserLoginForm(request.POST)
            if loginForm.is_valid():
                authenticated_user = authenticate(request, username=loginForm.cleaned_data.get('username'), password=loginForm.cleaned_data.get('password'))
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    redirect_url = get_redirectURL(request)
                    return redirect(redirect_url)
                else:
                    return render(request, 'skycast_app/login_page.html', {'form': loginForm, 'error_message': 'Incorrect Username or Password'})
        else:
            loginForm = UserLoginForm()
        return render(request, 'skycast_app/login_page.html', {'form': loginForm})

def create_account_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'skycast_app/create_account.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            currentLocation = locationInfo.Location(form.cleaned_data.get('location_Search'))
            if currentLocation.coordinates:
                userInput = form.save(commit=False)
                userInput.latitude = currentLocation.coordinates['lat']
                userInput.longitude = currentLocation.coordinates['lng']
                userInput.search_date = timezone.now()
                userInput.location_Search = currentLocation.address
                if request.user.is_authenticated() and not request.user.is_anonymous(): # anonymous user is redundant
                    userInput.user = request.user
                    userInput.save()
                    return redirect('location_detail', pk = userInput.pk)
                else:
                    #### Turn this into redirect to location detail by passing location object as pk
                    weatherData = getWeather.getForecast(currentLocation.coordinates)
                    return render(request, 'skycast_app/location_detail.html', {'location': userInput, 'weather': weatherData,})
            else:
                return render(request, 'skycast_app/home.html', {'form': form, 'error': 'Location Not Found!'})
    else:
        form = SearchForm()
    return render(request, 'skycast_app/home.html', {'form' : form, 'error' : None})


@login_required
def location_detail(request, pk):
    location_clicked = get_object_or_404(Search, pk=pk)
    if request.user == location_clicked.user:
        coordinates = {'lat': location_clicked.latitude, 'lng': location_clicked.longitude}
        weatherData = getWeather.getForecast(coordinates)
        #### Should update DB again with new search add two seconds to prevent update of DB repeatedly in quick succession
        if location_clicked.search_date < timezone.now() - timezone.timedelta(seconds=2): ## and if weather data is not none. Add timer or weather and location
            try:
                updateDB = Search.objects.create(user=request.user,latitude=location_clicked.latitude, longitude=location_clicked.longitude, location_Search=location_clicked.location_Search, search_date=timezone.now())
                return render(request, 'skycast_app/location_detail.html',
                              {'location': updateDB, 'weather': weatherData})
            except:
                return render(request, 'skycast_app/error_page.html', {"message": 'DB Update Failed'})
        else:
            return render(request, 'skycast_app/location_detail.html', {'location': location_clicked, 'weather': weatherData})
    else:
        return render(request, 'skycast_app/error_page.html', {"message": 'HTTP 404'})