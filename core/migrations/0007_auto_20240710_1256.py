# Generated by Django 3.2.25 on 2024-07-10 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20240710_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='grad_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='membership',
            constraint=models.UniqueConstraint(fields=('user', 'organization'), name='core_membership_user_organization'),
        ),
        migrations.AddField(
            model_name='organizationlink',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='core.organization'),
        ),
    ]
