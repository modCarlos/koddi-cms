# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='user_cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('wall', models.ImageField(upload_to=b'wall_images')),
                ('author', models.ForeignKey(related_name='author_course', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ForeignKey(related_name='category_course', to='page.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('variant', models.CharField(max_length=255)),
                ('status', models.CharField(default='waiting', max_length=10, choices=[('waiting', 'Waiting for confirmation'), ('preauth', 'Pre-authorized'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('refunded', 'Refunded'), ('error', 'Error'), ('input', 'Input')])),
                ('fraud_status', models.CharField(default='unknown', max_length=10, verbose_name='fraud check', choices=[('unknown', 'Unknown'), ('accept', 'Passed'), ('reject', 'Rejected'), ('review', 'Review')])),
                ('fraud_message', models.TextField(default='', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=255, blank=True)),
                ('currency', models.CharField(max_length=10)),
                ('total', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('delivery', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('tax', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('description', models.TextField(default='', blank=True)),
                ('billing_first_name', models.CharField(max_length=256, blank=True)),
                ('billing_last_name', models.CharField(max_length=256, blank=True)),
                ('billing_address_1', models.CharField(max_length=256, blank=True)),
                ('billing_address_2', models.CharField(max_length=256, blank=True)),
                ('billing_city', models.CharField(max_length=256, blank=True)),
                ('billing_postcode', models.CharField(max_length=256, blank=True)),
                ('billing_country_code', models.CharField(max_length=2, blank=True)),
                ('billing_country_area', models.CharField(max_length=256, blank=True)),
                ('billing_email', models.EmailField(max_length=254, blank=True)),
                ('customer_ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('extra_data', models.TextField(default='', blank=True)),
                ('message', models.TextField(default='', blank=True)),
                ('token', models.CharField(default='', max_length=36, blank=True)),
                ('captured_amount', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('summary', models.CharField(max_length=240)),
                ('content', models.TextField()),
                ('repository', models.URLField(blank=True)),
                ('position', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('wall', models.ImageField(upload_to=b'wall_images')),
                ('author', models.ForeignKey(related_name='author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(related_name='category_post', to='page.Category', null=True)),
                ('course', models.ForeignKey(related_name='course_post', blank=True, to='page.Course', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('twitter', models.CharField(max_length=128, blank=True)),
                ('facebook', models.CharField(max_length=128, blank=True)),
                ('google_plus', models.CharField(max_length=128, blank=True)),
                ('image', models.ImageField(upload_to=b'image')),
                ('facebook_uid', models.PositiveIntegerField(null=True, blank=True)),
                ('facebook_access_token', models.CharField(max_length=255, blank=True)),
                ('facebook_access_token_expires', models.PositiveIntegerField(null=True, blank=True)),
                ('favorites', models.ManyToManyField(related_name='favorites', to='page.Post')),
                ('user', models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='tags_post', to='page.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='cart',
            field=models.ForeignKey(related_name='cart', to='page.Cart'),
        ),
        migrations.AddField(
            model_name='article',
            name='post',
            field=models.ForeignKey(related_name='article', to='page.Post'),
        ),
    ]
