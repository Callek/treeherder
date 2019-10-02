# -*- coding: utf-8 -*-
# Generated by Django 2.2.4 on 2019-08-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0014_add_job_log_status_skipped_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='tc_root_url',
            field=models.CharField(db_index=True, default='https://taskcluster.net', max_length=255),
            # only apply this default when migrating; after this users must supply their
            # own rootUrl (and by the time you're reading this, `taskcluster.net` is likely
            # no longer operating)
            preserve_default=False,
        ),
    ]