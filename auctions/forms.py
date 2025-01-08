from django import forms
from django.forms import ModelForm
from .models import Listing, Bid, Comment, CATEGORY_CHOICES

class ListingForm(ModelForm):
    # By defining category as a form.ChoiceField we create the
    # HTML select element	
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_bid', 'image', 'category']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount'] 
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields=['comment']
        widgets = {'comment': forms.Textarea(attrs={'rows': 5, 'cols': 40}),}