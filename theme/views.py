from datetime import date
from django.shortcuts import render
from operator import itemgetter
from django.views.generic import View
from .models import Video, Comment, Thumb


class PopularThemes(View):

    def get(self, request):
        videos = Video.objects.all()
        themes_list = []
        for video in videos:
            views = video.views
            time_factor = self.get_time_factor(video)
            good_comments = self.get_good_comments(video)
            thumbs_up = self.get_thumbs_up(video)
            positive_factor = (0.7 * good_comments) + (0.3 * thumbs_up)
            score = views * time_factor * positive_factor
            themes = video.themes.values()

            for theme in themes:
                themes_dict = {
                    'id': theme['id'],
                    'name': theme['name'],
                    'score': score
                }
                themes_list.append(themes_dict)

        # temporary list to save the themes list ordered by id
        themes_tmp_list = sorted(themes_list, key=itemgetter('id'),
                                 reverse=False)
        themes_list = []
        theme_dict = {}
        for theme in themes_tmp_list:
            if theme['id'] in theme_dict.values():
                theme_dict['score'] += theme['score']
            elif len(theme_dict) == 0:
                theme_dict['id'] = theme['id']
                theme_dict['name'] = theme['name']
                theme_dict['score'] = theme['score']
            else:
                themes_list.append(theme_dict)
                theme_dict = {'id': theme['id'],
                              'name': theme['name'],
                              'score': theme['score']
                              }
        themes_list.append(theme_dict)

        themes_list = sorted(themes_list, key=itemgetter('score'), reverse=True)
        params = {'themes': themes_list }
        return render(request, 'popular_themes.html', params)

    def get_time_factor(self, video):
        date_uploaded = video.date_uploaded
        delta = date.today() - date_uploaded
        return max(0, 1 - (delta.days/365))

    def get_good_comments(self, video):
        comments = Comment.objects.filter(video=video)
        positive = 0
        negative = 0
        for comment in comments:
            if comment.is_positive:
                positive += 1
            else:
                negative += 1
        try:
            return positive / (positive + negative)
        except ZeroDivisionError:
            return 0.0

    def get_thumbs_up(self, video):
        thumbs = Thumb.objects.filter(video=video)
        positive = 0
        negative = 0
        for thumb in thumbs:
            if thumb.is_positive:
                positive += 1
            else:
                negative += 1
        try:
            return positive / (positive + negative)
        except ZeroDivisionError:
            return 0.0
