import django.core.files.storage
from django.db import migrations, models

import appsaabaza.apps.document_signatures.models


class Migration(migrations.Migration):
    dependencies = [
        ('document_signatures', '0006_auto_20160326_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detachedsignature',
            name='signature_file',
            field=models.FileField(
                blank=True, null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location=b'appsaabaza/media/document_storage'
                ), upload_to=appsaabaza.apps.document_signatures.models.upload_to,
                verbose_name='Signature file'
            ),
        ),
    ]
