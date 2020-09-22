from django.shortcuts import render, redirect

def schedulerView(request):
    data = {}
    return render(request, 'scheduler.html', data)

def checkTask(request, id, week=""):
    rUrl = '/#' + week if week != "" else '/'
    return redirect(rUrl)