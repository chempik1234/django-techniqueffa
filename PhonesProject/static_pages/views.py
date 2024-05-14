from django.conf import settings
from django.shortcuts import render


def contacts_page(request):
    data = settings.DEFAULT_CONTEXT.copy()
    data["title_header"] = "Контакты"
    return render(request, 'static_pages/contacts.html', context=data)


def support_page(request):
    data = settings.DEFAULT_CONTEXT.copy()
    data["title_header"] = "Поддержка и помощь"
    return render(request, "static_pages/support.html", context=data)


def about_page(request):
    data = settings.DEFAULT_CONTEXT.copy()
    data["title_header"] = "О магазине"
    return render(request, "static_pages/about.html", context=data)
