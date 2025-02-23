from django import forms
from .models import Comment, Vote, Product



# Product form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'estimated_cost', 'estimated_profit', 'estimated_time']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter product name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter product description'})
        self.fields['estimated_cost'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter estimated cost'})
        self.fields['estimated_profit'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter estimated profit'})
        self.fields['estimated_time'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter estimated time'})




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        
        
        
# Vote form
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['is_approved']

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['is_approved'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Vote approval'})





