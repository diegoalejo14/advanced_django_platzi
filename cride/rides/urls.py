#from django.urls.resolvers import URLPattern


"""Circles URLS."""

# from django.urls import path
# #Views
# from cride.circles.views import list_circles,create_circle

# urlpatterns=[
#   path('circles/',list_circles),
#   path('circles/create',create_circle)
# ]


from rest_framework.routers import DefaultRouter

from django.urls import include, path

# Views
from .views import rides as ride_views

router = DefaultRouter()
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/rides',
                ride_views.RidesViewSet,
                basename='ride'
                )


urlpatterns = [
    path('', include(router.urls))
]
