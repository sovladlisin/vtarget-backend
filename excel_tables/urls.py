from django.urls import path
from .views import updateExcelTable, uploadExcelTable, getExcelTables, deleteExcelTable, getExcelTable

urlpatterns = [
    path('excel_tables/api/updateExcelTable',
         updateExcelTable, name='updateExcelTable'),
    path('excel_tables/api/uploadExcelTable',
         uploadExcelTable, name='uploadExcelTable'),
    path('excel_tables/api/getExcelTables',
         getExcelTables, name='getExcelTables'),
    path('excel_tables/api/deleteExcelTable',
         deleteExcelTable, name='deleteExcelTable'),
    path('excel_tables/api/getExcelTable',
         getExcelTable, name='getExcelTable'),
]
