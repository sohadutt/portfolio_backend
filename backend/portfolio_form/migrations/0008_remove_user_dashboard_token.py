from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio_form", "0007_remove_portfoliosettings_share_token_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="dashboard_token",
        ),
    ]
