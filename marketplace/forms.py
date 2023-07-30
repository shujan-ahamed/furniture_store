from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    """Form definition for Review."""

    class Meta:
        """Meta definition for Reviewform."""
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
