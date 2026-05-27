from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import ResumeScreen
from .ai_service import screen_resume
from .utils import extract_text_from_pdf


# ── AUTH VIEWS ──

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not password1:
            messages.error(request, 'Username and password are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'Welcome, {username}! Account created.')
            return redirect('dashboard')
    return render(request, 'auth/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ── MAIN VIEWS ──

@login_required
def dashboard(request):
    screens = ResumeScreen.objects.filter(user=request.user)[:10]
    total = ResumeScreen.objects.filter(user=request.user).count()
    avg_score = 0
    if total > 0:
        avg_score = int(sum(s.ats_score for s in ResumeScreen.objects.filter(user=request.user)) / total)
    return render(request, 'screener/dashboard.html', {
        'screens': screens,
        'total': total,
        'avg_score': avg_score,
    })


@login_required
def screen_view(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '').strip()
        job_description = request.POST.get('job_description', '').strip()
        input_type = request.POST.get('input_type', 'text')

        resume_text = ''

        if input_type == 'pdf':
            pdf_file = request.FILES.get('resume_pdf')
            if not pdf_file:
                messages.error(request, 'Please upload a PDF file.')
                return render(request, 'screener/screen.html')
            resume_text = extract_text_from_pdf(pdf_file)
            if not resume_text:
                messages.error(request, 'Could not extract text from PDF. Try pasting the text instead.')
                return render(request, 'screener/screen.html')
        else:
            resume_text = request.POST.get('resume_text', '').strip()

        if not job_title or not job_description or not resume_text:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'screener/screen.html')

        # Call Groq AI
        result = screen_resume(resume_text, job_description, job_title)

        if result.get('error'):
            messages.error(request, f'AI Error: {result["error"]}')
            return render(request, 'screener/screen.html')

        # Save to DB
        screen = ResumeScreen.objects.create(
            user=request.user,
            job_title=job_title,
            job_description=job_description,
            resume_text=resume_text,
            ats_score=result['ats_score'],
            matched_skills=', '.join(result['matched_skills']),
            missing_skills=', '.join(result['missing_skills']),
            suggestions='\n'.join(result['suggestions']),
            overall_feedback=result['overall_feedback'],
        )
        return redirect('result', pk=screen.pk)

    return render(request, 'screener/screen.html')


@login_required
def result_view(request, pk):
    screen = get_object_or_404(ResumeScreen, pk=pk, user=request.user)
    score = screen.ats_score
    if score >= 85:
        score_label = "Excellent"
        score_color = "success"
    elif score >= 70:
        score_label = "Good"
        score_color = "info"
    elif score >= 50:
        score_label = "Average"
        score_color = "warning"
    else:
        score_label = "Poor"
        score_color = "danger"

    return render(request, 'screener/result.html', {
        'screen': screen,
        'score_label': score_label,
        'score_color': score_color,
    })


@login_required
def history_view(request):
    screens = ResumeScreen.objects.filter(user=request.user)
    return render(request, 'screener/history.html', {'screens': screens})


@login_required
def delete_screen(request, pk):
    screen = get_object_or_404(ResumeScreen, pk=pk, user=request.user)
    screen.delete()
    messages.success(request, 'Record deleted.')
    return redirect('history')
