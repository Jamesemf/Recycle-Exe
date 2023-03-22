from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .models import Statistic, Goal, UserGoal
from home.models import Transaction
from django.urls import reverse
from django.db.models import Q
from products.models import Product
from home.views import reset_sessions
import datetime
import schedule
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Count


def register(request):
    """
    Web backend for '../account/registration' (name 'registration')
    Registration page for new user register their account.

    Returns:
        * for 'POST' method:
            -> Registration page if form is not valid (Error information appears)
            -> Success-welcome page if form is valid and create the new user.
        * Registration page if used 'GET' method.
    """
    if request.user.is_authenticated:
        return redirect('index')
    if Product.objects.count() == 0:
        default_product = Product(
            barcode='1', name='None', weight=0, material='None', recycle='None')
        default_product.save()
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            if user_form.cleaned_data['password'] != user_form.cleaned_data['password_confirm']:
                return render(request, 'registration/register.html', {'user_form': user_form})
            # New user object without saving
            new_user = user_form.save(commit=False)
            # Set password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_statistic = Statistic.objects.create(user=new_user)
            new_statistic.save()
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            login(request, user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def password(request):
    """
    Web backend for '../account/password/' (name 'password')
    Display password change center middle page.

    Returns:
        * Password center page.
    """
    return render(request, 'account/password.html')


def account(request):
    """
    Web backend for 'account/' (name 'account')
    Display user recycle stats and points if the user is authenticated.

    Returns:
        * Account page with user recycle stats if user authenticated.
        * Redirect to login page if user is not authenticated.
    """
    reset_sessions(request)
    schedule.run_pending()
    if request.user.is_superuser:
        return redirect('index')
    if request.user.is_authenticated:
        data = Statistic.objects.get(user=request.user)
        loveRecycling = 0
        lastTransaction = 0
        if Transaction.objects.filter(user=request.user).exists():
            lastTransaction = Transaction.objects.filter(
                user=request.user).latest('time')
            transactionCount = Transaction.objects.annotate(num_transactions=Count('product', filter=Q(user=request.user)))
            loveRecycling = transactionCount.first()
        maxWeek = Statistic.objects.all().order_by('-curweek')[0]
        maxMonth = Statistic.objects.all().order_by('-curmonth')[0]
        maxYear = Statistic.objects.all().order_by('-curyear')[0]
        goalData = Goal.objects.all()
        userGoal1 = UserGoal.objects.filter(
            Q(userGoalNum=1) & Q(user=request.user)).first()
        userGoal2 = UserGoal.objects.filter(
            Q(userGoalNum=2) & Q(user=request.user)).first()
        userGoal3 = UserGoal.objects.filter(
            Q(userGoalNum=3) & Q(user=request.user)).first()
        data_dict = {
            'Profile': data,
            'maxWeek': maxWeek,
            'maxMonth': maxMonth,
            'maxYear': maxYear,
            'Goals': goalData,
            'UserGoal1': userGoal1,
            'UserGoal2': userGoal2,
            'UserGoal3': userGoal3,
            'lastTrans': lastTransaction,
            'loveRecycling': loveRecycling
        }
        return render(request, 'account/Profile_page.html', data_dict)
    else:
        return redirect('login')


def addUserGoal(request):
    """
    Web backend for '../account/addUserGoal/' (name 'addUserGoal')
    Create UserGoal model and redirect user back to account page.

    Returns:
        * Redirect to account page.
    """
    x = request.POST['goalNum']
    y = request.POST['goal-options']
    # This comment may no longer be needed -> # this is plastic and all the others
    z = request.POST['goal-type']
    goalNumType = Goal.objects.get(pk=y)
    current_user = request.user
    # Checking if the user has already got a goal for this specific value
    goalSet = UserGoal.objects.filter(Q(userGoalNum=x) & Q(user=current_user))
    if not goalSet:
        goal = UserGoal(userGoalNum=x, user=current_user,
                        goal=goalNumType, value=0, goalType=z)
        goal.save()
    else:
        UserGoal.objects.filter(
            Q(userGoalNum=x) & Q(user=current_user)).delete()
        goal = UserGoal(userGoalNum=x, user=current_user,
                        goal=goalNumType, value=0, goalType=z)
        goal.save()
    return HttpResponseRedirect(reverse('account'))


def addstats(user, product, points: int, kg=0):
    """
    Function that calculate point gain from recycle and add it into user point.

    params:
        user - the user object having points added to
        product - the product object which is giving them points
        points - the points being added to the user object
        kg - the kg amount being added to the users stats
    Returns:
        None
    """
    user_stats = Statistic.objects.get(user=user)
    user_stats.points += points
    kg *= 0.09
    kg = round(kg, 3)
    user_stats.curweek = round((user_stats.curweek + kg), 3)  # change field
    user_stats.curmonth = round((user_stats.curmonth + kg), 3)
    user_stats.curyear = round((user_stats.curyear + kg), 3)
    user_stats.carbon = round(((user_stats.carbon + kg)*0.24), 3)
    user_stats.lastRecycle = product
    user_stats.save()  # this will update only


def update_goal_stat(user, product):
    """
    Check and update user goal when user reached the requirement.

    params:
        user - the user who is having their goal updated
        product - the product which the user has recycled.
    """
    material = product.material
    recyclable = product.recycle
    if recyclable:
        bin_type = material
    else:
        bin_type = 'General Waste'
    user_goals = UserGoal.objects.filter(Q(goalType=bin_type) & Q(user=user))
    for item in user_goals:
        item.value += 1
        item.save()
    # Delete full goals and add points
    for item in user_goals:
        if item.value >= 100:
            item.delete()
            user.points += 100


def send_carbon_footprint_email(user):
    """
    This function will email the user after their stats have been reset by the schedular below. They will be email
    info on week, month, year and carbon

    params:
        user - this is the user object which we will be working with and emailing stats to.
    """
    user_stats = Statistic.objects.get(user=user)
    week_data = user_stats.curweek
    month_data = user_stats.curmonth
    year_data = user_stats.curyear
    carbon_data = user_stats.carbon
    html_message = render_to_string('carbon_footprint_email.html', {
                                    'User': user, 'Carbon': carbon_data, 'WeekData': week_data, 'MonthData': month_data, 'YearData': year_data})
    send_mail(
        'Your Carbon Footprint Report',
        '',
        'bytebrigade@outlook.com',
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def reset_week():
    """
    It is the end of the week so we reset all the weekly stats
    """
    for item in Statistic.objects.all():
        send_carbon_footprint_email(item.user)
        item.curweek = 0
        item.save()


def reset_month():
    """
    It is the end of the month potentially, so we reset the monthly stats
    """
    if datetime.datetime.now().day == 1:
        for item in Statistic.objects.all():
            send_carbon_footprint_email(item.user)
            item.curmonth = 0
            item.save()


def reset_year():
    """
    It is the end of the year potentially, so we reset the year stats
    """
    if datetime.datetime.now().month == 1 and datetime.datetime.now().day == 1:
        for item in Statistic.objects.all():
            send_carbon_footprint_email(item.user)
            item.curyear = 0
            item.save()


# Schedule the reset_stats function to run on the last day of each week, month and year  at 00:00 AM
schedule.every().sunday.at("00:00").do(reset_week)
schedule.every().day.at("00:00").do(reset_year)
schedule.every().day.at("00:00").do(reset_month)