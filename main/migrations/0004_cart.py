# Generated by Django 2.2 on 2021-04-21 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210417_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=1)),
                ('varian', models.TextField(null=True)),
                ('price', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]