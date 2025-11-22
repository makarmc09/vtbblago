from django.contrib import admin
from .models import Project, Donation, HelpRequest, User


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "goal", "collected")
    search_fields = ("title",)
    list_filter = ("goal",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("project", "amount")
    search_fields = ("project__title",)
    list_filter = ("project",)


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")
    search_fields = ("name", "email", "message")

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("name", "email", "balance")
    search_fields = ("name",)