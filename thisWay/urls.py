from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import thisWayDesign.views

urlpatterns = [
    path("", thisWayDesign.views.index, name="index"),
    path("db/", thisWayDesign.views.db, name="db"),
    path("admin/", admin.site.urls),
]