from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from dashboards.models import Notification
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Comment
from .forms import ProductForm, CommentForm, VoteForm
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required


# List of products
@method_decorator(never_cache, name='dispatch')
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    
  

# Add a new product 
@method_decorator(never_cache, name='dispatch')   
class AddProductView(LoginRequiredMixin ,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('product_list')  # Redirect to the product list after successful creation

    def form_valid(self, form):
        # Automatically set the current user as the product owner
        form.instance.user = self.request.user

        # Save the form data
        response = super().form_valid(form)

        # Create a notification for all users about the new product
        users = User.objects.exclude(id=self.request.user.id)  # Exclude the current user (product creator)
        for user in users:
            Notification.objects.create(
                user=user,
                product=form.instance,
                message=f"New product added: {form.instance.name}",
            )

        # Add success message for the notification
        messages.success(self.request, 'Product added and notifications sent to customers!')

        return response
  
  
  
  
# Product details   
@method_decorator(never_cache, name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Add the comment form and vote form to the context
        context['comment_form'] = CommentForm()
        context['vote_form'] = VoteForm()

        # Optimize fetching comments and votes
        context['comments'] = product.comments.select_related('user')
        context['votes'] = product.votes.select_related('user')
        
        # Optimize counting comments
        context['comment_count'] = product.comments.aggregate(count=Count('id'))['count']

        # Optimize counting votes
        context['vote_count'] = product.votes.aggregate(count=Count('id'))['count']
        
        # Optimize checking if user has voted
        context['has_voted'] = product.votes.filter(user=self.request.user).exists()

        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()

        # Handle the comment form submission
        if 'comment_text' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.user = request.user  # Assign the actual User object
                comment.save()

                # Create a notification for the product owner
                if product.user != request.user:
                    Notification.objects.create(
                        user=product.user,
                        product=product,
                        message=f"{request.user.username} commented on your product: {product.name}"
                    )
            return redirect('product_details', pk=product.pk)


        # Handle the vote form submission
        if request.method == 'POST':
            # تحقق من أن المستخدم قد حدد الـ checkbox
            if not request.POST.get('is_approved'):
                messages.error(request, 'Please select the vote option.')
                return redirect('product_details', pk=product.pk)

            # Check if the user has already voted
            if product.votes.filter(user=request.user).exists():
                return redirect('product_details', pk=product.pk)

            vote_form = VoteForm(request.POST)
            if vote_form.is_valid():
                vote = vote_form.save(commit=False)
                vote.product = product
                vote.user = request.user  # Assign the actual User object
                vote.save()

                # Create a notification for the product owner
                if product.user != request.user:
                    Notification.objects.create(
                        user=product.user,
                        product=product,
                        message=f"{request.user.username} voted on your product: {product.name}"
                    )
            else:
                # Log the errors if the form is invalid
                messages.error(request, 'There was an error with your vote.')
                print(vote_form.errors)

            return redirect('product_details', pk=product.pk)



@method_decorator(never_cache, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('product_list')  # Redirect to the product list after successful update



@method_decorator(never_cache, name='dispatch')
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_list')
    
    
@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Ensure the user is the comment owner
    if comment.user != request.user:
        return redirect('product_details', pk=comment.product.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('product_details', pk=comment.product.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'product_details.html', {'comment_form': form, 'comment': comment})
