from django.urls import path
from com_goldenthinker_trade_web import views

urlpatterns = [
    path("", views.home),
    path("com_goldenthinker_trade_web/templates/com_goldenthinker_trade_web/[name]", views.com_goldenthinker_trade_web,name=''),

]