# Generated by Django 3.1.7 on 2021-03-27 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('counter', '0014_auto_20210327_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('sum_for_worker', models.IntegerField(blank=True, null=True)),
                ('date_add', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Оказаная услуга',
                'verbose_name_plural': 'Оказанные услуги',
            },
        ),
        migrations.AddField(
            model_name='typeofwork',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Services',
        ),
        migrations.AddField(
            model_name='serviceslist',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counter.typeofwork'),
        ),
        migrations.AddField(
            model_name='serviceslist',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]