from django.shortcuts import render
from django.views.generic import View
from utils.user_utils import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import collections
import datetime
import time
from django.utils.timezone import now, timedelta
from scrapy_app.models import SuggestionModel
from scrapy_app.models import NeedTitleModel
from scrapy_app.models import NewsModel
from scrapy_app.models import MotionModel
from scrapy_app.models import OfflineWord2vecModel
import csv
from django.http import HttpResponse


def page_not_fount(request):
    """404 page
    """
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def error500(request):
    """500 page
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


class Index_layoutView(LoginRequiredMixin, View):
    """This web use structure in web pages and this view return the structure
    """

    def get(self, request):
        user = request.user
        need_title = NeedTitleModel.objects.all().values_list("key_words", flat=True)
        return render(request, 'index_layout.html', {
            'user': user,
            'need_title': need_title,
        })


class IndexView(LoginRequiredMixin, View):
    """Index web page and it is in a structure and add key words
    """

    def get(self, request):
        need_title = NeedTitleModel.objects.all()
        return render(request, 'index.html', {
            'need_title': need_title,
            'user': request.user,
        })

    def post(self, request):
        """User create a new key words and this method add it to the database
        """
        key_words = request.POST.get('key_words', '')
        key_words = "".join(key_words.split())
        del_key_words = request.POST.get('title_del', '')
        if key_words:
            need_title = NeedTitleModel.objects.all()
            contain_key = NeedTitleModel.objects.filter(key_words=key_words)
            if contain_key:
                return render(request, 'index.html', {
                    'msg_bad': "关键词已存在",
                    'need_title': need_title,
                    'user': request.user,
                })
            new_title = NeedTitleModel()
            new_title.add_user = request.user.username
            new_title.key_words = key_words
            new_title.save()
            return render(request, 'index.html', {
                'msg_good': "添加成功 : " + key_words,
                'need_title': need_title,
                'user': request.user,
            })
        elif del_key_words:
            title = NeedTitleModel.objects.get(key_words=del_key_words)
            title_name = title.key_words
            title.delete()
            need_title = NeedTitleModel.objects.all()
            return render(request, 'index.html', {
                'msg_good': "删除成功 : " + title_name,
                'need_title': need_title,
                'user': request.user,
            })
        need_title = NeedTitleModel.objects.all()
        return render(request, 'index.html', {
            'msg_bad': "添加失败",
            'need_title': need_title,
            'user': request.user,
        })


class GraphShowView(LoginRequiredMixin, View):
    """Get graph of a key word , contain some plane to describe the key word.
    :return title: topic
    :return frequency: count the word frequency from the news related to this topic
    :return motion_tup: the mood of the title
    :return recommend: relative words
    :return time_want: select time of graph
    :return suggests_list: some recommended suggest
    """

    def get(self, request):
        # use TF-IDF get relative words
        # 'title' is primary_key in need_title_model
        title = request.GET.get('title', '')
        # check if title in new_title
        really_need = NeedTitleModel.objects.filter(key_words=title)
        if not really_need:
            return page_not_fount(request)
        time_interval = request.GET.get('time_interval', '')
        if not title:
            return HttpResponseRedirect(reverse('backms:index'))
        time_want = ""
        # get last 30 days motion on default
        if time_interval:
            time_want = time_interval
            time_interval = time_interval.replace(' ', '').split('-')
            title_keys = NewsModel.objects.filter(key_words__contains=title).filter(time__range=(
                datetime.date(int(time_interval[0]), int(time_interval[1]), int(time_interval[2])),
                datetime.date(int(time_interval[3]), int(time_interval[4]), int(time_interval[5]))
            )).values_list("title_key", flat=True)
            title_motions = MotionModel.objects.filter(title=title).filter(date_time__range=(
                datetime.date(int(time_interval[0]), int(time_interval[1]), int(time_interval[2])),
                datetime.date(int(time_interval[3]), int(time_interval[4]), int(time_interval[5]))
            )).order_by('date_time').values_list("positive_rate", "date_time").all()
        else:
            title_keys = NewsModel.objects.filter(key_words__contains=title).filter(
                time__gte=now().date() + timedelta(days=-90)
            ).values_list("title_key", flat=True)
            title_motions = MotionModel.objects.filter(title=title).filter(
                date_time__gte=now().date() + timedelta(days=-90)
            ).order_by('date_time').values_list("positive_rate", "date_time").all()
        # Offline Word2Vec
        relative_content = OfflineWord2vecModel.objects.filter(key1=title).values_list("key2", flat=True)
        relative_content = relative_content[:10]
        # get suggests of this title
        suggestion_model = SuggestionModel.objects.filter(title__contains=title).values_list('suggestion', flat=True)
        suggests_list = []
        for suggestions in suggestion_model:
            suggest_list = suggestions.split(';')
            for suggest in suggest_list:
                suggests_list.append(suggest)
                if suggests_list.__len__() > 11:
                    break
        if title_keys:
            # word2vec have this title
            keys = ""
            for one_keys in title_keys:
                keys += one_keys
            keys = keys.replace("," + title + ",", ",")
            # TF-IDF and collection of all key_words of this title has complete
            frequency_s = collections.Counter(keys.split(",")).most_common(10)
            motion_tup = []
            for motion in title_motions:
                pos_rat = motion[0]
                this_time = datetime.datetime.strptime(str(motion[1]), '%Y-%m-%d')
                this_time = time.mktime(this_time.timetuple())
                motion_tup.append([this_time * 1000, pos_rat])
            return render(request, 'graph_flot.html', {
                'title': title,
                'frequency_s': frequency_s,
                'motion_tup': motion_tup,
                'recommend_words': relative_content,
                'time_want': time_want,
                'suggests_list': suggests_list,
            })
        else:
            # cant get words from offlineWord2vecModel of the database
            return render(request, 'graph_flot.html', {
                'title': title,
                'recommend_words': relative_content,
            })


class CompareView(LoginRequiredMixin, View):
    """ Analyze multi key words at one time
    """

    def get(self, request):
        compare_titles = request.GET.getlist("compare_check_box")
        motion_list = []
        time_compare_titles = ''
        for title in compare_titles:
            time_compare_titles += (title + ',')
            title_motions = MotionModel.objects.filter(title=title).order_by('date_time').values_list(
                "positive_rate",
                "date_time").all()
            motion_tup = []
            for motion in title_motions:
                pos_rat = motion[0]
                this_time = datetime.datetime.strptime(str(motion[1]), '%Y-%m-%d')
                this_time = time.mktime(this_time.timetuple())
                motion_tup.append([this_time * 1000, pos_rat])
            motion_list.append(motion_tup)
        return render(request, 'compare_graph_flot.html', {
            'time_compare_titles': time_compare_titles,
            'compare_titles': compare_titles,
            'motion_list': motion_list,
        })

    def post(self, request):
        time_interval = request.POST.get('time_interval', '')
        # get last 30 days motion on default
        if time_interval:
            time_interval = time_interval.replace(' ', '').split('-')
        motion_list = []
        time_compare_titles = request.POST.get("time_compare_titles", '')
        compare_titles = time_compare_titles.split(',')[:-1]
        for title in compare_titles:
            if not title:
                continue
            title_motions = MotionModel.objects.filter(title=title).filter(date_time__range=(
                datetime.date(int(time_interval[0]), int(time_interval[1]), int(time_interval[2])),
                datetime.date(int(time_interval[3]), int(time_interval[4]), int(time_interval[5]))
            )).order_by('date_time').values_list(
                "positive_rate",
                "date_time").all()
            motion_tup = []
            for motion in title_motions:
                pos_rat = motion[0]
                this_time = datetime.datetime.strptime(str(motion[1]), '%Y-%m-%d')
                this_time = time.mktime(this_time.timetuple())
                motion_tup.append([this_time * 1000, pos_rat])
            motion_list.append(motion_tup)
        return render(request, 'compare_graph_flot.html', {
            'time_compare_titles': time_compare_titles,
            'compare_titles': compare_titles,
            'motion_list': motion_list,
        })


class DownloadAsExcelView(LoginRequiredMixin, View):
    """ Download data as excel
    """

    def get(self, request):
        title = request.GET.get('title', '')
        time_interval = request.GET.get('time_interval', '')
        if time_interval:
            time_interval = time_interval.replace(' ', '').split('-')
            news_detail_list = NewsModel.objects.filter(key_words__contains=title).filter(time__range=(
                datetime.date(int(time_interval[0]), int(time_interval[1]), int(time_interval[2])),
                datetime.date(int(time_interval[3]), int(time_interval[4]), int(time_interval[5]))
            )).values_list("url", "title_key", "motion", "time")
        else:
            news_detail_list = NewsModel.objects.filter(key_words__contains=title).filter(
                time__gte=now().date() + timedelta(days=-90)
            ).values_list("url", "title_key", "motion", "time")
        if news_detail_list:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="users.csv"'
            writer = csv.writer(response)
            writer.writerow(['url', '新闻关键词', '情感', 'time'])
            for detail in news_detail_list:
                writer.writerow([detail[0], detail[1], detail[2], detail[3]])
            return response
        else:
            return page_not_fount(request)
