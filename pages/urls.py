from django.urls import path
from .views import Detect, HomePageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("detect/", Detect.as_view(), name="detect"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)