from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general', '0009_delete_wordcollection'),
    ]

    operations = [
        migrations.CreateModel(
            name='VocabularyExamResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='Score')),
                ('total_questions', models.IntegerField(default=10, verbose_name='Total Questions')),
                ('percentage', models.FloatField(default=0.0, verbose_name='Percentage')),
                ('mode', models.CharField(choices=[('en_to_bn', 'English to Bengali'), ('bn_to_en', 'Bengali to English'), ('mixed', 'Mixed Practice')], default='en_to_bn', max_length=20, verbose_name='Mode')),
                ('details', models.JSONField(blank=True, default=dict, verbose_name='Exam Breakdown')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date Taken')),
            ],
            options={
                'verbose_name': 'Vocabulary Exam Result',
                'verbose_name_plural': 'Vocabulary Exam Results',
                'ordering': ['-created_at'],
            },
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='WordCollection',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('english', models.CharField(max_length=255, unique=True, verbose_name='English Word')),
                        ('bengali', models.CharField(blank=True, max_length=255, verbose_name='Bengali Meaning')),
                        ('status', models.CharField(choices=[('new', 'New'), ('familiar', 'Familiar'), ('unfamiliar', 'Unfamiliar'), ('confident', 'Confident')], default='new', max_length=20, verbose_name='Status')),
                        ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                        ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                    ],
                    options={
                        'verbose_name': 'Word Collection',
                        'verbose_name_plural': 'Word Collections',
                        'db_table': 'general_wordcollection',
                        'ordering': ['-created_at'],
                    },
                ),
            ],
            database_operations=[]
        ),
    ]
