from django.urls import path
from .views import  (home, add_product, add_category, add_sale,add_staff,
                    list_staff,list_user,view_attendance,mark_check_in,
                    mark_check_out,staff_detail , plot_cumulative_sales,
                    mark_user_attendance,
                    list_sales,)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home,name='home'),
    
    path('add_p/', add_product, name='add_p'),
    path('add_cat/', add_category, name='add_cat'),
   
    path('add_sale/', add_sale, name='add_sale'),
    path('add_staff/', add_staff, name='add_staff'),
    path('list_staff/', list_staff, name='list_staff'),
    path('list_user/', list_user, name='list_user'),
    path('staff_detail/<int:staff_id>/', staff_detail, name='staff_detail'),
    path('plot_cumulative_sales/', plot_cumulative_sales, name='plot_cumulative_sales'),
    path('list_sale/', list_sales, name='list_sale'),
    #path('view_loans/', view_loans, name='view_loans'),
    #path('view_credits/', view_credits, name='view_credits'),
    #path('sale_credit/', sale_credit, name='sale_credit'),
    path('mark_check_in/<int:staff_id>/', mark_check_in, name='mark_check_in'),
    path('mark_check_out/<int:staff_id>/', mark_check_out, name='mark_check_out'),
    path('view_attendance/', view_attendance, name='view_attendance'),
    path('mark_user_attendance/', mark_user_attendance, name='mark_user_attendance'),
    #path('create_credit_sale/', create_credit_sale, name='create_credit_sale'),
     #path('credit_sales_list/', list_credit_sales, name='credit_sales_list'),
    # Add
    # Add other URLs as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




