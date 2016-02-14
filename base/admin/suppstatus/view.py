# -*- coding:utf-8 -*-
__author__ = 'End-e'
from base.models import BasFee, BasSupplier, BasRole, BasUserRole
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SuppQuery, SuppStatusForm
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
# 引入分页
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

import json,decimal


@csrf_exempt
def index(request):
    posts = []
    page = request.GET.get('page', 1)
    sql_topic = "select a.bid, a.ucode, a.suppcode as suppcode, a.status as status, a.grpcode as grpcode, a.bsum as bsum, b.chnm as chnm"
    sql_topic += ",a.begindate,a.enddate,a.remark from bas_fee as a, bas_supplier as b where a.suppcode = b.suppcode"
    if request.method == 'GET':
        bid =  request.GET.get('bid')
        suppcode =  request.GET.get('suppcode')
        status =  request.GET.get('status')
        form = SuppQuery({"bid":bid,"suppcode":suppcode,"status":status})
        if bid:
            sql_topic += " and a.bid like '%" + bid.strip() + "%'"
        else:
            bid = ""
        if suppcode:
            sql_topic += " and a.suppcode like '%" + suppcode.strip() + "%'"
        else:
            suppcode = ""
        if status:
            sql_topic += " and a.status='" + status + "'"
        else:
            status = ""
        sql_topic += " order by a.suppcode"

        cursor = connection.cursor()
        cursor.execute(sql_topic)
        rslist = cursor.fetchall()
        for rowsList in rslist:
            post_dict = {}
            post_dict['bid'] = rowsList[0]
            post_dict['ucode'] = rowsList[1]
            post_dict['suppcode'] = rowsList[2]
            post_dict['chnm'] = rowsList[6]
            post_dict['status'] = rowsList[3]
            post_dict['grpcode'] = rowsList[4]
            post_dict['bsum'] = rowsList[5]
            post_dict['begindate'] = rowsList[7]
            post_dict['enddate'] = rowsList[8]
            post_dict['remark'] = rowsList[9]
            posts.append(post_dict)
        paginator = Paginator(posts, 10)  # 实例化一个分页对象
        try:
            resultList = paginator.page(page)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            resultList = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太长,没有相应的记录
            resultList = paginator.page(paginator.num_pages)  # 取最后一页的记录
    else:
        form = SuppQuery()

    return render(request, 'admin/sysConf_supply_status.html',
                  {'form': form, 'resultList': resultList, 'posts': posts, 'page': page, 'bid': bid,
                   'suppcode': suppcode, 'status': status})


@csrf_exempt
def suppStatusForm(request):
    rs = {}
    if request.method == 'POST':
        form_status = SuppStatusForm(request.POST)
        if form_status.is_valid():
            status = form_status.cleaned_data['status']
            bsum = form_status.cleaned_data['bsum']
            bid = form_status.cleaned_data['bid']
            ucode = form_status.cleaned_data['ucode']
            grpcode = form_status.cleaned_data['grpcode']
            suppcode = form_status.cleaned_data['suppcode']
            begindate = form_status.cleaned_data['begindate']
            enddate = form_status.cleaned_data['enddate']
            remark = form_status.cleaned_data['remark']

            if begindate:
                begindate = begindate.strftime("%Y-%m-%d")
            if enddate:
                enddate = enddate.strftime("%Y-%m-%d")

            if bsum:
                bsum = bsum
            else:
                bsum = decimal.Decimal("0.0")

            # 数据库查询是否有记录
            supsum_sql = "select supsum from bas_feesum where bid=" + bid
            try:
                cursor = connection.cursor()
                cursor.execute(supsum_sql)
                supsum_list = cursor.fetchone()
                sum = bsum
                if supsum_list:
                    sum += supsum_list[0]
                    feesumup_sql = "update bas_feesum set supsum="+str(sum)+",bfdate=curdate() where bid="+bid
                    cursor.execute(feesumup_sql)

                else:
                    feesum_sql = "insert into bas_feesum (bid, suppcode, grpcode, ucode, supsum, status, bfdate) " \
                                 "values (" + bid +",'"+suppcode+"','"+grpcode+"','"+ucode+"','"+str(bsum)+"','"+status+"',curdate())"
                    cursor.execute(feesum_sql)

                sql = "update bas_fee set status='" + status + "', bsum=" + str(bsum) + ",begindate='"+begindate+"',enddate='"+enddate+"',remark='"+remark+"' where bid=" + bid
                cursor.execute(sql)
                rs["flag"] = '0'
            except Exception as e:
                print(e)
                rs["flag"] = '1'
            finally:
                cursor.close()
        return HttpResponse(json.dumps(rs))


@csrf_exempt
def findRole(request):
    grpcode = request.session.get("s_grpcode")
    utype = request.POST.get("utype")
    userid = request.POST.get("ucode")
    rs = {}
    if utype == "1":
        roleList = BasRole.objects.filter(grpcode__in=[utype, grpcode], status='1').values("rcode", "nm")
    else:
        roleList = BasRole.objects.filter(grpcode__in=[utype], status='1').values("rcode", "nm")

    urlist = BasUserRole.objects.filter(ucode=str(userid)).values("rcode")

    ct = [dict(c) for c in urlist]
    rt = [dict(d) for d in roleList]

    rs["urlist"] = ct
    rs["rolelist"] = rt
    try:
        rsjson = json.dumps(rs)
    except Exception as e:
        rsjson = {}
        print(e)
    return HttpResponse(rsjson)


@csrf_exempt
def addRole(request):
    rs = {}
    ucode = request.POST.get('ucode')
    check_choices = request.POST.getlist('choices')
    try:
        cursor = connection.cursor()
        sql = "delete from bas_user_role where ucode=" + ucode
        cursor.execute(sql)
        for row in check_choices:
            sql = "insert into bas_user_role(ucode, rcode, status,brdate) values ('" + ucode + "','" + row + "', 0, curdate())"
            cursor.execute(sql)
        rs["flag"] = '0'
    except Exception as e:
        print(e)
        rs["flag"] = '1'
    return HttpResponse(json.dumps(rs))


@csrf_exempt
def getUserStatus(request):
    bid = request.POST.get('bid')
    sql = "select status from bas_fee where bid=" + bid
    cursor = connection.cursor()
    cursor.execute(sql)
    tupStatus = cursor.fetchone()
    status = tupStatus[0]
    return HttpResponse(json.dump(status))
