import email

from django.test import TestCase
from django.urls import reverse

from .models import User
from .views import DashboarView, UserLoginView, UserRegistrationView


class UserRegistrationViewTests(TestCase):
    def test_get_registration_page(self):
        response = self.client.get(reverse("users:registration"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration.html")

    def test_register_user_success(self):
        data = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@doe.com",
            "role": "student",
            "nationality": "Indian",
            "mobile": "9876543210",
            "password": "testpass123",
        }
        response = self.client.post(reverse("users:registration"), data)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("users:login"))

    def test_register_user_failure(self):
        data = {
            "firstname": "Jane",
            "lastname": "Doe",
            "email": "john@doe.com",  # duplicate email
            "role": "student",
            "nationality": "American",
            "mobile": "9876543210",
            "password": "testpass123",
        }
        response = self.client.post(reverse("users:registration"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "users/registration.html")
        self.assertContains(response, "Email already exists")


class UserLoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="john@doe.com", email="john@doe.com", password="testpass123"
        )

    def test_get_login_page(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_success(self):
        data = {"email": "john@doe.com", "password": "testpass123"}
        response = self.client.post(reverse("users:login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("users:dashboard"))

    def test_login_failure(self):
        data = {
            "email": "john@doe.com",
            "password": "wrongpass",
        }
        response = self.client.post(reverse("users:login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertContains(response, "Invalid email or password")


class DashboarViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="john@doe.com",
            email="john@doe.com",
            password="testpass123",
            role="student",
        )

    def test_dashboard_redirect_unauthenticated(self):
        response = self.client.get(reverse("users:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login"))

    def test_dashboard_student(self):
        self.client.login(email="john@doe.com", password="testpass123")
        response = self.client.get(reverse("users:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/student.html")

    def test_dashboard_staff(self):
        self.user.role = "staff"
        self.user.save()
        self.client.login(email="john@doe.com", password="testpass123")
        response = self.client.get(reverse("users:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/staff.html")

    def test_dashboard_admin(self):
        self.user.role = "admin"
        self.user.save()
        self.client.login(email="john@doe.com", password="testpass123")
        response = self.client.get(reverse("users:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/admin.html")

    def test_dashboard_admin_success(self):
        user = User.objects.create(
            username="john@doe.com",
            email="john@doe.com",
            password="testpass123",
            role="admin",
        )
        self.client.login(email="john@doe.com", password="testpass123")
        response = self.client.get(reverse("users:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_admin_unauthenticated(self):
        response = self.client.get(reverse("users:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:login"))
