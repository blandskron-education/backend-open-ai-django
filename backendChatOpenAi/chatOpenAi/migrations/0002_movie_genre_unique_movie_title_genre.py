# Generated manually to keep the educational model and migration in sync.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatOpenAi", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="genre",
            field=models.CharField(default="Sin clasificar", max_length=100),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="movie",
            constraint=models.UniqueConstraint(
                fields=("title", "genre"), name="unique_movie_title_genre"
            ),
        ),
        migrations.AlterModelOptions(
            name="movie",
            options={"ordering": ["title", "genre"]},
        ),
    ]
