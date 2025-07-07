from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Volunteer

from .models import FinancialAidRequest, FinancialDonation
admin.site.register(Volunteer)



admin.site.register(FinancialAidRequest)
admin.site.register(FinancialDonation)
