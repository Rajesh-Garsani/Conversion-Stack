from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import ContactInquiry, HeroSlide, Project, ProjectCategory, Service, SiteSettings, TeamMember

class PublicApiTests(APITestCase):
    def setUp(self):
        self.service = Service.objects.create(title="Automation", slug="automation", short_description="Automation service", description="Automate business work.", is_active=True)
        category = ProjectCategory.objects.create(name="Operations", slug="operations")
        Project.objects.create(title="Workflow Platform", slug="workflow-platform", category=category, overview="A useful project", is_active=True)

    def test_services_list_only_active_content(self):
        Service.objects.create(title="Hidden", slug="hidden", short_description="Hidden", description="Hidden", is_active=False)
        response = self.client.get("/api/services/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_project_detail_uses_slug(self):
        response = self.client.get("/api/projects/workflow-platform/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Workflow Platform")

    def test_contact_submission_is_persisted(self):
        response = self.client.post("/api/contact/", {"name": "Test User", "email": "test@example.com", "service": self.service.pk, "project_description": "We need a secure automation workflow for our team.", "preferred_contact_method": "Email", "website": ""}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(ContactInquiry.objects.count(), 1)

    def test_honeypot_rejects_spam(self):
        response = self.client.post("/api/contact/", {"name": "Bot User", "email": "bot@example.com", "project_description": "A long enough spam message for validation.", "website": "spam.example"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactInquiry.objects.count(), 0)

    def test_site_settings_are_singleton(self):
        SiteSettings.objects.create(agency_name="Your Agency")
        second = SiteSettings(agency_name="Another Name")
        second.save()
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_bootstrap_returns_only_visible_carousel_and_team_content(self):
        HeroSlide.objects.create(internal_name="Visible", heading="Visible slide", video_url="https://example.com/video.mp4", is_active=True)
        HeroSlide.objects.create(internal_name="Hidden", heading="Hidden slide", video_url="https://example.com/hidden.mp4", is_active=False)
        TeamMember.objects.create(name="Visible Member", designation="Engineer", image="team/visible.jpg", description="Builds reliable systems.", is_active=True)
        TeamMember.objects.create(name="Hidden Member", designation="Engineer", image="team/hidden.jpg", description="Hidden profile.", is_active=False)

        response = self.client.get("/api/bootstrap/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([slide["heading"] for slide in response.data["data"]["hero_slides"]], ["Visible slide"])
        self.assertEqual([member["name"] for member in response.data["data"]["team"]], ["Visible Member"])
