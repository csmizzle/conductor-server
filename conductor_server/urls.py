"""
URL configuration for conductor_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from chains import views as chains_views
from reports import views as report_views
from agents import views as agent_views


api_info = openapi.Info(
    title="Conductor API",
    default_version="v1",
    description="Conductor API for managing agents and workflows",
)

schema_view = get_schema_view(
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"chains/tasks", chains_views.TaskViewSet, basename="chains-task")
router.register(
    r"reports",
    report_views.ReportViewSet,
    basename="reports",
)
router.register(
    r"paragraphs",
    report_views.ParagraphViewSet,
    basename="paragraphs",
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path(
        "generate/<int:report_id>/html/",
        report_views.ReportToHtmlView.as_view(),
        name="generate-html",
    ),
    path(
        "generate/<int:report_id>/pdf/",
        report_views.ReportToPDFView.as_view(),
        name="generate-pdf",
    ),
    path(
        "crews/marketing/report/",
        agent_views.URLMarketingCrewView.as_view(),
        name="marketing-report",
    ),
    path(
        "chains/tasks/<str:task_id>/report/",
        report_views.ReportFromChainTaskIdView.as_view(),
        name="report-from-task",
    ),
    path(
        "query/reports/",
        report_views.GetReportByTitleView.as_view(),
        name="query-reports",
    ),
]
