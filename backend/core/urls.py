from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="service")
router.register("projects", ProjectViewSet, basename="project")
router.register("technologies", TechnologyViewSet, basename="technology")
router.register("clients", ClientViewSet, basename="client")
router.register("hero-slides", HeroSlideViewSet, basename="hero-slide")
router.register("team", TeamMemberViewSet, basename="team-member")
router.register("testimonials", TestimonialViewSet, basename="testimonial")
router.register("pages", PageViewSet, basename="page")

urlpatterns = [
    path("", include(router.urls)),
    path("bootstrap/", WebsiteBootstrapView.as_view(), name="bootstrap"),
    path("site-settings/", SiteSettingsListView.as_view(), name="site-settings"),
    path("navigation/", NavigationListView.as_view(), name="navigation"),
    path("hero/", HeroListView.as_view(), name="hero"),
    path("about/", AboutListView.as_view(), name="about"),
    path("statistics/", StatisticsListView.as_view(), name="statistics"),
    path("ctas/", CTAListView.as_view(), name="ctas"),
    path("footer-links/", FooterLinkListView.as_view(), name="footer-links"),
    path("social-links/", SocialLinkListView.as_view(), name="social-links"),
    path("contact/", ContactInquiryCreateView.as_view(), name="contact"),
]
