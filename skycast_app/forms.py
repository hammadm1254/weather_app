from django import forms

from .models import Search


# Need this User object to convert fields to lowercase then pass to user object
# Ended up not using the class requiring these
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class SearchForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('location_Search',)


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, min_length=1)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


"""
class UserSignupForm(UserCreationForm):
    Not using this class because of conflict with dealing
    with UserObjects
    
    Using this class mainly to override the save function
    in the parent UserCreationForm class to convert typed
    username to lowercase before saving form. This was all
    usernames are saved as lowercase. The login page also
    converts all username input to lowercase.
    
    def save(self, *args, **kwargs):
        #data = self.data.copy()
        print("Typed Username:", self.data.get('username'))
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        print("save override:", self.cleaned_data['username'])
        #print(data['username'])
        #self.data = data.copy()
        #self.fields['username'] = self.['username'].lower()
        return super(UserSignupForm, self).save(*args, **kwargs)

"""