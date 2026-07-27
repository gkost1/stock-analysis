import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("simulations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="study",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="portfolio",
                to="simulations.study",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="portfolio",
            name="initial_investment",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="portfolioholdings",
            name="cost_per_share",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="portfolioholdings",
            name="date_purchased",
            field=models.DateField(default="2026-01-01"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="portfolioholdings",
            name="date_sold",
            field=models.DateField(blank=True, null=True),
        ),
    ]
