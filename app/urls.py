from django.urls import path
from .views import ItemFilterView
from .views import ItemDetailView
from .views import ItemCreateView
from .views import ItemUpdateView
from .views import ItemDeleteView
from .views import ItemObjectDatabasesView
from .views import ItemObjectTablesView
from .views import ItemObjectTableSchemaView
from .views import ItemObjectTableStatusView
from .views import ItemPrivilegesView
from .views import ItemPrivilegesUserView
from .views import ItemPrivilegesDbView
from .views import ItemPrivilegesTableView
from .views import ItemShowListView
from .views import ItemShowFullProcesslistView
from .views import ItemShowVariablesView
from .views import ItemShowGlobalStatusView
from .views import ItemShowEngineInnodbStatusView
from .views import ItemShowMasterStatusView
from .views import ItemShowMasterLogsView
from .views import ItemShowSlaveStatusView
from .views import ItemShowSlaveHostsView
from .views import ItemOperationKillProcessView
from .views import ItemOperationChangeParameterView
from .views import ItemOperationPurgeMasterLogsView
from .views import ItemOperationSlaveStartView
from .views import ItemOperationSlaveStopView
from .views import ItemOperationSlaveSkipCounterView
from .views import ItemOperationSlaveResetView
from .views import ItemOperationSlaveChangeMasterView


urlpatterns = [
    path('', ItemFilterView.as_view(), name='index'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/object_databases', ItemObjectDatabasesView.as_view(), name='object_databases'),
    path('detail/<int:pk>/object_tables/<path_db>', ItemObjectTablesView.as_view(), name='object_tables'),
    path('detail/<int:pk>/object_table_schema/<path_db>/<path_table>', ItemObjectTableSchemaView.as_view(), name='object_table_schema'),
    path('detail/<int:pk>/object_table_status/<path_db>/<path_table>', ItemObjectTableStatusView.as_view(), name='object_table_status'),
    path('detail/<int:pk>/privileges', ItemPrivilegesView.as_view(), name='privileges'),
    path('detail/<int:pk>/privileges/user', ItemPrivilegesUserView.as_view(), name='privileges_user'),
    path('detail/<int:pk>/privileges/db', ItemPrivilegesDbView.as_view(), name='privileges_db'),
    path('detail/<int:pk>/privileges/table', ItemPrivilegesTableView.as_view(), name='privileges_table'),
    path('detail/<int:pk>/show_list', ItemShowListView.as_view(), name='show_list'),
    path('detail/<int:pk>/show_full_processlist', ItemShowFullProcesslistView.as_view(), name='show_full_processlist'),
    path('detail/<int:pk>/show_variables', ItemShowVariablesView.as_view(), name='show_variables'),
    path('detail/<int:pk>/show_global_status', ItemShowGlobalStatusView.as_view(), name='show_global_status'),
    path('detail/<int:pk>/show_engine_innodb_status', ItemShowEngineInnodbStatusView.as_view(), name='show_engine_innodb_status'),
    path('detail/<int:pk>/show_master_status', ItemShowMasterStatusView.as_view(), name='show_master_status'),
    path('detail/<int:pk>/show_master_logs', ItemShowMasterLogsView.as_view(), name='show_master_logs'),
    path('detail/<int:pk>/show_slave_status', ItemShowSlaveStatusView.as_view(), name='show_slave_status'),
    path('detail/<int:pk>/show_slave_hosts', ItemShowSlaveHostsView.as_view(), name='show_slave_hosts'),
    path('detail/<int:pk>/operation_kill_process', ItemOperationKillProcessView.as_view(), name='operation_kill_process'),
    path('detail/<int:pk>/operation_change_parameter', ItemOperationChangeParameterView.as_view(), name='operation_change_parameter'),
    path('detail/<int:pk>/operation_purge_master_logs', ItemOperationPurgeMasterLogsView.as_view(), name='operation_purge_master_logs'),
    path('detail/<int:pk>/operation_slave_start', ItemOperationSlaveStartView.as_view(), name='operation_slave_start'),
    path('detail/<int:pk>/operation_slave_stop', ItemOperationSlaveStopView.as_view(), name='operation_slave_stop'),
    path('detail/<int:pk>/operation_slave_skip_counter', ItemOperationSlaveSkipCounterView.as_view(), name='operation_slave_skip_counter'),
    path('detail/<int:pk>/operation_slave_reset', ItemOperationSlaveResetView.as_view(), name='operation_slave_reset'),
    path('detail/<int:pk>/operation_slave_change_master', ItemOperationSlaveChangeMasterView.as_view(), name='operation_slave_change_master'),
]
