from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.shortcuts import render, redirect
from django.http import QueryDict, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from pure_pagination.mixins import PaginationMixin
from chartjs.views.lines import BaseLineChartView
from .models import Item
from .filters import ItemFilter
from .forms import ItemForm
from .consts import *
import pymysql.cursors
import json


def render_response(request, template_name, response_data):
    try:
        if 'json' in QueryDict(request.META['QUERY_STRING'])['format']:
            response = JsonResponse(response_data)
    except KeyError:
        response = render(request, template_name, response_data)
    # print(vars())
    return response


# Create your views here.
class ItemFilterView(LoginRequiredMixin, PaginationMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    queryset = Item.objects.all().order_by('id')

    # Settings for pure_pagination.
    paginate_by = 10
    object = Item

    # Save search condition in session.
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')


class ItemObjectDatabasesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show databases"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_object_databases.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemObjectTablesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_db):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        db_name = path_db
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port, db = db_name)
        cursor = conn.cursor()
        sql = "show tables"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_object_tables.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'db_name': db_name, 'result': result}
        return render_response(request, template_name, response_data)


class ItemObjectTableSchemaView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_db, path_table):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        db_name = path_db
        table_name = path_table
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port, db = db_name)
        cursor = conn.cursor()
        sql = "show create table " + "`" + table_name + "`"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_object_table_schema.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'db_name': db_name, 'table_name': table_name, 'result': result}
        return render_response(request, template_name, response_data)


class ItemObjectTableStatusView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_db, path_table):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        db_name = path_db
        table_name = path_table
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port, db = db_name)
        cursor = conn.cursor()
        sql = "show table status like " + "'" + table_name + "'"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_object_table_status.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'db_name': db_name, 'table_name': table_name, 'result': result}
        return render_response(request, template_name, response_data)


class ItemPrivilegesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor_user_priv = conn.cursor()
        sql_user_priv = "select Host, User, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv, Reload_priv, Shutdown_priv, Process_priv, File_priv, Grant_priv, References_priv, Index_priv, Alter_priv, Show_db_priv, Super_priv, Create_tmp_table_priv, Lock_tables_priv, Execute_priv, Repl_slave_priv, Repl_client_priv, Create_view_priv, Show_view_priv, Create_routine_priv, Alter_routine_priv, Create_user_priv, Event_priv, Trigger_priv, Create_tablespace_priv from mysql.user"
        cursor_user_priv.execute(sql_user_priv)
        desc_user_priv = [d[0].replace('#', '') for d in cursor_user_priv.description]
        result_user_priv = [dict(zip(desc_user_priv, line)) for line in cursor_user_priv]
        cursor_user_priv.close()
        cursor_db_priv = conn.cursor()
        sql_db_priv = "select * from mysql.db"
        cursor_db_priv.execute(sql_db_priv)
        desc_db_priv = [d[0].replace('#', '') for d in cursor_db_priv.description]
        result_db_priv = [dict(zip(desc_db_priv, line)) for line in cursor_db_priv]
        cursor_db_priv.close()
        cursor_table_priv = conn.cursor()
        sql_table_priv = "select * from mysql.tables_priv"
        cursor_table_priv.execute(sql_table_priv)
        desc_table_priv = [d[0].replace('#', '') for d in cursor_table_priv.description]
        result_table_priv = [dict(zip(desc_table_priv, line)) for line in cursor_table_priv]
        cursor_table_priv.close()
        template_name = 'app/item_privileges.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result_user_priv': result_user_priv, 'result_db_priv': result_db_priv, 'result_table_priv': result_table_priv}
        return render_response(request, template_name, response_data)


class ItemPrivilegesUserView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "select Host, User, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv, Reload_priv, Shutdown_priv, Process_priv, File_priv, Grant_priv, References_priv, Index_priv, Alter_priv, Show_db_priv, Super_priv, Create_tmp_table_priv, Lock_tables_priv, Execute_priv, Repl_slave_priv, Repl_client_priv, Create_view_priv, Show_view_priv, Create_routine_priv, Alter_routine_priv, Create_user_priv, Event_priv, Trigger_priv, Create_tablespace_priv from mysql.user"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_privileges_user.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemPrivilegesDbView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "select * from mysql.db"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_privileges_db.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemPrivilegesTableView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "select * from mysql.tables_priv"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_privileges_table.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowListView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        # print(vars())
        return render(request, 'app/item_show_list.html', {'id': id, 'host_name': host_name, 'port': port})


class ItemShowFullProcesslistView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        qs = QueryDict(request.META['QUERY_STRING'])
        if 'kill_id' in qs:
            cursor_update = conn.cursor()
            kill_id = QueryDict(request.META['QUERY_STRING'])['kill_id']
            sql_update = "kill " + kill_id
            cursor_update.execute(sql_update)
            # print(sql_update)
            cursor_update.close()
            return redirect('show_full_processlist', pk=id)

        cursor = conn.cursor()
        sql = "show full processlist"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_full_processlist.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowVariablesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show variables"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_variables.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowGlobalStatusView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show global status"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_global_status.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowEngineInnodbStatusView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show engine innodb status"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_engine_innodb_status.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowMasterStatusView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show master status"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_master_status.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowMasterLogsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show master logs"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_master_logs.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowSlaveStatusView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show slave status"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_slave_status.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)


class ItemShowSlaveHostsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'host_name', 'port').get(id = pk)
        id = queryset['id']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = pymysql.connect(
            user = CONNECT_USER, password = CONNECT_PASSWORD, host = host_name, port = port)
        cursor = conn.cursor()
        sql = "show slave hosts"
        cursor.execute(sql)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        template_name = 'app/item_show_slave_hosts.html'
        response_data = {'id': id, 'host_name': host_name, 'port': port, 'result': result}
        return render_response(request, template_name, response_data)
