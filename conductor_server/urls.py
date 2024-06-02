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

from agents import views as agent_views
from buckets import views as bucket_views
from chains import views as chains_views
from collect import views as collect_views
from flows import views as flow_views
from search import views as search_views
from reports import views as report_views

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
router.register(r"collect/tasks", collect_views.TaskViewSet, basename="collect-task")
router.register(
    r"collect/url/summarize", collect_views.URLSummaryViewSet, basename="url-summary"
)
router.register(r"chains/tasks", chains_views.TaskViewSet, basename="chains-task")
router.register(
    r"chains/summarize",
    chains_views.SummarizeContentViewSet,
    basename="chains-summarize",
)
router.register(
    r"chains/apollo/input",
    chains_views.ApolloInputChainView,
    basename="chains-apollo-input",
)
router.register(
    r"chains/apollo/context",
    chains_views.ApolloContextChainView,
    basename="chains-apollo-context",
)
router.register(
    r"chains/email/context",
    chains_views.CreateEmailChainView,
    basename="chains-email-from-context",
)
router.register(
    r"reports",
    report_views.ReportViewSet,
    basename="reports",
)
router.register(
    r"reports/paragraphs",
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
    path("agents/", agent_views.MarketEmailCrewViewSet.as_view(), name="agents"),
    path(
        "search/apollo/", search_views.ApolloSearchView.as_view(), name="search_apollo"
    ),
    path(
        "search/discord/",
        search_views.DiscordSearchView.as_view(),
        name="search_discord",
    ),
    path("search/", search_views.PineconeSearchView.as_view(), name="search"),
    path("buckets/", bucket_views.BucketApi.as_view(), name="buckets"),
    path(
        "buckets/object/", bucket_views.BucketObjectApi.as_view(), name="buckets-object"
    ),
    path(
        "buckets/object/latest/",
        bucket_views.BucketObjectLatestView.as_view(),
        name="buckets-object-latest",
    ),
    path(
        "flows/deployments/<str:deployment_id>/",
        flow_views.FlowRunApiView.as_view(),
        name="flow-deployments-create",
    ),
    path(
        "flows/deployments/",
        flow_views.ReadFlowDeploymentsView.as_view(),
        name="flow-deployments-list",
    ),
    path("flows/results/", flow_views.FlowResultView.as_view(), name="flow-results"),
]
