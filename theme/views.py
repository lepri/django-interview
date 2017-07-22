from datetime import date
from django.shortcuts import render
from operator import itemgetter
from django.views.generic import View
from .models import Video, Comment, Thumb


class PopularThemes(View):

    def get(self, request):
        videos = Video.objects.all()
        videos_list = []
        for video in videos:
            views = video.views
            time_factor = self.get_time_factor(video)
            good_comments = self.get_good_comments(video)
            thumbs_up = self.get_thumbs_up(video)
            positive_factor = 0.7 * good_comments + 0.3 * thumbs_up
            score = views * time_factor * positive_factor
            video_dict = {
                'id': video.id,
                'name': video.title,
                'score': score
            }
            videos_list.append(video_dict)
        videos_list = sorted(videos_list, key=itemgetter('score'), reverse=True)
        params = {'videos': videos_list }
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
