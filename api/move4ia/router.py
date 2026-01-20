from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.move4ia.views import blogs as views_blogs, enterprises as views_enterprises, activities as views_activities, registers_activity as views_registers_activity

router = DefaultRouter()

router.register(r'blogs', views_blogs.BlogViewSet, basename='blogs')
router.register(
    r'enterprises', views_enterprises.EnterpriseViewSet, basename='enterprises')
router.register(
    r'competences', views_enterprises.CompetenceViewSet, basename='competences')
router.register(r'activities', views_activities.ActivityViewSet,
                basename='activities')
router.register(r'register-activities',
                views_registers_activity.RegisterActivityViewSet, basename='register-activities')

urlpatterns = [
    path('', include(router.urls))
]
