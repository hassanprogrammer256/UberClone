from django.db import migrations, models


def populate_usernames(apps, schema_editor):
    User = apps.get_model('accounts', 'CustomUser')
    used_usernames = set()

    for user in User.objects.only('pk', 'email').order_by('pk').iterator():
        base_username = user.email.split('@', 1)[0].strip().lower()[:140]
        if not base_username:
            base_username = f'user{user.pk}'

        username = base_username
        suffix = 1
        while username.casefold() in used_usernames:
            username = f'{base_username[:140]}{suffix}'
            suffix += 1

        user.username = username
        user.save(update_fields=['username'])
        used_usernames.add(username.casefold())


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.RunPython(populate_usernames, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
