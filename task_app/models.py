from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    color = models.CharField('Hex color',max_length=7)
    icon = models.CharField('Material Design Icon code',max_length=30)

    def __str__(self):
        return str(self.id) + ': ' + self.name

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ': ' + self.title