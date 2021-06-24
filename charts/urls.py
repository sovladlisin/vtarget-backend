from django.urls import path
from .views import updateMedal, assignMedalToUser, removeMedalFromUser, getMedals
from .cabinets_view import getCabinets, createCabinet, deleteCabinet, updateCabinet, getCabinet
from .charts_view import getCharts, createChart, deleteChart, updateChart
from .tables_view import getTables, createTable, deleteTable, updateTable

# urlpatterns = [path('api/vkUserPermissions',
#                     getPermissions, name='vkUserPermissions')]
urlpatterns = [path('charts/updateMedal',
                    updateMedal, name='updateMedal'),

               path('charts/assignMedalToUser',
                    assignMedalToUser, name='assignMedalToUser'),
               path('charts/removeMedalFromUser',
                    removeMedalFromUser, name='removeMedalFromUser'),
               path('charts/getMedals',
                    getMedals, name='getMedals'),

               path('charts/getCabinets',
                    getCabinets, name='getCabinets'),
               path('charts/getCabinet',
                    getCabinet, name='getCabinet'),
               path('charts/createCabinet',
                    createCabinet, name='createCabinet'),
               path('charts/deleteCabinet',
                    deleteCabinet, name='deleteCabinet'),
               path('charts/updateCabinet',
                    updateCabinet, name='updateCabinet'),

               path('charts/getCharts',
                    getCharts, name='getCharts'),
               path('charts/createChart',
                    createChart, name='createChart'),
               path('charts/deleteChart',
                    deleteChart, name='deleteChart'),
               path('charts/updateChart',
                    updateChart, name='updateChart'),

               path('charts/getTables',
                    getTables, name='getTables'),
               path('charts/createTable',
                    createTable, name='createTable'),
               path('charts/deleteTable',
                    deleteTable, name='deleteTable'),
               path('charts/updateTable',
                    updateTable, name='updateTable'),
               ]
