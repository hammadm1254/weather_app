## for redirection and rendering
from django.shortcuts import render, get_object_or_404, redirect

## for user authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

## for errror page handling
from django.core.exceptions import PermissionDenied
from django.http import Http404

# for getting current time
from django.utils import timezone

## my own functions in modules directory
from modules import getWeather, locationInfo

## The forms and models
from django.contrib.auth.forms import UserCreationForm
from .forms import SearchForm, UserLoginForm
from .models import Search

"""
def getGeoLocation():
    geoLoc = GeoIP()
    return geoLoc.city(request.META['REMOTE_ADDR'])
"""

"""
Not needed because email verification not implemented 
def get_verificationURL(the_request):
    print("request.get_host():", request.get_host())
"""

def get_redirectURL(the_request):
    redirect_url = the_request.get_full_path().split('/?next=')
    return str(redirect_url[-1])

@login_required
def search_list(request):
    """
    Don't need this because of the @login_required decorator


    if request.user.is_authenticated() == False:
        raise PermissionDenied
    else:
        searches = Search.objects.filter(user=request.user).order_by('search_date')
        return render(request, 'skycast_app/search_list.html', {'searches' : searches})
    """
    searches = Search.objects.filter(user=request.user).order_by('search_date')
    return render(request, 'skycast_app/search_list.html', {'searches': searches})

def login_view(request):
    if request.user.is_authenticated():
        return redirect('search_list') ## Was 'search list' before. will later redirect to user detail page
        #return redirect('search_list')
    else:
        if request.method == "POST":
            loginForm = UserLoginForm(request.POST)
            if loginForm.is_valid():
                ### Add .get after formfields below
                authenticated_user = authenticate(request, username=loginForm.cleaned_data.get('username'), password=loginForm.cleaned_data.get('password'))
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    redirect_url = get_redirectURL(request)
                    #print("Login Successful\nURL requested:", request.get_host())
                    return redirect(redirect_url) ##Was 'search_list' before Don't redirect necessarily go to requested page
                else:
                    return render(request, 'skycast_app/login_page.html', {'form': loginForm, 'error_message': 'Incorrect Username or Password'})
        else:
            loginForm = UserLoginForm()
        return render(request, 'skycast_app/login_page.html', {'form': loginForm})
"""
def create_account_view(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username').lower()
            raw_password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('search_list')
            #if user is not None:
            #    signup_form.save()
            #    login(request, user)
            #    return redirect('search_list')
    else:
        signup_form = UserCreationForm()
    return render(request, 'skycast_app/create_account.html', {'form' : signup_form})
"""

def create_account_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("User typed:", form.cleaned_data.get('username'))
            form.save()
            print("User Saved:", form.cleaned_data.get('username'))
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print("User to be Authenticated:", username)
            user = authenticate(username=username, password=raw_password)
            print("Authenticated User", user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'skycast_app/create_account.html', {'form': form})



@login_required
def logout_view(request):
    """
    with the use of the @login_required decorator this function
    only executes if user is logged in. Otherwise redirects to
    login page. Previous code logged out and redirected to home
    page in both cases.


    if request.user.is_authenticated():
        ## call logoiut function then redirect to homepage
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
    """
    logout(request)
    return redirect('home')

def home(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            print("Time request is made:", timezone.now())
            currentLocation = locationInfo.Location(form.cleaned_data.get('location_Search')) #Put cleaned data here
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
                    return render(request, 'skycast_app/location_detail.html',{'location': userInput, 'weather': weatherData})
            else:
                return render(request, 'skycast_app/home.html', {'form': form, 'error': 'Location Not Found!'})
    else:
        form = SearchForm()
    return render(request, 'skycast_app/home.html', {'form' : form, 'error' : None})


@login_required
def location_detail(request, pk):
    location_clicked = get_object_or_404(Search, pk=pk)
    print("user making request:", request.user)
    if request.user == location_clicked.user:
        coordinates = {'lat': location_clicked.latitude, 'lng': location_clicked.longitude}
        weatherData = getWeather.getForecast(coordinates)
        #### Should update DB again with new search add two seconds to prevent update of DB repeatedly in quick succession
        print("Time data is ready to display:", timezone.now())
        if location_clicked.search_date < timezone.now() - timezone.timedelta(seconds=2): ## and if weather data is not none. Add timer or weather and location
            print("User who searched:", request.user, "\nSearch is delayed enough to update DB")
            try:
                updateDB = Search.objects.create(user=request.user,latitude=location_clicked.latitude, longitude=location_clicked.longitude, location_Search=location_clicked.location_Search, search_date=timezone.now())
                return render(request, 'skycast_app/location_detail.html',
                              {'location': updateDB, 'weather': weatherData})
            except:
                return render(request, 'skycast_app/error_page.html', {"message": 'DB Update Failed'})
        else:
            print("User who searched:", request.user, "\nSearching too fast, not updating DB")
            #return render(request, 'skycast_app/error_page.html', {'message': 'please try your search in a few seconds'})
            return render(request, 'skycast_app/location_detail.html',
                          {'location':location_clicked, 'weather': weatherData})
    else:
        return render(request, 'skycast_app/error_page.html', {"message": 'HTTP 404'})