from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0008_auto_20181120_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='groceryitem',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterModelOptions(
            name='groceryitem',
            options={'ordering': ['list_id', 'order', 'pk']},
        ),
    ]
