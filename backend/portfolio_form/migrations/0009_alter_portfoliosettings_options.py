from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio_form", "0008_remove_user_dashboard_token"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="portfoliosettings",
            options={"verbose_name": "Portfolio", "verbose_name_plural": "Portfolios"},
        ),
    ]
