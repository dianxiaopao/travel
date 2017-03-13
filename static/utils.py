# -*- coding: utf-8 -*-
import os
from django.conf import settings
from elasticsearch import Elasticsearch


def switch_path_relative(absolute_path, keyword):
    idx = absolute_path.index(keyword)
    path = "\\" + absolute_path[idx:]
    path = '/'.join(path.split("\\"))
    return path


def write_es(data, index='travel', doc_type='note'):
    es_data = []
    es_data.append({"create": {"_index": index, "_type": doc_type}})
    es_data.append(data)
    es_host = settings.ES_HOST
    es = Elasticsearch([es_host], timeout=20)
    result = es.bulk(index=index, doc_type=doc_type, body=es_data, refresh=True)
    return result

def sql_get_es(sql):
    '''
    当用sql语句从es获取数据的时候可以使用此函数
    :param sql:传入sql语句。例：'select * from backup/backup_log ORDER BY dev_name desc limit 0,10'
    :return:{'count': 0, 'data': []}    其中count是符合条件的数据总条数，data是返回整理好的数据，是一个数组
    '''
    result = {}
    es_host_dict = settings.ES_HOST
    host = str(es_host_dict[u"host"])
    port = str(es_host_dict[u"port"])
    sql_url = "http://%s:%s/" % (host, port) + "_sql?sql=" + sql
    # 发起get请求获取数据
    es_res = requests.session().get(sql_url).content
    es_res = json.loads(es_res)
    data_res = es_res["hits"]["hits"] if es_res.has_key("hits") else {}
    result["count"] = es_res['hits']['total'] if es_res.has_key("hits") else 0
    data = []
    for item in data_res:
        data_dict = {}
        for filed in item["_source"]:
            data_dict[filed] = item["_source"][filed]
        data.append(data_dict)
    result["data"] = data
    return result
