from django.conf.urls import url
from .views import IndexView, Index_layoutView, GraphShowView, CompareView
from .views import DownloadAsExcelView

urlpatterns = [
    url('^index_layout$', Index_layoutView.as_view(), name='index_layout'),
    url('^index/$', IndexView.as_view(), name='index'),
    url('^graph/$', GraphShowView.as_view(), name='graph'),
    url('^compare/$', CompareView.as_view(), name='compare'),
    url('^download_csv/', DownloadAsExcelView.as_view(), name='down_csv')
]
