from .models import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        ]


class DataMixin:
    """Общий класс для всех вьюшек"""

    def get_user_context(self, **kwargs):
        context = kwargs
        list_of_leagues = Seasons.objects.filter(name='2022/2023')
        context['menu'] = menu
        context['list_of_leagues'] = list_of_leagues
        return context
