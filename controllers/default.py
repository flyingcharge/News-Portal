# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################



def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    posts=db(db.news).select()
    
    
    return dict(posts=posts,form=FORM(INPUT(_id='keyword',_name='keyword', _placeholder='Search',
                _onkeyup="ajax('callback', ['keyword'], 'target');")),
                   target_div=DIV(_id='target'))


def callback():

    query = db.tags.refcategory.contains('All')
    query2 = db.tags.giventag.contains(request.vars.keyword)
    pages = db(query & query2).select(orderby=db.tags.giventag)
    links = [A(p.giventag, _href=URL('show',args=p.linkid)) for p in pages]
    return UL(*links)


@auth.requires_login()
def create():
    form = SQLFORM(db.news,request.args(0)).process()
    #form.id.readable=False
    category =1 
    
    if form.accepted:
        session.flash = "Posted!"
        getid = form.vars.id
        lines = db(db.news.id == getid).select(db.news.tag)
        category = db(db.news.id == getid).select(db.news.category)[0].category
        for line in lines:
            for eachtag in line.tag.split(','):
                db.tags.insert(giventag = eachtag, refcategory = 'All', linkid = getid)
                for jal in category:            
                    db.tags.insert(giventag = eachtag, refcategory = jal, linkid = getid)
        redirect(URL('index'))
    elif form.errors:
        session.flash="Errors!"
    return locals()

@auth.requires_login()
def myposts():
    cols = db(db.news.created_by==auth.user).select()
    return locals()
    
def politics():
    products = db(db.news.category.contains('Politics')).select()
    rows = db().select(db.news.tag)
    return dict(products=products,rows=rows,form=FORM(INPUT(_id='keyword',_name='keyword',_placeholder='Search',
                _onkeyup="ajax('callback_politics', ['keyword'], 'target');")),
                   target_div=DIV(_id='target'))

def callback_politics():

    query = db.tags.refcategory.contains('Politics')
    query2 = db.tags.giventag.contains(request.vars.keyword)
    pages = db(query & query2).select(orderby=db.tags.giventag)
    links = [A(p.giventag, _href=URL('show',args=p.linkid)) for p in pages]
    return UL(*links)

def entertainment():
    products = db(db.news.category.contains('Entertainment')).select()
    rows = db().select(db.news.tag)
    return dict(products=products,rows=rows,form=FORM(INPUT(_id='keyword',_name='keyword',_placeholder='Search',
                _onkeyup="ajax('callback_entertainment', ['keyword'], 'target');")),
                   target_div=DIV(_id='target'))

def callback_entertainment():

    query = db.tags.refcategory.contains('Entertainment')
    query2 = db.tags.giventag.contains(request.vars.keyword)
    pages = db(query & query2).select(orderby=db.tags.giventag)
    links = [A(p.giventag, _href=URL('show',args=p.linkid)) for p in pages]
    return UL(*links)


def sports():
    products = db(db.news.category.contains('Sports')).select()
    rows = db().select(db.news.tag)
    return dict(products=products,rows=rows,form=FORM(INPUT(_id='keyword',_name='keyword',_placeholder='Search',
                _onkeyup="ajax('callback_sports', ['keyword'], 'target');")),
                   target_div=DIV(_id='target'))

def callback_sports():

    query = db.tags.refcategory.contains('Sports')
    query2 = db.tags.giventag.contains(request.vars.keyword)
    pages = db(query & query2).select(orderby=db.tags.giventag)
    links = [A(p.giventag, _href=URL('show',args=p.linkid)) for p in pages]
    return UL(*links)


def business():
    products = db(db.news.category.contains('Business')).select()
    rows = db().select(db.news.tag)
    return dict(products=products,rows=rows,form=FORM(INPUT(_id='keyword',_name='keyword',_placeholder='Search',
                _onkeyup="ajax('callback_business', ['keyword'], 'target');")),
                   target_div=DIV(_id='target'))

def callback_business():

    query = db.tags.refcategory.contains('Business')
    query2 = db.tags.giventag.contains(request.vars.keyword)
    pages = db(query & query2).select(orderby=db.tags.giventag)
    links = [A(p.giventag, _href=URL('show',args=p.linkid)) for p in pages]
    return UL(*links)


def technology():
    products = db(db.news.category.contains('Technology')).select()
    rows = db().select(db.news.tag)
    return dict(products=products,rows=rows,form=FORM(INPUT(_id='keyword',_name='keyword',_placeholder='Search',
                _onkeyup="ajax('callback_technology', ['keyword'], 'target');")),
                   target_div=DIV(_id='target'))

def callback_technology():

    query = db.tags.refcategory.contains('Technology')
    query2 = db.tags.giventag.contains(request.vars.keyword)
    pages = db(query & query2).select(orderby=db.tags.giventag)
    links = [A(p.giventag, _href=URL('show',args=p.linkid)) for p in pages]
    return UL(*links)

def show():
    
    post = db.news(request.args(0,cast=int))
    picture = db(db.news.id ==post.id).select().first().picture
    pic1 = db(db.news.id ==post.id).select().first().pic_1
    pic2 = db(db.news.id ==post.id).select().first().pic_2
    pic3 = db(db.news.id ==post.id).select().first().pic_3
    form = SQLFORM(db.blog_comment).process()
    
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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
