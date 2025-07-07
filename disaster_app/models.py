from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
class Profile(models.Model):
    ROLE_CHOICES = [
        ('Victim', 'Victim'),
        ('Volunteer', 'Volunteer'),
        ('Organization', 'Organization')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to default User model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username



class FoodRequest(models.Model):
    FOOD_CHOICES = [
        ('cooked', 'Cooked Food'),
        ('dry', 'Dry Rations'),
        ('baby', 'Baby Food'),
    ]

    user = models.ForeignKey (User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    location = models.TextField()
    people_count = models.IntegerField(default=1)  # Sets a default of 1
    food_type = models.CharField(max_length=10, choices=FOOD_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto store the request time

    def __str__(self):
        return f"{self.full_name} - {self.food_type} ({self.created_at})"


class FoodOffer(models.Model):
    provider_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    food_type = models.CharField(max_length=50, choices=[('cooked', 'Cooked Food'), ('dry', 'Dry Rations'), ('baby', 'Baby Food')])
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(null=True, blank=True)  # Expiry date for cooked food
    image = models.ImageField(upload_to="food_images/", null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider_name} - {self.food_type} ({self.quantity})"


class DisasterReport(models.Model):
    DISASTER_TYPES = [
        ("Flood", "Flood"),
        ("Earthquake", "Earthquake"),
        ("Fire", "Fire"),
        ("Tornado", "Tornado"),
        ("Other", "Other"),
    ]
    disaster_type = models.CharField (max_length=50, choices=DISASTER_TYPES)
    location = models.CharField(max_length=255)
    description = models.TextField()
    contact = models.CharField (max_length=100)
    image = models.ImageField(upload_to='disaster_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField (default=now)  # Auto-set timestamp

    def is_active(self):
        """Check if the disaster occurred within the last 24 hours."""
        from datetime import timedelta
        return now() - self.timestamp <= timedelta (hours=24)

    def __str__(self):
        return f"{self.disaster_type} at {self.location} - {'Active' if self.is_active() else 'Past'}"

class Volunteer(models.Model):
    ROLE_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('victim', 'Victim'),
        ('organization', 'Organization'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    availability = models.DateTimeField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"


class FinancialAidRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Victim requesting aid
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    reason = models.TextField()
    amount_needed = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=[
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('PayPal', 'PayPal'),
        ('Other', 'Other'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount_needed} requested"

class FinancialDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    aid_request = models.ForeignKey(FinancialAidRequest, on_delete=models.CASCADE)
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('PayPal', 'PayPal'),
        ('Other', 'Other'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount_donated} for {self.aid_request.name}"


class ShelterRequest(models.Model):
    full_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    num_people = models.IntegerField()
    current_location = models.CharField(max_length=255)
    shelter_location = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.shelter_location}"

class ShelterOffer(models.Model):
    full_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    shelter_address = models.CharField(max_length=255)
    capacity = models.IntegerField()
    shelter_type = models.CharField(max_length=100)
    sleeping_arrangements = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.shelter_address}"

class MedicalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    issue_type = models.CharField(max_length=50, choices=[
        ('injury', 'Injury'),
        ('illness', 'Illness'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ])
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.issue_type} ({self.status})"


class Feedback(models.Model):
    rating = models.IntegerField()  # Storing rating from 1 to 5
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating} - {self.description[:20]}"
