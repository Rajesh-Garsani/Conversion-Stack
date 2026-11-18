from django.db.models import Prefetch
from rest_framework import generics, permissions, response, viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .throttles import ContactRateThrottle

class ActiveReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    def get_queryset(self): return self.queryset.filter(is_active=True)

class ServiceViewSet(ActiveReadOnlyViewSet):
    queryset = Service.objects.prefetch_related(Prefetch("features", queryset=ServiceFeature.objects.filter(is_active=True)))
    serializer_class = ServiceSerializer
    filterset_fields = ("is_featured",)
    search_fields = ("title", "short_description", "description")

class ProjectViewSet(ActiveReadOnlyViewSet):
    queryset = Project.objects.select_related("category").prefetch_related("technologies", Prefetch("features", queryset=ProjectFeature.objects.filter(is_active=True)), Prefetch("media", queryset=ProjectMedia.objects.filter(is_active=True)))
    serializer_class = ProjectSerializer
    filterset_fields = ("is_featured", "category__slug")
    search_fields = ("title", "subtitle", "overview")

class TechnologyViewSet(ActiveReadOnlyViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    filterset_fields = ("category",)
    search_fields = ("name", "description")

class PageViewSet(ActiveReadOnlyViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.filter(is_active=True)
    serializer_class = ClientSerializer
class HeroSlideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HeroSlide.objects.filter(is_active=True)
    serializer_class = HeroSlideSerializer
class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer
    filterset_fields = ("is_featured",)

class NavigationListView(generics.ListAPIView):
    queryset = NavigationItem.objects.filter(is_active=True, parent__isnull=True).prefetch_related("children")
    serializer_class = NavigationItemSerializer
    pagination_class = None
class SiteSettingsListView(generics.ListAPIView):
    queryset = SiteSettings.objects.all()[:1]
    serializer_class = SiteSettingsSerializer
    pagination_class = None
class HeroListView(generics.ListAPIView):
    queryset = HeroSection.objects.filter(is_active=True)[:1]
    serializer_class = HeroSectionSerializer
    pagination_class = None
class AboutListView(generics.ListAPIView):
    queryset = AboutSection.objects.filter(is_active=True)[:1]
    serializer_class = AboutSectionSerializer
    pagination_class = None
class StatisticsListView(generics.ListAPIView):
    queryset = Statistic.objects.filter(is_active=True)
    serializer_class = StatisticSerializer
    pagination_class = None
class CTAListView(generics.ListAPIView):
    queryset = CTASection.objects.filter(is_active=True)
    serializer_class = CTASectionSerializer
    pagination_class = None
class FooterLinkListView(generics.ListAPIView):
    queryset = FooterLink.objects.filter(is_active=True)
    serializer_class = FooterLinkSerializer
    pagination_class = None
class SocialLinkListView(generics.ListAPIView):
    queryset = SocialLink.objects.filter(is_active=True)
    serializer_class = SocialLinkSerializer
    pagination_class = None

class ContactInquiryCreateView(generics.CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    throttle_classes = [ContactRateThrottle]
    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        return response.Response({"success": True, "message": "Your inquiry has been received.", "data": result.data}, status=201)

class WebsiteBootstrapView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        context = {"request": request}
        settings_obj = SiteSettings.objects.first(); hero = HeroSection.objects.filter(is_active=True).first(); about = AboutSection.objects.filter(is_active=True).first()
        services = Service.objects.filter(is_active=True).prefetch_related(Prefetch("features", queryset=ServiceFeature.objects.filter(is_active=True)))
        projects = Project.objects.filter(is_active=True).select_related("category").prefetch_related("technologies", Prefetch("features", queryset=ProjectFeature.objects.filter(is_active=True)), Prefetch("media", queryset=ProjectMedia.objects.filter(is_active=True)))
        return response.Response({"success": True, "data": {
            "settings": SiteSettingsSerializer(settings_obj, context=context).data if settings_obj else None,
            "navigation": NavigationItemSerializer(NavigationItem.objects.filter(is_active=True, parent__isnull=True).prefetch_related("children"), many=True, context=context).data,
            "hero": HeroSectionSerializer(hero, context=context).data if hero else None,
            "hero_slides": HeroSlideSerializer(HeroSlide.objects.filter(is_active=True), many=True, context=context).data,
            "about": AboutSectionSerializer(about, context=context).data if about else None,
            "statistics": StatisticSerializer(Statistic.objects.filter(is_active=True), many=True).data,
            "services": ServiceSerializer(services, many=True, context=context).data,
            "projects": ProjectSerializer(projects, many=True, context=context).data,
            "technologies": TechnologySerializer(Technology.objects.filter(is_active=True), many=True, context=context).data,
            "clients": ClientSerializer(Client.objects.filter(is_active=True), many=True, context=context).data,
            "team": TeamMemberSerializer(TeamMember.objects.filter(is_active=True), many=True, context=context).data,
            "testimonials": TestimonialSerializer(Testimonial.objects.filter(is_active=True), many=True, context=context).data,
            "ctas": CTASectionSerializer(CTASection.objects.filter(is_active=True), many=True).data,
            "footer_links": FooterLinkSerializer(FooterLink.objects.filter(is_active=True), many=True).data,
            "social_links": SocialLinkSerializer(SocialLink.objects.filter(is_active=True), many=True).data,
        }})
