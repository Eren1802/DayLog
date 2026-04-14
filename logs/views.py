import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import DailyLogForm
from .models import DailyLog

@login_required
def complete_pending(request, log_id):
    log = DailyLog.objects.get(id=log_id, user=request.user)
    log.pending = ''
    log.save()
    return redirect('dashboard')
def dashboard(request):
    if request.method == 'POST':
        form = DailyLogForm(request.POST)
        if form.is_valid():
            DailyLog.objects.create(
                user=request.user,
                done=form.cleaned_data['done'],
                pending=form.cleaned_data['pending'],
                mood=form.cleaned_data['mood']
            )
            return redirect('dashboard')
    else:
        form = DailyLogForm()

    today = timezone.now().date()
    week_start = today - timedelta(days=7)

    logs = DailyLog.objects.filter(user=request.user).order_by('-date')
    total_logs = logs.count()
    week_logs = DailyLog.objects.filter(user=request.user, date__gte=week_start).count()

    streak = 0
    check_date = today
    while DailyLog.objects.filter(user=request.user, date=check_date).exists():
        streak += 1
        check_date -= timedelta(days=1)
    # Weekly analysis data
    week_days = []
    week_counts = []
    week_moods = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = DailyLog.objects.filter(user=request.user, date=day).count()
        moods = list(DailyLog.objects.filter(user=request.user, date=day).values_list('mood', flat=True))
        week_days.append(day.strftime('%a'))
        week_counts.append(count)
        if moods:
            week_moods.append(moods[-1])
        else:
            week_moods.append('')

    most_productive_day = week_days[week_counts.index(max(week_counts))] if max(week_counts) > 0 else 'None'

    return render(request, 'logs/dashboard.html', {
        'form': form,
        'logs': logs,
        'total_logs': total_logs,
        'week_logs': week_logs,
        'streak': streak,
        'today': today,
        'week_days': json.dumps(week_days),
        'week_counts': json.dumps(week_counts),
        'week_moods': json.dumps(week_moods),
        'most_productive_day': most_productive_day,
    })

@login_required
def delete_log(request, log_id):
    log = DailyLog.objects.get(id=log_id, user=request.user)
    log.delete()
    return redirect('dashboard')

@login_required
def edit_log(request, log_id):
    log = DailyLog.objects.get(id=log_id, user=request.user)
    if request.method == 'POST':
        log.done = request.POST.get('done')
        log.pending = request.POST.get('pending')
        log.mood = request.POST.get('mood')
        log.save()
        return redirect('dashboard')
    return render(request, 'logs/edit_log.html', {'log': log})