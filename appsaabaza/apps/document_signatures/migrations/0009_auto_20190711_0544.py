from django.db import migrations, models

import appsaabaza.apps.document_signatures.models
import appsaabaza.apps.storage.classes


class Migration(migrations.Migration):
    dependencies = [
        ('document_signatures', '0008_auto_20180429_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detachedsignature',
            name='signature_file',
            field=models.FileField(
                blank=True, null=True,
                storage=appsaabaza.apps.storage.classes.FakeStorageSubclass(),
                upload_to=appsaabaza.apps.document_signatures.models.upload_to,
                verbose_name='Signature file'
            ),
        ),
    ]
