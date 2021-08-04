from django.conf.urls import url
from managers.view.planner import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', PlannerAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', PlannerAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', PlannerModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', PlannerModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', PlannerEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', PlannerEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', PlannerWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', PlannerWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', PlannerWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', PlannerWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', PlannerWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', PlannerWorkerEditorDelete.as_view()),

    url(r'^workspace_create_close/(?P<uuid>[0-9a-f-]+)/$', WorkspaceCloseCreate.as_view()),
    url(r'^workspace_delete_close/(?P<uuid>[0-9a-f-]+)/$', WorkspaceCloseDelete.as_view()),
    url(r'^workspace_create_rejected/(?P<pk>\d+)/$', WorkspaceRejectedCreate.as_view()),
    url(r'^workspace_create_claim/(?P<uuid>[0-9a-f-]+)/$', WorkspaceClaimCreate.as_view()),
    url(r'^workspace_unverify/(?P<uuid>[0-9a-f-]+)/$', WorkspaceUnverify.as_view()),

    url(r'^board_create_close/(?P<uuid>[0-9a-f-]+)/$', BoardPlannerCloseCreate.as_view()),
    url(r'^board_delete_close/(?P<uuid>[0-9a-f-]+)/$', BoardPlannerCloseDelete.as_view()),
    url(r'^board_create_rejected/(?P<pk>\d+)/$', BoardPlannerRejectedCreate.as_view()),
    url(r'^board_create_claim/(?P<uuid>[0-9a-f-]+)/$', BoardPlannerClaimCreate.as_view()),
    url(r'^board_unverify/(?P<uuid>[0-9a-f-]+)/$', BoardPlannerUnverify.as_view()),

    url(r'^column_create_close/(?P<uuid>[0-9a-f-]+)/$', ColumnPlannerCloseCreate.as_view()),
    url(r'^column_delete_close/(?P<uuid>[0-9a-f-]+)/$', ColumnPlannerCloseDelete.as_view()),
    url(r'^column_create_rejected/(?P<pk>\d+)/$', ColumnPlannerRejectedCreate.as_view()),
    url(r'^column_create_claim/(?P<uuid>[0-9a-f-]+)/$', ColumnPlannerClaimCreate.as_view()),
    url(r'^column_unverify/(?P<uuid>[0-9a-f-]+)/$', ColumnPlannerUnverify.as_view()),

    url(r'^card_create_close/(?P<uuid>[0-9a-f-]+)/$', CardPlannerCloseCreate.as_view()),
    url(r'^card_delete_close/(?P<uuid>[0-9a-f-]+)/$', CardPlannerCloseDelete.as_view()),
    url(r'^card_create_rejected/(?P<pk>\d+)/$', CardPlannerRejectedCreate.as_view()),
    url(r'^card_create_claim/(?P<uuid>[0-9a-f-]+)/$', CardPlannerClaimCreate.as_view()),
    url(r'^card_unverify/(?P<uuid>[0-9a-f-]+)/$', CardPlannerUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentPlannerCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentPlannerCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentPlannerRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentPlannerClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentPlannerUnverify.as_view()),
]
