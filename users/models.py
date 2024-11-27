from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    email = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id',]
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'