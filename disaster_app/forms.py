from django import forms
from .models import FoodRequest
from .models import FoodOffer
from .models import DisasterReport
from .models import Volunteer
from .models import ShelterRequest, ShelterOffer
from .models import MedicalRequest
class FoodRequestForm(forms.ModelForm):
    class Meta:
        model = FoodRequest
        fields = ['full_name', 'contact', 'location', 'people_count', 'food_type', 'notes']


class FoodOfferForm(forms.ModelForm):
    class Meta:
        model = FoodOffer
        fields = ["provider_name", "contact", "location", "food_type", "quantity", "expiry_date", "image", "notes"]
        expiry_date = forms.DateField (required=False)
        food_image = forms.ImageField (required=False)
        notes = forms.CharField (widget=forms.Textarea, required=False)


class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = DisasterReport
        fields = [ 'disaster_type','location', 'description', 'contact','image' ]


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'location', 'role', 'availability', 'skills']
        widgets = {
            'availability': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



class ShelterRequestForm(forms.ModelForm):
    class Meta:
        model = ShelterRequest
        fields = ['full_name', 'contact', 'email', 'num_people', 'current_location', 'shelter_location', 'additional_info']

class ShelterOfferForm(forms.ModelForm):
    class Meta:
        model = ShelterOffer
        fields = ['full_name', 'contact', 'email', 'shelter_address', 'capacity', 'shelter_type', 'sleeping_arrangements']



class MedicalRequestForm(forms.ModelForm):
    class Meta:
        model = MedicalRequest
        fields = ["name", "contact", "location", "issue_type", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter full name"}),
            "contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter contact number"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your location"}),
            "issue_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Describe the issue"}),
        }