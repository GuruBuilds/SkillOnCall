from django.urls import path
from .views import signup_view, sign_in, sign_out, upload_work_image, delete_work_image

urlpatterns = [
    path('signup/', signup_view, name='signup_view'),
    path('login/', sign_in, name='sign_in'),
    path('logout/', sign_out, name='sign_out'),
    path('edit-profile/', signup_view, name='edit_profile'),
    path('upload-work-image/', upload_work_image, name='upload_work_image'),
    path('delete-work-image/<int:image_id>/', delete_work_image, name='delete_work_image'),
]
