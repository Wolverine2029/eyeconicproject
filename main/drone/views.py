from django.shortcuts import render, redirect
from .models import RegisteredUsers, UnRegisteredUsers, tickets
# Create your views here.
from django.shortcuts import render

def Users_List(request):
    users = RegisteredUsers.objects.all()
    unReg = UnRegisteredUsers.objects.all()
    issueTicket = True
    licenseNum = request.POST.get("license")
    print(licenseNum)
    message = "Car is not registed with UMKC. Issue Ticket?"
    for usr in users:
        print("Entered for")
        if usr.license == licenseNum:
            print("Entered IF")
            message = "Car is registered at UMKC"
            issueTicket = False
        else:
            for unreg in unReg:
                print("Entered UnReg for")
                if unreg.license == licenseNum:
                    print("Entered Unreg IF")
                    message = "Car is Unregistered. Issue Ticket?"

    print(message)
    context = {
        'users': users,
        'unreg': unReg,
        'message' : message,
        'issueTicket' : issueTicket,
    }
    return render(request, 'drone/list.html' ,context)

def issueTicket(request):
    licenseNum = request.POST.get("license")
    ticks = tickets.objects.all()
    for i in ticks:
        if i == licenseNum:
            message = "Ticket Already Issued."
    new_ticket = tickets(license=request.POST.get('license'))
    new_ticket.save()
    context = {
        'message': "Issued Ticket Successfully",
    }
    return render(request, 'drone/list.html' ,context)


def check_user(request):
    if 'license' in request.POST:
        pass
    # do somethings
    users = RegisteredUsers.objects.all()
    context = {
        'users': users,
    }

    return render(request, context)


def create_user(request):
    return render(request, 'drone/create.html', context)


def delete_user(request, pk):
    return render(request, 'drone/delete.html', context)


def edit_user(request, pk):
    return render(request, 'drone/update.html', context)