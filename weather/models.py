# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

class Country(models.Model):
	country = models.CharField(max_length=20)
	country_code =  models.IntegerField(unique=True)

class Weather(models.Model):
	country_code = models.IntegerField(default=0)
	tag_code =models.CharField(default='NA',max_length=50)
	year = models.IntegerField(default=0)
	january = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	february = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	march = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	april = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	may = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	june = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	july = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	august = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	september = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	october = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	november = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	december = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	winter = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	spring = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	summer = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	autumn = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	annual = models.DecimalField(default=0,max_digits=9, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)

	