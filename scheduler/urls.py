from django.urls import path
from .views import deleteSavedPost, getSavedPosts, addSavedPost, addPlannedPosts, getPlannedPosts, getAvailableGroups, addAvailableGroup, deleteAvailableGroup, deletePlannedPost
# urlpatterns = [path('api/vkUserPermissions',
#                     getPermissions, name='vkUserPermissions')]
urlpatterns = [path('scheduler/api/getPlannedPosts',
                    getPlannedPosts, name='getPlannedPosts'),
               path('scheduler/api/getAvailableGroups',
                    getAvailableGroups, name='getAvailableGroups'),
               path('scheduler/api/addAvailableGroup',
                    addAvailableGroup, name='addAvailableGroup'),
               path('scheduler/api/deleteAvailableGroup',
                    deleteAvailableGroup, name='deleteAvailableGroup'),
               path('scheduler/api/deletePlannedPost',
                    deletePlannedPost, name='deletePlannedPost'),

               path('scheduler/api/addPlannedPost',
                    addPlannedPosts, name='addPlannedPosts'),
               path('scheduler/api/addSavedPost',
                    addSavedPost, name='addSavedPost'),
               path('scheduler/api/getSavedPosts',
                    getSavedPosts, name='getSavedPosts'),
               path('scheduler/api/deleteSavedPost',
                    deleteSavedPost, name='deleteSavedPost'),
               ]
