from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .validators import validate_media_file, validate_video_file

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class OrderedVisibleModel(TimeStampedModel):
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    class Meta:
        abstract = True

class SEOFields(models.Model):
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=170, blank=True)
    canonical_url = models.URLField(blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True, validators=[validate_media_file])
    class Meta:
        abstract = True

class SiteSettings(TimeStampedModel, SEOFields):
    agency_name = models.CharField(max_length=120, default="Your Agency")
    tagline = models.CharField(max_length=180, default="Software & Digital Solutions")
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True, validators=[validate_media_file])
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True, validators=[validate_media_file])
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    copyright_text = models.CharField(max_length=255, blank=True)
    class Meta:
        verbose_name_plural = "Site settings"
    def __str__(self): return self.agency_name
    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
            self.created_at = existing.created_at
        super().save(*args, **kwargs)

class NavigationItem(OrderedVisibleModel):
    label = models.CharField(max_length=80)
    url = models.CharField(max_length=255)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)
    open_in_new_tab = models.BooleanField(default=False)
    is_cta = models.BooleanField(default=False)
    class Meta:
        ordering = ["display_order", "id"]
    def __str__(self): return self.label

class HeroSection(TimeStampedModel):
    eyebrow = models.CharField(max_length=120, blank=True)
    heading = models.CharField(max_length=220)
    highlighted_text = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.CharField(max_length=255, blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.CharField(max_length=255, blank=True)
    background_image = models.ImageField(upload_to="hero/", blank=True, null=True, validators=[validate_media_file])
    video_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Hero section"
    def __str__(self): return self.heading

class HeroSlide(OrderedVisibleModel):
    internal_name = models.CharField(max_length=120, help_text="Admin-only label used to identify this slide.")
    eyebrow = models.CharField(max_length=120, blank=True)
    heading = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to="hero/videos/", blank=True, null=True, validators=[validate_video_file])
    video_url = models.URLField(blank=True, help_text="Optional direct MP4/WebM URL. Uploads take priority.")
    poster_image = models.ImageField(upload_to="hero/posters/", blank=True, null=True, validators=[validate_media_file])
    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.CharField(max_length=255, blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.CharField(max_length=255, blank=True)
    duration_seconds = models.PositiveSmallIntegerField(default=8, validators=[MinValueValidator(4), MaxValueValidator(30)], help_text="Fallback slide duration if the video does not end first.")
    overlay_strength = models.PositiveSmallIntegerField(default=58, validators=[MinValueValidator(20), MaxValueValidator(85)], help_text="Dark overlay percentage for readable text.")
    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Hero video slide"
        verbose_name_plural = "Hero video slides"
    def __str__(self): return self.internal_name
    def clean(self):
        super().clean()
        if not self.video_file and not self.video_url:
            raise ValidationError("Upload a video file or provide a direct video URL.")

class AboutSection(TimeStampedModel):
    eyebrow = models.CharField(max_length=120, blank=True)
    heading = models.CharField(max_length=220)
    introduction = models.TextField()
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    philosophy = models.TextField(blank=True)
    image = models.ImageField(upload_to="about/", blank=True, null=True, validators=[validate_media_file])
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "About section"
    def __str__(self): return self.heading

class Statistic(OrderedVisibleModel):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=40)
    suffix = models.CharField(max_length=20, blank=True)
    def __str__(self): return f"{self.value}{self.suffix} {self.label}"

class Technology(OrderedVisibleModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    category = models.CharField(max_length=80, db_index=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="technologies/", blank=True, null=True, validators=[validate_media_file])
    class Meta:
        ordering = ["category", "display_order", "name"]
        verbose_name_plural = "Technologies"
    def __str__(self): return self.name

class Service(OrderedVisibleModel, SEOFields):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    short_description = models.TextField(max_length=500)
    description = models.TextField()
    outcome = models.TextField(blank=True)
    icon_name = models.CharField(max_length=80, blank=True, help_text="Lucide icon name used by the frontend")
    image = models.ImageField(upload_to="services/", blank=True, null=True, validators=[validate_media_file])
    is_featured = models.BooleanField(default=False, db_index=True)
    class Meta:
        ordering = ["display_order", "title"]
    def __str__(self): return self.title

class ServiceFeature(OrderedVisibleModel):
    service = models.ForeignKey(Service, related_name="features", on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ["display_order", "id"]
    def __str__(self): return f"{self.service}: {self.title}"

class ProjectCategory(OrderedVisibleModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    def __str__(self): return self.name

class Project(OrderedVisibleModel, SEOFields):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    subtitle = models.CharField(max_length=220, blank=True)
    category = models.ForeignKey(ProjectCategory, related_name="projects", on_delete=models.PROTECT)
    overview = models.TextField()
    problem = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    result = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True, null=True, validators=[validate_media_file])
    demo_video_url = models.URLField(blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    technologies = models.ManyToManyField(Technology, related_name="projects", blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    published_at = models.DateField(blank=True, null=True)
    class Meta:
        ordering = ["display_order", "-published_at", "title"]
    def __str__(self): return self.title

class ProjectFeature(OrderedVisibleModel):
    project = models.ForeignKey(Project, related_name="features", on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ["display_order", "id"]
    def __str__(self): return f"{self.project}: {self.title}"

class ProjectMedia(OrderedVisibleModel):
    MEDIA_TYPES = (("image", "Image"), ("video", "Video"))
    project = models.ForeignKey(Project, related_name="media", on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default="image")
    file = models.FileField(upload_to="projects/media/", blank=True, null=True, validators=[validate_media_file])
    external_url = models.URLField(blank=True)
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    class Meta:
        ordering = ["display_order", "id"]
    def __str__(self): return f"{self.project} {self.media_type}"

class Client(OrderedVisibleModel):
    company_name = models.CharField(max_length=160)
    logo = models.ImageField(upload_to="clients/", blank=True, null=True, validators=[validate_media_file])
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ["display_order", "company_name"]
    def __str__(self): return self.company_name

class TeamMember(OrderedVisibleModel):
    name = models.CharField(max_length=120)
    designation = models.CharField(max_length=140)
    image = models.ImageField(upload_to="team/", validators=[validate_media_file])
    description = models.TextField(max_length=800)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    class Meta:
        ordering = ["display_order", "name"]
    def __str__(self): return f"{self.name} — {self.designation}"

class Testimonial(OrderedVisibleModel):
    customer_name = models.CharField(max_length=120)
    company = models.CharField(max_length=160, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    profile_image = models.ImageField(upload_to="testimonials/profiles/", blank=True, null=True, validators=[validate_media_file])
    company_logo = models.ImageField(upload_to="testimonials/logos/", blank=True, null=True, validators=[validate_media_file])
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    class Meta:
        ordering = ["display_order", "-review_date"]
    def __str__(self): return self.customer_name

class CTASection(OrderedVisibleModel):
    name = models.CharField(max_length=100, unique=True)
    eyebrow = models.CharField(max_length=120, blank=True)
    heading = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.CharField(max_length=255, blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.CharField(max_length=255, blank=True)
    def __str__(self): return self.name

class FooterLink(OrderedVisibleModel):
    group = models.CharField(max_length=80, default="Company")
    label = models.CharField(max_length=80)
    url = models.CharField(max_length=255)
    def __str__(self): return self.label

class SocialLink(OrderedVisibleModel):
    platform = models.CharField(max_length=80)
    url = models.URLField()
    icon_name = models.CharField(max_length=80, blank=True)
    def __str__(self): return self.platform

class Page(OrderedVisibleModel, SEOFields):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    eyebrow = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    class Meta:
        ordering = ["display_order", "title"]
    def __str__(self): return self.title

class ContactInquiry(TimeStampedModel):
    STATUS_CHOICES = (("new", "New"), ("contacted", "Contacted"), ("qualified", "Qualified"), ("closed", "Closed"))
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    company = models.CharField(max_length=160, blank=True)
    service = models.ForeignKey(Service, blank=True, null=True, related_name="inquiries", on_delete=models.SET_NULL)
    budget_range = models.CharField(max_length=80, blank=True)
    project_description = models.TextField()
    preferred_contact_method = models.CharField(max_length=40, default="Email")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", db_index=True)
    source_ip_hash = models.CharField(max_length=64, blank=True, db_index=True)
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "-created_at"], name="contact_status_created")]
    def __str__(self): return f"{self.name} — {self.email}"
