from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, UserProfile

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'consumer/dashboard.html', {'user_profile': user_profile, 'transactions': transactions})

@login_required
def deposit(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.balance += amount
        user_profile.save()
        transactions = Transaction.objects.create(user=request.user, amount=amount)
        return redirect('dashboard')
    else:
        return render(request, 'consumer/deposit.html')

@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        user_profile = UserProfile.objects.get(user=request.user)
        if amount <= user_profile.balance:
            user_profile.balance -= amount
            user_profile.save()
            transactions = Transaction.objects.create(user=request.user, amount=-amount)
            return redirect('dashboard')
        else:
            error_message = "Insufficient funds"
            return render(request, 'consumer/withdraw.html', {'error_message': error_message})
    else:
        return render(request, 'consumer/withdraw.html')

