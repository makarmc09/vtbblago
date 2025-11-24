from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Donation, HelpRequest, User

def help_request(request):
    return render(request, "VTBBlago/help.html")


def help_form(request):
    help_type = request.GET.get("type", "other")
    error = None
    success = False

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        message = request.POST.get("message")

        user = User.objects.filter(email=email, password=password).first()

        if not user:
            error = "Неверный email или пароль."
        elif not message.strip():
            error = "Введите текст запроса."
        else:

            HelpRequest.objects.create(
                name=user.name,
                email=user.email,
                message=f"[{help_type}] {message}"
            )
            success = True

    return render(request, "VTBBlago/help_form.html", {
        "help_type": help_type,
        "error": error,
        "success": success
    })


def index(request):
    total = sum((p.collected or Decimal("0.00")) for p in Project.objects.all())
    today = datetime.today().date()
    start_date = today - timedelta(days=6)

    donations = (
        Donation.objects
        .filter(created_at__date__gte=start_date)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Sum("amount"))
        .order_by("day")
    )

    normalized = [{"day": d["day"].strftime("%Y-%m-%d"), "total": d["total"]} for d in donations]

    chart_data = []
    for offset in range(7):
        day = start_date + timedelta(days=offset)
        dstr = day.strftime("%Y-%m-%d")
        total_amount = next((d["total"] for d in normalized if d["day"] == dstr), 0)
        chart_data.append({"day": day.strftime("%d-%m"), "total": float(total_amount)})

    return render(request, "VTBBlago/index.html", {"total": total, "chart_data": chart_data})

def projects(request):
    projects = Project.objects.all()
    category = request.GET.get("category")
    sort = request.GET.get("sort")

    if category:
        projects = projects.filter(category=category)
    if sort == "collected":
        projects = projects.order_by("-collected")
    elif sort == "goal":
        projects = projects.order_by("-goal")

    return render(request, "VTBBlago/project.html", {
        "projects": projects,
        "selected_category": category,
        "selected_sort": sort
    })


def pay(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    error = None

    if project.collected_all:
        return render(request, "VTBBlago/pay.html", {
            "project": project,
            "error": "Сбор завершён. Пожертвования закрыты."
        })

    if request.method == "POST":
        anonymous = request.POST.get("anonymous") == "on"
        email = request.POST.get("email")
        password = request.POST.get("password")
        amount_raw = request.POST.get("amount")

        try:
            amount = Decimal(amount_raw)
            if amount <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            error = "Неверная сумма. Введите положительное число."
            return render(request, "VTBBlago/pay.html", {"project": project, "error": error})

        user = None
        if not anonymous and email and password:
            user = User.objects.filter(email=email, password=password).first()

        Donation.objects.create(project=project, amount=amount, user=user, anonymous=anonymous)
        project.collected = (project.collected or Decimal("0.00")) + amount
        project.save()
        if user:
            user.balance = (user.balance or Decimal("0.00")) + amount
            user.save()

        return redirect("projects")

    return render(request, "VTBBlago/pay.html", {"project": project})

def about(request):
    return render(request, "VTBBlago/about.html")

def register(request):
    created = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        password = request.POST.get("password")
        if name and email and number and password:
            if not User.objects.filter(email=email).exists():
                User.objects.create(name=name, email=email, number=number, password=password, balance=Decimal("0.00"))
                created = True
            else:
                return render(request, "VTBBlago/register.html", {"error": "Почта уже используется."})
    return render(request, "VTBBlago/register.html", {"created": created})

def login_view(request):
    failed = False
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email=email, password=password).first()
        if user:
            request.session["user_id"] = user.id
            return redirect("index")
        else:
            failed = True
    return render(request, "VTBBlago/login.html", {"failed": failed})
