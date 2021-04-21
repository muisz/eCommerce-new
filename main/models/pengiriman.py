from django.db import models

class Pengiriman(models.Model):
	name = models.CharField(max_length=100)
	startRange = models.FloatField(default=0)
	endRange = models.FloatField(default=10000)

	class Meta:
		db_table = 'pengiriman'