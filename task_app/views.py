from django.shortcuts import render, redirect

from datetime import datetime, date, timedelta
from functools import reduce
from django.utils.dateformat import DateFormat
from django.utils import timezone
from django.utils.formats import get_format
from .forms import CategoryForm, TaskForm

from .models import Task, Category

def monday(date):
    """ 
    Get the monday from a Date
    args:
        date (Date): Date to get monday
    return:
        Date: The monday
    """   
    return date - timedelta(days=date.weekday())

def taskInfo(task):
    """ 
    Task info to display
    args:
        task (Task): Task to store
    return:
        Dictionary: dictionary containing the task information
    """   
    df = DateFormat(task.date.astimezone(timezone.get_current_timezone()))
    
    htmlInfo = {
        "icon": task.category.icon,
        "color": task.category.color,
        "h": "h"+df.format("H")
    }
    tInfo = {
        "id": task.id,
        "title": task.title,
        "category": task.category.name,
        "description": task.description,
        "date": df.format("l b d Y - H:i"),
        "complete": task.complete,
        "htmlInfo": htmlInfo
    }
    return tInfo

def reduceTasks(accumulator, task):
    """ 
    stores the tasks in the dictionary created by createWeeks(startMonday, numWeeks)
    args:
        accumulator (Dict): Dictionary to store the task
        task (Task): Task to store
    return:
        Dictionary: Task grouped by hours, days and weeks
    """
    tInfo = taskInfo(task)
    taskDate = task.date.astimezone(timezone.get_current_timezone())
    hourInfo = DateFormat(monday(taskDate)).format("b d Y")
    hours = accumulator[hourInfo]["week"][taskDate.weekday()]["hours"]
    if tInfo["htmlInfo"]["h"] in hours:
        hours[tInfo["htmlInfo"]["h"]].append(tInfo)
    else:
        accumulator[hourInfo]["week"][taskDate.weekday()]["hours"][tInfo["htmlInfo"]["h"]] =  [tInfo]

    return accumulator

def createWeeks(startMonday, numWeeks):
    """ 
    create a dictionary to group days by weeks from a start date to a number of weeks
    args:
        startMonday (date): First date
        numWeeks (int): Number of weeks
    return:
        Dictionary: Days grouped by weeks
    """
    w = 0
    monday = startMonday
    weeks = {}
    while w <= numWeeks:
        name = "Semana actual" if w == 0 else "Semana " + str(w+1)
        wid =  "week" + str(w+1)
        weekInfo = {"week": {}, "name":name, "index": w, "id":wid}
        for r in range(7):
            day = (monday + timedelta(days=r))
            df = DateFormat(day)
            weekInfo["week"][r] = {"hours":{}, "weekday":r, "name":df.format("D"), "date":df.format("b/d")}

        weeks[DateFormat(monday).format("b d Y")] = weekInfo
        monday = (monday + timedelta(days=7))
        w += 1
    return weeks

def schedulerView(request):
    """ Task Scheduler View """
    data = {}
    data['hours'] = map(lambda x: {'h': x if x > 9 else '0'+str(x), 'i': x+3}, range(24))
    
    now = datetime.now()
    today = date.today()
    iDate = today - timedelta(days=today.weekday())
    tasksList = Task.objects.filter(date__gte=iDate).order_by('date')

    firstTask = tasksList.first()
    lastTask = tasksList.last()
    weeks = (1 + ( monday(lastTask.date) - monday(firstTask.date)).days) / 7 if tasksList.count() > 0 and (firstTask.id != lastTask) else 0

    weeksInfo = createWeeks(monday(firstTask.date), weeks) if tasksList.count() > 0 else createWeeks(monday(today), weeks)
    
    tasks = reduce(reduceTasks, tasksList, weeksInfo)
    data["weeks"] = tasks
    data['datetext'] = DateFormat(now).format("l b d Y")


    summary = {}
    summary["complete"] = Task.objects.filter(complete=True).count()
    summary["pending"] = Task.objects.filter(date__gte=iDate).filter(complete=False).count()
    summary["lost"] = Task.objects.filter(date__lt=iDate).filter(complete=False).count()
    data["summary"] = summary

    data["forms"] = {
        "newTask": TaskForm(),
        "newCategory": CategoryForm()
    }

    data["categories"] = Category.objects.all()
    return render(request, 'scheduler.html', data)

def checkTask(request, id, week=""):
    """ 
    Change the completion status of a task 
    args:
        id (int): Task id
        week (slug): Task week. ex: week2
    return:
        HttpResponseRedirect: redirect to  task scheluder view 
    """
    task = Task.objects.get(id=id)
    task.complete = not task.complete
    task.save()
    rUrl = '/#' + week if week != "" else '/'
    return redirect(rUrl)

def newTask(request):
    if request.method == "POST": 
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("/")

def newCategory(request):
    if request.method == "POST": 
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("/")