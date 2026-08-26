from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_alter_notes_id_alter_studynote_id_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='WordCollection',
                ),
            ],
            database_operations=[]
        )
    ]
