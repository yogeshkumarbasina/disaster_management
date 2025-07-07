from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import FoodRequest
from .forms import FoodRequestForm
from django.contrib.auth.decorators import login_required
from .models import FoodOffer
from .forms import FoodOfferForm
from .forms import DisasterReportForm
from .models import DisasterReport
from django.utils.timezone import now
from datetime import timedelta
from .models import Volunteer
from .forms import VolunteerForm
from disaster_app.models import FinancialAidRequest
from django.shortcuts import render, get_object_or_404
from .models import ShelterRequest, ShelterOffer
from .forms import ShelterRequestForm, ShelterOfferForm
from .models import MedicalRequest
from .forms import MedicalRequestForm
from django.http import JsonResponse, HttpResponse
from .models import Feedback
from django.views.decorators.csrf import csrf_exempt


def home(request):
    disaster_reported = DisasterReport.objects.exists()  # Check if any disaster is reported
    return render(request, 'home.html', {'disaster_reported': disaster_reported})

@login_required
def disaster_reports(request):
    all_reports = DisasterReport.objects.all ().order_by ('-timestamp')

    active_disasters = [report for report in all_reports if report.is_active ()]
    past_disasters = [report for report in all_reports if not report.is_active ()]

    context = {
        'active_disasters': active_disasters,
        'past_disasters': past_disasters,
        'has_active_disasters': bool (active_disasters),  # Flag for blinking button
    }
    return render (request, 'disaster_reports.html', context)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logges out.')
    return redirect('home')
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                messages.success(request, "Account created successfully! please login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'signup.html')

def submit_feedback(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        description = request.POST.get("description")
        if not rating:
            return render (request, "feedback.html", {"error": "Please select a rating."})

            # Save feedback
        Feedback.objects.create (rating=int (rating), description=description)

        return redirect("thank_you")
    return render(request,"feedback.html")

def thank_you(request):
    return render(request, 'thank_you.html')
def aboutus(request):
    return render(request, 'aboutus.html')

@login_required
def volunteer(request):
    if request.method == "POST":
        form = VolunteerForm (request.POST)
        if form.is_valid ():
            form.save ()
            messages.success (request, "Thank you for joining as a volunteer!")
            return redirect ('volunteer')  # Redirect after successful submission

    else:
        form = VolunteerForm ()

    volunteers = Volunteer.objects.all ().order_by ('-created_at')  # Fetch all volunteers

    return render (request, 'volunteeer.html', {'form': form, 'volunteers': volunteers})

@login_required
def food(request):
    return render(request, 'food.html')

def success_page(request):
    return render(request, "success.html")

def disasterreport(request):
    if request.method == "POST":
        form = DisasterReportForm (request.POST, request.FILES)  # Handle form submission
        if form.is_valid ():
            form.save ()
            return redirect("success")  # Redirect to the same page after submission

    else:
        form = DisasterReportForm ()

    return render (request, "disasterreport.html", {"form": form})

@login_required
def viewfood(request):
    food_requests = FoodRequest.objects.all ()  # Fetch all requests
    food_offers = FoodOffer.objects.all()  # Fetch all offers

    return render (request, "viewfood.html", {"food_requests": food_requests, "food_offers": food_offers})


@login_required
def offerfood(request):
    if request.method == "POST":
        provider_name = request.POST.get('provider_name')
        contact = request.POST.get('contact')
        location = request.POST.get('location')
        food_type = request.POST.get('food_type')
        quantity = request.POST.get('quantity')
        expiry_date = request.POST.get('expiry_date')
        notes = request.POST.get('notes')
        image = request.FILES.get('image')

        FoodOffer.objects.create(
            provider_name=provider_name,
            contact=contact,
            location=location,
            food_type=food_type,
            quantity=quantity,
            expiry_date=expiry_date,
            notes=notes,
            image=image
        )
        return redirect('viewfood')  # Redirect to view page

    return render(request, 'offerfood.html')

@login_required
# Ensures only logged-in users can request food
def request_food(request):
    if request.method == "POST":
        form = FoodRequestForm (request.POST)
        if form.is_valid ():
            food_request = form.save (commit=False)  # Save but don’t commit to DB yet
            food_request.user = request.user  # Assign logged-in user
            food_request.save ()  # Now save to DB
            return redirect ('success')  # Redirect to success page
    else:
        form = FoodRequestForm ()

    return render (request, "requestfood.html", {'form': form})

@login_required
def financial(request):
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        reason = request.POST.get('reason')
        amount_needed = request.POST.get('amount_needed')
        payment_mode = request.POST.get('payment_mode')

        FinancialAidRequest.objects.create(
            user=request.user,
            name=name,
            location=location,
            reason=reason,
            amount_needed=amount_needed,
            payment_mode=payment_mode
        )

        return redirect('financial_requests')  # Redirect to all requests

    return render(request, 'financial.html')
def financial_requests(request):
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        reason = request.POST.get('reason')
        amount_needed = request.POST.get('amount_needed')
        payment_mode = request.POST.get('payment_mode')

        # Check if the user already has an existing request with the same details
        existing_request = FinancialAidRequest.objects.filter(
            user=request.user, name=name, location=location, reason=reason, amount_needed=amount_needed, payment_mode=payment_mode
        ).exists()

        if not existing_request:
            FinancialAidRequest.objects.create(
                user=request.user,
                name=name,
                location=location,
                reason=reason,
                amount_needed=amount_needed,
                payment_mode=payment_mode
            )

        return redirect('financial_requests')  # Redirect to the requests page

    requests_list = FinancialAidRequest.objects.all()
    return render(request, 'financial_requests.html', {'requests': requests_list})
def relief_fund(request):
    return render(request, 'relief_fund.html')
@login_required
def donate_money(request, request_id):
    aid_request = get_object_or_404(FinancialAidRequest, id=request_id)
    if request.method == "POST":
        # Handle donation process (example: mark as donated)
        aid_request.delete ()
        return redirect ('financial_requests')

    return render (request, 'donate.html', {'aid_request': aid_request})


@login_required
def delete_financial_request(request, request_id):
    request_obj = get_object_or_404(FinancialAidRequest, id=request_id, user=request.user)
    request_obj.delete()
    return redirect('financial_requests')

def shelter(request):
    return render(request, 'shelter.html')
def request_shelter(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        num_people = request.POST.get ("num_people")
        current_location = request.POST.get("current_location")
        shelter_location = request.POST.get("shelter_location")
        additional_info = request.POST.get("additional_info")

        try:
            num_people = int (num_people) if num_people else 0  # Default to 0 if empty
        except ValueError:
            num_people = 0  # If invalid input, set to 0

        print (
            f"Received Shelter Request: {full_name}, {contact}, {email}, {num_people}, {current_location}, {shelter_location}, {additional_info}")
        # Save to database
        ShelterRequest.objects.create(
            full_name=full_name,
            contact=contact,
            email=email,
            num_people=num_people,
            current_location=current_location,
            shelter_location=shelter_location,
            additional_info=additional_info,
        )

        messages.success(request, "✅ Shelter request submitted successfully!")
        return redirect('view_requests')  # Redirect to shelter request list

    return render(request, "request_shelter.html")

@login_required
def offer_shelter(request):
    if request.method == "POST":
        form = ShelterOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Shelter offer submitted successfully!")
            return redirect('view_requests')
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = ShelterOfferForm()

    return render(request, "offer_shelter.html", {"form": form})

@login_required
def view_requests(request):
    shelter_requests = ShelterRequest.objects.all().order_by("-created_at")  # Show latest requests first
    shelter_offers = ShelterOffer.objects.all ().order_by ("-created_at")  # Latest first
    return render(request, "view_requests.html", {"shelter_requests": shelter_requests,"shelter_offers": shelter_offers })

def submit_medical_request(request):
    if request.method == "POST":
        form = MedicalRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("medical_request_success")  # Ensure this matches the URL name
    else:
        form = MedicalRequestForm()

    return render(request, "medical_request.html", {"form": form})



def medical_request_success(request):
    return render(request, "medical_request_success.html")


def doctors_dashboard(request):
    # Fetch pending and resolved requests separately
    pending_requests = MedicalRequest.objects.filter(status="pending")
    resolved_requests = MedicalRequest.objects.filter(status="resolved")

    return render(request, "doctors_dashboard.html", {
        "pending_requests": pending_requests,
        "resolved_requests": resolved_requests
    })
def mark_as_resolved(request, request_id):
    medical_request = get_object_or_404(MedicalRequest, id=request_id)
    medical_request.status = "resolved"
    medical_request.save()
    return redirect("doctors_dashboard")
def medical_assistance(request):
    return render(request, 'medical_assistance.html')