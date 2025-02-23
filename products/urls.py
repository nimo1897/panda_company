from django.urls import path
from .views import *



urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('update-product/<int:pk>/', PostUpdateView.as_view(), name='update_product'),
    path('delete-product/<int:pk>/', PostDeleteView.as_view(), name='delete_product'),
    path('comment/update/<int:pk>/', comment_update, name='comment_update'),
    # path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]