from django.db import models


from django.contrib.auth.models import AbstractUser, Group, Permission


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from courses.models import CommonFields

class CustomUser(AbstractUser,CommonFields):
    USER_TYPE_CHOICES = (
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Changed related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Changed related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

    


class Market_User(models.Model):
    GENDER_CHOICES = [
        ('Male', 'M'),
        ('Female', 'F'),
        ('Other', 'O'),
    ]
    
    AGE_GROUP_CHOICES = [
        ('AGE GROUP 3-4', 'aGE GROUP 3-4'),
        ('AGE GROUP 4-5', 'aGE GROUP 3-4'),
        ('AGE GROUP 5-6', 'aGE GROUP 3-4'),
    
    ]
    
    SUBSCRIPTION_TYPES = [
        ('one years', 'One years'),
        ('six month', 'Six month'),
        ('three month', 'Three month'),
        
    ]
    
    name = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=230,null=True, blank=True)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=18, choices=AGE_GROUP_CHOICES)
    subscription = models.CharField(max_length=255, choices=SUBSCRIPTION_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Ensure max_digits and decimal_places are set
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

    def calculate_price(self):
        base_price = 10.00
        age_group_additional = {
            'AGE GROUP 3-4': 0.00,
            'AGE GROUP 4-5': 20.00,
            'AGE GROUP 5-6': 50.00
        }
        return base_price + age_group_additional.get(self.age_group, 0.00)

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.calculate_price()
        super().save(*args, **kwargs)



        