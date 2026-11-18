import hashlib
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers
from .models import *

class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta: model = ServiceFeature; fields = ("id", "title", "description", "display_order")

class TechnologySerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()
    class Meta: model = Technology; fields = ("id", "name", "slug", "category", "description", "icon_url", "display_order")
    def get_icon_url(self, obj): return self._url(obj.icon)
    def _url(self, value):
        if not value: return None
        request = self.context.get("request")
        return request.build_absolute_uri(value.url) if request else value.url

class ServiceSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta: model = Service; fields = ("id", "title", "slug", "short_description", "description", "outcome", "icon_name", "image_url", "is_featured", "features", "seo_title", "seo_description", "display_order")
    def get_image_url(self, obj):
        if not obj.image: return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta: model = ProjectCategory; fields = ("id", "name", "slug")

class ProjectFeatureSerializer(serializers.ModelSerializer):
    class Meta: model = ProjectFeature; fields = ("id", "title", "description", "display_order")

class ProjectMediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    class Meta: model = ProjectMedia; fields = ("id", "media_type", "file_url", "external_url", "caption", "alt_text", "display_order")
    def get_file_url(self, obj):
        if not obj.file: return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url

class ProjectSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer(read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)
    features = ProjectFeatureSerializer(many=True, read_only=True)
    media = ProjectMediaSerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    class Meta: model = Project; fields = ("id", "title", "slug", "subtitle", "category", "overview", "problem", "solution", "result", "thumbnail_url", "demo_video_url", "project_url", "github_url", "technologies", "features", "media", "is_featured", "published_at", "seo_title", "seo_description", "display_order")
    def get_thumbnail_url(self, obj):
        if not obj.thumbnail: return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.thumbnail.url) if request else obj.thumbnail.url

class NavigationItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta: model = NavigationItem; fields = ("id", "label", "url", "open_in_new_tab", "is_cta", "display_order", "children")
    def get_children(self, obj): return NavigationItemSerializer(obj.children.filter(is_active=True), many=True, context=self.context).data

class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField(); favicon_url = serializers.SerializerMethodField()
    class Meta: model = SiteSettings; fields = "__all__"
    def _url(self, value):
        if not value: return None
        request = self.context.get("request")
        return request.build_absolute_uri(value.url) if request else value.url
    def get_logo_url(self, obj): return self._url(obj.logo)
    def get_favicon_url(self, obj): return self._url(obj.favicon)

class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta: model = HeroSection; fields = "__all__"
class HeroSlideSerializer(serializers.ModelSerializer):
    video_file_url = serializers.SerializerMethodField()
    poster_image_url = serializers.SerializerMethodField()
    class Meta:
        model = HeroSlide
        fields = ("id", "eyebrow", "heading", "description", "video_file_url", "video_url", "poster_image_url", "primary_button_text", "primary_button_url", "secondary_button_text", "secondary_button_url", "duration_seconds", "overlay_strength", "display_order")
    def _url(self, value):
        if not value: return None
        request = self.context.get("request")
        return request.build_absolute_uri(value.url) if request else value.url
    def get_video_file_url(self, obj): return self._url(obj.video_file)
    def get_poster_image_url(self, obj): return self._url(obj.poster_image)
class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta: model = AboutSection; fields = "__all__"
class StatisticSerializer(serializers.ModelSerializer):
    class Meta: model = Statistic; fields = ("id", "label", "value", "suffix", "display_order")
class ClientSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    class Meta: model = Client; fields = ("id", "company_name", "logo_url", "website", "description", "display_order")
    def get_logo_url(self, obj):
        if not obj.logo: return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
class TeamMemberSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = TeamMember
        fields = ("id", "name", "designation", "description", "email", "linkedin_url", "image_url", "display_order")
    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url
class TestimonialSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    company_logo_url = serializers.SerializerMethodField()
    class Meta:
        model = Testimonial
        fields = ("id", "customer_name", "company", "job_title", "review", "rating", "review_date", "is_featured", "display_order", "profile_image_url", "company_logo_url")
    def _url(self, value):
        if not value: return None
        request = self.context.get("request")
        return request.build_absolute_uri(value.url) if request else value.url
    def get_profile_image_url(self, obj): return self._url(obj.profile_image)
    def get_company_logo_url(self, obj): return self._url(obj.company_logo)
class CTASectionSerializer(serializers.ModelSerializer):
    class Meta: model = CTASection; exclude = ("is_active", "created_at", "updated_at")
class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta: model = FooterLink; fields = ("id", "group", "label", "url", "display_order")
class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta: model = SocialLink; fields = ("id", "platform", "url", "icon_name", "display_order")
class PageSerializer(serializers.ModelSerializer):
    class Meta: model = Page; exclude = ("is_active", "created_at", "updated_at")

class ContactInquirySerializer(serializers.ModelSerializer):
    website = serializers.CharField(write_only=True, required=False, allow_blank=True)
    class Meta:
        model = ContactInquiry
        fields = ("id", "name", "email", "phone", "company", "service", "budget_range", "project_description", "preferred_contact_method", "website", "created_at")
        read_only_fields = ("id", "created_at")
    def validate_website(self, value):
        if value: raise serializers.ValidationError("Invalid submission.")
        return value
    def validate_project_description(self, value):
        value = " ".join(value.split())
        if len(value) < 20: raise serializers.ValidationError("Please provide at least 20 characters.")
        return value
    def create(self, validated_data):
        validated_data.pop("website", None)
        request = self.context.get("request")
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR", "")
        validated_data["source_ip_hash"] = hashlib.sha256(ip.encode()).hexdigest() if ip else ""
        inquiry = super().create(validated_data)
        if settings.CONTACT_NOTIFICATION_EMAIL:
            send_mail("New agency website inquiry", f"{inquiry.name} ({inquiry.email})\n\n{inquiry.project_description}", settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_NOTIFICATION_EMAIL], fail_silently=True)
        return inquiry
