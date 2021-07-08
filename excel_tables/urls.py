from django.urls import path
from .views import updateExcelTable, uploadExcelTable, getExcelTables, deleteExcelTable

urlpatterns = [
    path('excel_tables/api/updateExcelTable',
         updateExcelTable, name='updateExcelTable'),
    path('excel_tables/api/uploadExcelTable',
         uploadExcelTable, name='uploadExcelTable'),
    path('excel_tables/api/getExcelTables',
         getExcelTables, name='getExcelTables'),
    path('excel_tables/api/deleteExcelTable',
         deleteExcelTable, name='deleteExcelTable'),
]
