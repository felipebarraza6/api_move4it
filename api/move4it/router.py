from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.move4it.views import blogs as views_blogs, enterprises as views_enterprises, activities as views_activities 

router = DefaultRouter()

router.register(r'blogs', views_blogs.BlogViewSet, basename='blogs')
router.register(r'enterprises', views_enterprises.EnterpriseViewSet, basename='enterprises')
router.register(r'competences', views_enterprises.CompetenceViewSet, basename='competences')
router.register(r'activities', views_activities.ActivityViewSet, basename='activities')

urlpatterns = [
    path('', include(router.urls))
]
