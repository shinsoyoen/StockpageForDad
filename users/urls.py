from django.contrib import admin
from django.urls import path, include
from users import views  # ✅ 내가 만든 views.py 참조

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('transaction_History.urls')),
    path('delete/<int:trade_id>/', views.delete_trade, name='delete_trade'),
]
