
from django.contrib import admin
from django.urls import path, include
from .views import home, send_daily_reminders
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path('', home, name="home"),

    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path('admin/', admin.site.urls),
    path("tasks/send-daily-reminders/",
         send_daily_reminders, name="send_daily_reminders"),
)

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
