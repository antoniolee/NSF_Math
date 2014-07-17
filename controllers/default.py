# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    post_url = URL('addEntry')
    myEntries = (db.entries.author == get_email())
    grid = SQLFORM.grid(myEntries,
        searchable=True,
        fields=[db.entries.creation_date, db.entries.data1, 
                db.entries.data2, db.entries.data3, db.entries.results],
        csv=False,
        details=True, create=False, editable=True, deletable=True,
        maxtextlength=64, paginate=10,
        )
    return dict(grid=grid)    

@auth.requires_login()
def save():
    var1 = request.vars.var1
    var2 = request.vars.var2
    var3 = request.vars.var3
    result = request.vars.result
    db.entries.insert(data1=var1,data2=var2,data3=var3, results=result)
    return dict()

@auth.requires_login()
def add():
    return dict()

def addEntry():
    s = request.vars.msg or ''
    return response.json(dict(result=s.upper()))


def user():
    
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
