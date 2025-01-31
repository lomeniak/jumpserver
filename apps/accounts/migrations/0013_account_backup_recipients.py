# Generated by Django 4.1.10 on 2023-08-03 08:28

from django.conf import settings
from django.db import migrations, models


def migrate_recipients(apps, schema_editor):
    account_backup_model = apps.get_model('accounts', 'AccountBackupAutomation')
    execution_model = apps.get_model('accounts', 'AccountBackupExecution')
    for account_backup in account_backup_model.objects.all():
        recipients = list(account_backup.recipients.all())
        if not recipients:
            continue
        account_backup.recipients_part_one.set(recipients)

    execution_bojs = []
    for execution in execution_model.objects.all():
        snapshot = execution.snapshot
        recipients = snapshot.pop('recipients', {})
        snapshot.update({'recipients_part_one': recipients, 'recipients_part_two': {}})
        execution_bojs.append(execution)
    execution_model.objects.bulk_update(execution_bojs, ['snapshot'])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0012_auto_20230621_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountbackupautomation',
            name='recipients_part_one',
            field=models.ManyToManyField(
                blank=True, related_name='recipient_part_one_plans',
                to=settings.AUTH_USER_MODEL, verbose_name='Recipient part one'
            ),
        ),
        migrations.AddField(
            model_name='accountbackupautomation',
            name='recipients_part_two',
            field=models.ManyToManyField(
                blank=True, related_name='recipient_part_two_plans',
                to=settings.AUTH_USER_MODEL, verbose_name='Recipient part two'
            ),
        ),
        migrations.RenameField(
            model_name='accountbackupexecution',
            old_name='plan_snapshot',
            new_name='snapshot',
        ),
        migrations.RunPython(migrate_recipients),
        migrations.RemoveField(
            model_name='accountbackupautomation',
            name='recipients',
        ),

    ]
