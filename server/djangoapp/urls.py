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
                  path('about/', view=views.about_us, name='about_us'),

                  # path for contact us view
                  path('contact/', view=views.contact_us, name='contact_us'),

                  # path for registration
                  path('signup/', view=views.registration_request, name='registration'),

                  # path for login
                  path('login/', view=views.login_request, name='login'),

                  # path for logout
                  path('logout/', view=views.logout_request, name='logout'),

                  # path for dealer reviews view
                  path(route='', view=views.get_dealerships, name='index'),

                  # path for add a review view

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)