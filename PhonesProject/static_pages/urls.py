from django.urls import path, re_path
from .views import contacts_page, support_page, about_page

app_name = 'static_pages'

urlpatterns = [
    re_path(r'contacts', contacts_page, name="contacts"),
    re_path(r'support', support_page, name="support"),
    re_path(r'about', about_page, name="about"),
]
