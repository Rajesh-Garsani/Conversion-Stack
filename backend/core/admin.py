from django.contrib import admin
from django.utils.html import format_html
from .models import *

def image_preview(obj, field_name="image"):
    value = getattr(obj, field_name, None)
    return format_html('<img src="{}" style="max-height:70px;max-width:140px;border-radius:8px" alt="Preview">', value.url) if value else "—"

class OrderedAdmin(admin.ModelAdmin):
    list_display = ("__str__", "display_order", "is_active", "updated_at")
    list_filter = ("is_active",)
    ordering = ("display_order",)
    list_editable = ("display_order", "is_active")
    readonly_fields = ("created_at", "updated_at")

class ServiceFeatureInline(admin.TabularInline): model = ServiceFeature; extra = 1
class ProjectFeatureInline(admin.TabularInline): model = ProjectFeature; extra = 1
class ProjectMediaInline(admin.TabularInline): model = ProjectMedia; extra = 1

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("agency_name", "email", "phone", "updated_at")
    search_fields = ("agency_name", "email")
    readonly_fields = ("created_at", "updated_at", "logo_preview")
    fieldsets = (("Brand", {"fields": ("agency_name", "tagline", "description", "logo", "logo_preview", "favicon")}), ("Contact", {"fields": ("email", "phone", "address")}), ("SEO", {"fields": ("seo_title", "seo_description", "canonical_url", "og_image")}), ("Footer", {"fields": ("copyright_text",)}), ("System", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}))
    @admin.display(description="Logo preview")
    def logo_preview(self, obj): return image_preview(obj, "logo")
    def has_add_permission(self, request): return not SiteSettings.objects.exists()

@admin.register(NavigationItem)
class NavigationItemAdmin(OrderedAdmin):
    list_display = ("label", "url", "parent", "is_cta", "display_order", "is_active")
    list_filter = ("is_active", "is_cta", "open_in_new_tab")
    search_fields = ("label", "url")
    prepopulated_fields = {}

@admin.register(HeroSlide)
class HeroSlideAdmin(OrderedAdmin):
    list_display = ("internal_name", "heading", "video_source", "duration_seconds", "display_order", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("internal_name", "heading", "description")
    readonly_fields = ("poster_preview", "created_at", "updated_at")
    fieldsets = (
        ("Content", {"fields": ("internal_name", "eyebrow", "heading", "description")}),
        ("Video", {"fields": ("video_file", "video_url", "poster_image", "poster_preview", "duration_seconds", "overlay_strength")}),
        ("Calls to action", {"fields": ("primary_button_text", "primary_button_url", "secondary_button_text", "secondary_button_url")}),
        ("Publishing", {"fields": ("is_active", "display_order")}),
        ("System", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    @admin.display(description="Video")
    def video_source(self, obj): return "Uploaded file" if obj.video_file else "External URL"
    @admin.display(description="Poster preview")
    def poster_preview(self, obj): return image_preview(obj, "poster_image")

@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    list_display = ("title", "slug", "is_featured", "display_order", "is_active", "updated_at")
    list_filter = ("is_active", "is_featured")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceFeatureInline]
    fieldsets = (("Service", {"fields": ("title", "slug", "short_description", "description", "outcome", "icon_name", "image")}), ("Publishing", {"fields": ("is_active", "is_featured", "display_order")}), ("SEO", {"fields": ("seo_title", "seo_description", "canonical_url", "og_image")}), ("System", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}))

@admin.register(Project)
class ProjectAdmin(OrderedAdmin):
    list_display = ("title", "category", "is_featured", "display_order", "is_active", "published_at")
    list_filter = ("is_active", "is_featured", "category", "technologies")
    search_fields = ("title", "subtitle", "overview", "problem", "solution")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [ProjectFeatureInline, ProjectMediaInline]
    fieldsets = (("Project", {"fields": ("title", "slug", "subtitle", "category", "overview", "problem", "solution", "result")}), ("Media & links", {"fields": ("thumbnail", "demo_video_url", "project_url", "github_url")}), ("Technology", {"fields": ("technologies",)}), ("Publishing", {"fields": ("is_active", "is_featured", "display_order", "published_at")}), ("SEO", {"fields": ("seo_title", "seo_description", "canonical_url", "og_image")}), ("System", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}))

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "service", "status", "created_at")
    list_filter = ("status", "service", "created_at")
    search_fields = ("name", "email", "company", "project_description")
    ordering = ("-created_at",)
    list_editable = ("status",)
    readonly_fields = ("name", "email", "phone", "company", "service", "budget_range", "project_description", "preferred_contact_method", "source_ip_hash", "created_at", "updated_at")

@admin.register(Technology)
class TechnologyAdmin(OrderedAdmin):
    list_display = ("name", "category", "display_order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Testimonial)
class TestimonialAdmin(OrderedAdmin):
    list_display = ("customer_name", "company", "rating", "is_featured", "display_order", "is_active")
    list_filter = ("rating", "is_featured", "is_active")
    search_fields = ("customer_name", "company", "review")

@admin.register(Client)
class ClientAdmin(OrderedAdmin):
    list_display = ("company_name", "website", "display_order", "is_active")
    search_fields = ("company_name", "description")

@admin.register(TeamMember)
class TeamMemberAdmin(OrderedAdmin):
    list_display = ("name", "designation", "email", "display_order", "is_active", "updated_at")
    list_filter = ("is_active", "designation")
    search_fields = ("name", "designation", "description", "email")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fieldsets = (
        ("Profile", {"fields": ("name", "designation", "image", "image_preview", "description")}),
        ("Contact links", {"fields": ("email", "linkedin_url")}),
        ("Publishing", {"fields": ("is_active", "display_order")}),
        ("System", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    @admin.display(description="Image preview")
    def image_preview(self, obj): return image_preview(obj, "image")

@admin.register(Page)
class PageAdmin(OrderedAdmin):
    list_display = ("title", "slug", "display_order", "is_active", "updated_at")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(HeroSection)
admin.site.register(AboutSection)
admin.site.register(Statistic, OrderedAdmin)
admin.site.register(ProjectCategory, OrderedAdmin)
admin.site.register(CTASection, OrderedAdmin)
admin.site.register(FooterLink, OrderedAdmin)
admin.site.register(SocialLink, OrderedAdmin)
