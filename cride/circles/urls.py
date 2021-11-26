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
from .views import circles as circle_views
from .views import memberships as memberships_views

router = DefaultRouter()
router.register('circles', circle_views.CircleViewSet, basename='circle')
router.register(r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
                memberships_views.MembershipViewSet,
                basename='membership'

                )


urlpatterns = [
    path('', include(router.urls))
]
