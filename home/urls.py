from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.search, name='search'),
    path('extract/', views.pdf_extract, name='pdf_extract'),
    path('search/<str:id>', views.detail_putusan, name='detail_putusan'),
    path('view/<str:id>', views.view_pdf, name='view_pdf'),
    path('openpdf/<str:id>/<str:key>', views.open_pdf, name='open_pdf'),
    path('previewpdf/<id>', views.preview_pdf, name='preview_pdf'),
    path('download/<str:id>', views.download_pdf, name='download'),
    # path("dashboard/", views.dashboard, name="dashboard"),
    # path('search_sampel/', views.search_sampel, name='search_sampel'),
    path('select_pdf/<str:id>', views.select_pdf, name="select_pdf"),
    # path('news/', views.news, name='news'),
    path('audittrail/', views.audittrail, name='audittrail')
]
