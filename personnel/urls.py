from django.urls import path

from .views import DepartmentView, PersonnelView, PersonnelDetailView, DepartmentDetailView, DepartmentDetail

urlpatterns = [
    path("department/", DepartmentView.as_view()),
    path("personnel/", PersonnelView.as_view()),
    path("personnel/<int:pk>/", PersonnelDetailView.as_view()),
    # path("department/<str:department>/", DepartmentDetail.as_view()),  # We created it to be able to write dynamic endpoints
    path("department/<str:name>/", DepartmentDetailView.as_view()),  # We created it to be able to write dynamic endpoints
]
