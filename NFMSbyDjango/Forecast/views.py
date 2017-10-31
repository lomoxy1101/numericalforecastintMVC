from django.shortcuts import render,HttpResponsePermanentRedirect
from Forecast import models
from Forecast import Forms
# import pynq
from Forecast import viewmodels
from django.http import JsonResponse
from django.conf import settings
import os
import json

# Create your views here.

def selectMapping(request):
    #注意render也是需要返回的
    # 不能直接携程render(xxx)
    return render(request,"Forecast/Index.html",{})
    # return "selectMapping"

def routeMapping():
    return "routeMapping"

def test(request):
    # 1 获取请求中的用户名及密码
    # 对于传统的?方式提交的参数直接通过request.GET.get('key')的方式获取
    name = request.GET.get('name', None)
    pwd = request.GET.get('pwd', None)
    list_nodes=getActions(name,pwd)

    return render(request, 'Forecast/Test.html', {'list_actions': list_nodes})

def initModelData(request):
    obj= models.UserInfo(Name="ceshi",Pwd="123")
    obj.save()
    print("写入成功")
    return render(request, 'Forecast/Test.html', {})

def getActions(name,pwd):
    '''
    根据用户名及密码获取该用户所拥有的菜单集合
    :param name:用户名
    :param pwd:密码
    :return:
    '''
    # 2 根据用户名及密码查询是否存在指定用户，密码是否正确
    # obj_user= models.UserInfo.objects.get(Name=name)
    users = models.UserInfo.objects.filter(Name=name)
    if users.count() == 1:
        obj_user = users.first()
        if obj_user and pwd:
            if obj_user.Pwd == pwd:
                # 2.1 密码用户名均正确
                # 根据该用户查询其拥有的权限
                # 注意此处的r是个 <QuerySet[]>
                r = obj_user.r_userinfo_action_set.all()
                # 查找该用户拥有的全部权限
                # actions= From(r).Where()
                # actions=pynq.From(r.ActionId).Where("isPass==0").select_many()
                list_actions = [x.ActionId for x in r]
                # 对actions进行排序
                # actions_sorted=sorted(actions,key=lambd a:a.Sort)
                # new_actions=list(set(actions))
                # new_actions.sort(key=actions.Url)
                # func=lambda x,y:x if y.Url==x.Url
                for a in list_actions:
                    #
                    print(a.Name)

                navbarmenu = Forms.NavbarMenu(list_actions)
                list_nodes = navbarmenu.getHomeTreeNode(list_actions, 0)
    return  list_nodes

def searchInit(request):
    #初始化显示全球里面的所有内容
    data_dict,files = iterator_dir(os.path.join(settings.BASE_DIR, 'static\images\pic\Global'))
    return render(request, 'Forecast/SerachHistory.html', {'data_dict': data_dict,'image_url':data_dict[files[0]]})

# 遍历文件夹下所有文件
def iterator_dir(dirpath):
    leng = len(settings.BASE_DIR)
    dict = {} #{filename:filepath}
    files=[] #[filename]
    for dirpath, dirnames, filenames in os.walk(dirpath, topdown=True):
        root = dirpath[leng:]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            dict[filename] = filepath
            files.append(filename)
    return dict,files

# @csrf.exempt
# <a href="#" class="list-group-item" data-imgurl="{{ value }}" onclick="changePic(this)">{{ key }}</a>
# request.POST[start_time]= 2017-09-01
# request.POST[end_time]=
# request.POST[area]= 西北太
# request.POST[category]= C1
# request.POST[factor]= F5
# request.POST[layer]= L7
# request.POST[moment]= M7
def searchHistory(request):
    # 暂时使用本地图片路径做测试
    root_path = os.path.join(settings.BASE_DIR, 'static\images\pic')
    html = ''
    if request.method == 'POST':
    #     print('request.POST=',request.POST)
    #     for i in request.POST:
    #        print("request.POST[%s]=" % i, request.POST[i])
        dir_path = os.path.join(root_path,
                                settings.AREA_DICT[request.POST['area']])
        data_dict, files = iterator_dir(dir_path)
        #判断查询是否有结果
        for filename,filepath in data_dict.items():
            line = "<a href='#' class='list-group-item' data-imgurl="+filepath+" onclick='changePic(this)'>"+filename+"</a>";
            html += line
        return_json={'image_url':data_dict[files[0]],'html':html}
    return JsonResponse(return_json)
