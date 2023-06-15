# Generated by Django 4.2.1 on 2023-06-02 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryLeagues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255, verbose_name='Страна')),
                ('name_of_league', models.CharField(max_length=255, verbose_name='Название турнира')),
                ('pars_id', models.IntegerField(verbose_name='id для парсинга')),
            ],
            options={
                'verbose_name': 'Турнир',
                'verbose_name_plural': 'Турниры',
            },
        ),
        migrations.CreateModel(
            name='FootballClubs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('logo', models.ImageField(upload_to='logos/%Y/%m/%d/', verbose_name='Логотип')),
                ('pars_id', models.IntegerField(verbose_name='id для парсинга')),
            ],
            options={
                'verbose_name': 'Футбольный клуб',
                'verbose_name_plural': 'Футбольные клубы',
            },
        ),
        migrations.CreateModel(
            name='TotalTables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.IntegerField(verbose_name='Матчи')),
                ('wins', models.IntegerField(verbose_name='Победы')),
                ('draws', models.IntegerField(verbose_name='Ничьи')),
                ('loses', models.IntegerField(verbose_name='Поражения')),
                ('goals_scored', models.IntegerField(verbose_name='Забито')),
                ('goals_conceded', models.IntegerField(verbose_name='Пропущено')),
                ('goal_difference', models.IntegerField(verbose_name='Разница')),
                ('points', models.IntegerField(verbose_name='Очки')),
                ('name_club', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='topfive.footballclubs', verbose_name='Название клуба')),
            ],
            options={
                'verbose_name': 'Итоговая таблица',
                'verbose_name_plural': 'Итоговые таблицы',
                'ordering': ['-points', '-goal_difference'],
            },
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Сезон')),
                ('start_of_season', models.DateTimeField(verbose_name='Дата начала сезона')),
                ('finish_of_season', models.DateTimeField(verbose_name='Дата окончания сезона')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='topfive.countryleagues', verbose_name='Лига')),
            ],
            options={
                'verbose_name': 'Сезон',
                'verbose_name_plural': 'Сезоны',
            },
        ),
        migrations.CreateModel(
            name='FootballMatches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_match', models.DateTimeField(verbose_name='Дата матча')),
                ('home_goals', models.IntegerField(verbose_name='забито хозяевами')),
                ('guests_goals', models.IntegerField(verbose_name='забито хозяевами')),
                ('guest_club', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='guest_club_set', to='topfive.footballclubs', verbose_name='Название')),
                ('home_club', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_club_set', to='topfive.footballclubs', verbose_name='Название')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='topfive.countryleagues', verbose_name='Лига')),
            ],
            options={
                'verbose_name': 'Матч',
                'verbose_name_plural': 'Матчи',
            },
        ),
    ]
