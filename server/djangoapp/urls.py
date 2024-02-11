from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout
    
    path(route='', view=views.get_dealerships, name='index'),
    path('about/', view=views.about, name='about'),
    path('contact/', view=views.contact, name='contact'),
    path('login/', view=views.login_request, name='login'),
    path('logout/', view=views.logout_request, name='logout'),
    path('registration/', view=views.registration_request, name='registration'),
    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path('add_dealer_review/<int:dealer_id>/', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)