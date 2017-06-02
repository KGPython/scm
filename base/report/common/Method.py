from django.core.cache import caches
import json
def getRbacDepart(p_id=None):
    rbac = caches['redis2'].get('rbac_role')

    rbacDepartList = []
    rbacDepart = ''
    departs = rbac['depart']
    if len(departs):
        departs = departs.replace('},', '}$')
        departList = departs.split('$')
        for depart in departList:
            depart = json.loads(depart)
            if p_id:
                if depart['p_id'] == str(p_id):
                    subDepartStr = depart['sub'][0:len(depart['sub']) - 1]
                    subDepartList = subDepartStr.split(',')
                    subDepartListStr  = '"' + '","'.join(subDepartList) + '"'

                    rbacDepartList += subDepartList
                    rbacDepart += subDepartListStr+','
            else:
                subDepartStr = depart['sub'][0:len(depart['sub']) - 1]
                subDepartList = subDepartStr.split(',')
                subDepartListStr = '"' + '","'.join(subDepartList) + '"'

                rbacDepartList += subDepartList
                rbacDepart += subDepartListStr + ','
    rbacDepart = rbacDepart[0:len(rbacDepart) - 1]

    return rbacDepartList,rbacDepart

def getRbacClass():
    rbac = caches['redis2'].get('rbac_role')
    rbacClassList = []
    rbacClass = ''
    rbacCategory = rbac['category']
    if len(rbacCategory):
        rbacCategory = rbacCategory.replace('},', '}$')
        rbacCategoryList = rbacCategory.split('$')
        for category in rbacCategoryList:
            category = json.loads(category)
            ClassStr = category['sub'][0:len(category['sub']) - 1]
            ClassList = ClassStr.split(',')
            ClassListStr = '"' + '","'.join(ClassList) + '"'

            rbacClassList += ClassList
            rbacClass += ClassListStr + ','
    rbacClass = rbacClass[0:len(rbacClass) - 1]

    return rbacClassList,rbacClass

def getFileModifyTime(filePath=None):
    import sys, os,time
    if not filePath:
        filePath = sys.argv[0]
    stinfo = os.stat(filePath)
    time_local = time.localtime(stinfo.st_mtime)
    return time.strftime("%Y-%m-%d %H:%M:%S",time_local)