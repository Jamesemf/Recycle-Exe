from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .models import Statistic, Goal, UserGoal
from home.models import Transaction
from django.urls import reverse
from django.db.models import Q


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

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
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def account(request):
    if request.user.is_authenticated:
        data = Statistic.objects.get(user=request.user)
        lastTransaction = 0
        if Transaction.objects.filter(user=request.user).exists():
            lastTransaction = Transaction.objects.filter(user=request.user).latest('time')


        maxWeek = Statistic.objects.all().order_by('-curweek')[0]
        maxMonth = Statistic.objects.all().order_by('-curmonth')[0]
        maxYear = Statistic.objects.all().order_by('-curyear')[0]
        goalData = Goal.objects.all()
        userGoal1 = UserGoal.objects.filter(Q(userGoalNum=1) & Q(user=request.user)).first()
        userGoal2 = UserGoal.objects.filter(Q(userGoalNum=2) & Q(user=request.user)).first()
        userGoal3 = UserGoal.objects.filter(Q(userGoalNum=3) & Q(user=request.user)).first()
        data_dict = {
            'Profile': data,
            'maxWeek': maxWeek,
            'maxMonth': maxMonth,
            'maxYear': maxYear,
            'Goals': goalData,
            'UserGoal1': userGoal1,
            'UserGoal2': userGoal2,
            'UserGoal3': userGoal3,
            'lastTrans': lastTransaction
        }
        return render(request, 'account/Profile_page.html', data_dict)
    else:
        return redirect('login')

def password(request):
    return render(request, 'account/password.html')

def addUserGoal(request):
    x = request.POST['goalNum']
    y = request.POST['goal-options']
    z = request.POST['goal-type'] # this is plastic and all the others
    goalNumType = Goal.objects.get(pk=y)
    current_user = request.user

    # Checking if the user has already got a goal for this specific value
    goalSet = UserGoal.objects.filter(Q(userGoalNum=x) & Q(user=current_user))
    if not goalSet:
        goal = UserGoal(userGoalNum = x, user = current_user, goal = goalNumType, value = 0, goalType = z)
        goal.save()
    else:
        UserGoal.objects.filter(Q(userGoalNum=x) & Q(user=current_user)).delete()
        goal = UserGoal(userGoalNum = x, user = current_user, goal = goalNumType, value = 0, goalType = z)
        goal.save()
    
    return HttpResponseRedirect(reverse('account'))


def addstats(user, product, points: int, kg=0):
    print("In add stats")
    user_stats = Statistic.objects.get(user=user)
    user_stats.points += points
    kg *= 0.09
    kg = round(kg, 3)
    user_stats.curweek = round((user_stats.curweek + kg), 3)  # change field
    user_stats.curmonth = round((user_stats.curmonth + kg), 3)
    user_stats.curyear = round((user_stats.curyear + kg), 3)
    user_stats.lastRecycle = product
    user_stats.save()  # this will update only


def update_goal_stat(user, product):
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

