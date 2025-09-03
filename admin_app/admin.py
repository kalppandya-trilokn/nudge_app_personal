# admin.py
from datetime import timedelta, date
from django.contrib import admin, messages
from django.utils import timezone
from django.apps import apps
from django.contrib.admin import AdminSite
from .models import Users, Prompts, ChatSessions


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "name", "age", "location", "status", "suspended_until", "created_at")
    list_filter = ("status", "location", "created_at")  # Using our custom filter
    search_fields = ("phone_number", "name", "location")
    readonly_fields = ("created_at",)
    actions = ["make_active", "suspend_for_30_days", "block_users"]

    def make_active(self, request, queryset):
        updated = queryset.update(status=Users.STATUS_ACTIVE, suspended_until=None)
        self.message_user(request, f"{updated} user(s) marked Active.", level=messages.SUCCESS)

    def suspend_for_30_days(self, request, queryset):
        until = timezone.now() + timedelta(days=30)
        updated = queryset.update(status=Users.STATUS_SUSPENDED, suspended_until=until)
        self.message_user(request, f"{updated} user(s) suspended until {until:%Y-%m-%d}.", level=messages.WARNING)

    def block_users(self, request, queryset):
        updated = queryset.update(status=Users.STATUS_BLOCKED, suspended_until=None)
        self.message_user(request, f"{updated} user(s) blocked.", level=messages.ERROR)


@admin.register(Prompts)
class PromptsAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'text', 'ai_response', 'status', 'session_order', 'created_at', 'moderation_reason')
    # Filter and search options
    list_filter = ('status', 'created_at')
    search_fields = ('text', 'ai_response', 'moderation_reason')
    # The ForeignKey relationship should be handled automatically, so list_select_related isn't strictly necessary here but can be added for performance if you have many related objects.
    list_select_related = ('session',)
    # Specify fields for searching within the related ChatSession model
    raw_id_fields = ('session',)



# ModelAdmin for the ChatSessions model
# @admin.register(ChatSessions)
# class ChatSessionsAdmin(admin.ModelAdmin):
#     # Display all the fields from your model in the changelist view
#     list_display = ('id', 'user', 'message_count', 'is_completed', 'last_activity_at', 'created_at')
#     # Filter and search options
#     list_filter = ('is_completed', 'created_at')
#     search_fields = ('user__phone_number', 'user__name',)
#     # Use select_related for performance
#     list_select_related = ('user',)
#     # Use a raw ID field for the foreign key to avoid performance issues
#     raw_id_fields = ('user',)

class MyAdminSite(AdminSite):
    site_header = "Welcome to Nudge"
    site_title = "Nudge Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        filter_option = request.GET.get("filter", "all")
        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")

        total_users = Users.objects.count()
        users_count = total_users

        try:
            if filter_option == "daily":
                users_count = Users.objects.filter(
                    created_at__date=timezone.now().date()
                ).count()
            elif filter_option == "weekly":
                start_week = timezone.now() - timedelta(days=7)
                users_count = Users.objects.filter(
                    created_at__gte=start_week
                ).count()
            elif filter_option == "monthly":
                start_month = timezone.now() - timedelta(days=30)
                users_count = Users.objects.filter(
                    created_at__gte=start_month
                ).count()
            elif filter_option == "yearly":
                start_year = timezone.now() - timedelta(days=365)
                users_count = Users.objects.filter(
                    created_at__gte=start_year
                ).count()
            elif filter_option == "to_date" and end_date_str:
                end_date = date.fromisoformat(end_date_str)
                users_count = Users.objects.filter(
                    created_at__date__lte=end_date
                ).count()
            elif filter_option == "custom_range" and start_date_str and end_date_str:
                start_date = date.fromisoformat(start_date_str)
                end_date = date.fromisoformat(end_date_str)
                users_count = Users.objects.filter(
                    created_at__date__range=[start_date, end_date]
                ).count()
        except ValueError:
            # Fallback if date strings are invalid
            users_count = 0

        context = {
            "total_users": total_users,
            "users_count": users_count,
            "filter_option": filter_option,
            "start_date_str": start_date_str,
            "end_date_str": end_date_str,
        }

        if extra_context:
            context.update(extra_context)

        return super().index(request, extra_context=context)

# create a global admin site instance
my_admin_site = MyAdminSite(name="myadmin")

# Register your models again to the custom site
my_admin_site.register(Users, UsersAdmin)
my_admin_site.register(Prompts, PromptsAdmin)
# my_admin_site.register(ChatSessions, ChatSessionsAdmin) 