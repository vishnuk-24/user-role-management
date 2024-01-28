from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, UpdateView

User = get_user_model()

ROLE_TEMPLATE = {
    "student": "users/student.html",
    "staff": "users/staff.html",
    "admin": "users/admin.html",
    "editor": "users/editor.html",
}


class UserRegistrationView(View):
    def get(self, request):
        return render(request, "users/registration.html")

    def post(self, request):
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        role = request.POST.get("role")
        nationality = request.POST.get("nationality")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(
                request, "users/registration.html", {"error": "Email already exists"}
            )

        with transaction.atomic():
            # Create a new user with user roles
            user = User.objects.create(
                username=email,
                first_name=firstname,
                last_name=lastname,
                email=email,
                role=role,
                nationality=nationality,
                mobile=mobile,
            )
            if user:
                user.set_password(password)
                user.save()

        return redirect("users:login")


class UserLoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            return redirect("users:dashboard")
        else:
            # return invalid credentials error message
            return render(
                request, "users/login.html", {"error": "Invalid email or password"}
            )


class DashboarView(View):
    def get(self, request):
        if request.user.is_authenticated:
            role = request.user.role
            template = ROLE_TEMPLATE[role]
            if role == "student":
                users = User.objects.get(username=request.user.username)
            elif role == "staff":
                users = User.objects.filter(role="student")
            elif role == "editor":
                users = User.objects.filter(role__in=["staff", "student"])
            else:
                users = User.objects.all()
            return render(request, template, {"users": users})
        else:
            return redirect("users:login")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")


class UserProfileView(DetailView):
    model = User
    fields = ["first_name", "last_name", "email", "nationality", "mobile"]
    template_name = "users/profile.html"


class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "email", "nationality", "mobile"]
    template_name = "users/user_edit.html"

    def get_success_url(self):
        return reverse("users:dashboard")
