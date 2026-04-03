from django.db import migrations, models

import portfolio_form.models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio_form", "0003_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="dashboard_token",
            field=models.CharField(
                default=portfolio_form.models.generate_dashboard_token,
                editable=False,
                max_length=80,
                unique=True,
            ),
        ),
    ]
