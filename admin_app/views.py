from datetime import date, timedelta
from django.shortcuts import render
from .models import Users
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_view(request):
    total_users = Users.objects.count()
    users_count = None
    
    filter_option = request.GET.get('filter', 'all')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    today = date.today()

    if filter_option == 'all':
        users_count = total_users
    elif filter_option == 'daily':
        users_count = Users.objects.filter(created_at__date=today).count()
    elif filter_option == 'weekly':
        start = today - timedelta(days=7)
        users_count = Users.objects.filter(created_at__date__gte=start).count()
    elif filter_option == 'monthly':
        start = today - timedelta(days=30)
        users_count = Users.objects.filter(created_at__date__gte=start).count()
    elif filter_option == 'yearly':
        start = today - timedelta(days=365)
        users_count = Users.objects.filter(created_at__date__gte=start).count()
    elif filter_option == 'to_date' and end_date_str:
        try:
            end_date = date.fromisoformat(end_date_str)
            users_count = Users.objects.filter(created_at__date__lte=end_date).count()
        except ValueError:
            users_count = 0
    elif filter_option == 'custom_range' and start_date_str and end_date_str:
        try:
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
            users_count = Users.objects.filter(created_at__date__range=[start_date, end_date]).count()
        except ValueError:
            users_count = 0

    context = {
        'total_users': total_users,
        'filter_option': filter_option,
        'users_count': users_count,
        'start_date_str': start_date_str,
        'end_date_str': end_date_str,
    }

    return render(request, 'admin_app/dashboard.html', context)
