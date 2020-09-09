from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0011_auto_20180917_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadatatype',
            name='parser',
            field=models.CharField(
                blank=True, choices=[
                    (
                        'appsaabaza.apps.metadata.parsers.DateAndTimeParser',
                        'appsaabaza.apps.metadata.parsers.DateAndTimeParser'
                    ), (
                        'appsaabaza.apps.metadata.parsers.DateParser',
                        'appsaabaza.apps.metadata.parsers.DateParser'
                    ), (
                        'appsaabaza.apps.metadata.parsers.TimeParser',
                        'appsaabaza.apps.metadata.parsers.TimeParser'
                    )
                ], help_text='The parser will reformat the value entered to '
                'conform to the expected format.', max_length=64,
                verbose_name='Parser'
            ),
        ),
        migrations.AlterField(
            model_name='metadatatype',
            name='validation',
            field=models.CharField(
                blank=True, choices=[
                    (
                        'appsaabaza.apps.metadata.validators.DateAndTimeValidator',
                        'appsaabaza.apps.metadata.validators.DateAndTimeValidator'
                    ), (
                        'appsaabaza.apps.metadata.validators.DateValidator',
                        'appsaabaza.apps.metadata.validators.DateValidator'
                    ), (
                        'appsaabaza.apps.metadata.validators.TimeValidator',
                        'appsaabaza.apps.metadata.validators.TimeValidator'
                    )
                ], help_text='The validator will reject data entry if the '
                'value entered does not conform to the expected format.',
                max_length=64, verbose_name='Validator'
            ),
        ),
    ]
