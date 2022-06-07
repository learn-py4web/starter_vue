"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from unicodedata import name
from py4web import action, request, abort, redirect, URL, Field
from pydal.validators import IS_NOT_EMPTY, IS_IN_SET
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_user_name
import time
from .courses import *

from py4web.utils.form import Form, FormStyleBulma, RadioWidget
from py4web.utils.grid import Grid, GridClassStyleBulma


from .models import OLIVE_KINDS

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', url_signer)
def index():
    if len(db(db.admin).select().as_list()) == 0 and get_user_email() != None:
        db.admin.insert(email = get_user_email(), name = get_user_name(), permission = "admin", true_permission = "admin")
    perm = db(db.admin.email == get_user_email()).select().as_list()
    active_tables = db(db.planners.status == True).select().as_list()
    inactive_tables = db(db.planners.status == False).select().as_list()
    # print(perm[0])
    user_name = None
    user_perm = None
    user_true_perm = None
    print(perm)
    if len(perm) != 0:
        user_name = perm[0]["name"]
        user_perm = perm[0]["permission"]
        user_true_perm = perm[0]["true_permission"]

    return dict(
        # This is the signed URL for the callback.
        user_name = user_name,
        user_perm = user_perm,
        true_perm = user_true_perm,
        user_email = get_user_email(),
        active_tables = active_tables,
        inactive_tables = inactive_tables
    )

@action('add_table', method=["GET","POST"])
@action.uses('add_table.html', url_signer)
def add_table():
    if len(db(db.admin.email == get_user_email()).select().as_list()) == 0:
        return dict(error = True)
    form = Form(db.planners, deletable=False, formstyle=FormStyleBulma)
    # FormStyleBulma.widgets['Populate_with_default_class_data']=RadioWidget()
    # FormStyleBulma.widgets['Populate_with_default_instructor_data']=RadioWidget()
    form = Form([Field('Table_Name', requires=IS_NOT_EMPTY()), 
        Field('Populate_with_default_class_data', requires=IS_IN_SET(['Yes','No'])),
        Field('Populate_with_default_instructor_data', requires=IS_IN_SET(['Yes','No']))], csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # The update already happened!
        
        if form.vars['Populate_with_default_class_data'] == 'Yes':
            planner_id = db.planners.insert(name = form.vars['Table_Name'], status = True, class_num = len(courses), instruct_num = 100)
            for course in courses:
                print(course)
                db.classes.insert(class_name = course['class_name'], 
                    class_type = course['class_name'].split(" ")[0], 
                    class_num = course['class_name'].split(" ")[1],
                    class_sub = course['class_subtitle'], 
                    class_desc = course['class_description'], 
                    href = course['href'],
                    default_inst = course['class_instructor'].split(", "),
                    default_quarters = course['class_quarters'].split(", "),
                    planner_id = planner_id
                    )
        else:
            db.planners.insert(name = form.vars['Table_Name'], status = True, class_num = 0, instruct_num = 0)


        if form.vars['Populate_with_default_instructor_data'] == 'Yes':
            # planner_id = db.planners.insert(name = form.vars['Table_Name'], status = True, class_num = len(courses), instruct_num = 100)
            for course in courses:
                # print(course)
                db.instructors.insert(name = course['class_instructor'],
                    planner_id = planner_id
                    )

        redirect(URL('index'))
    return dict(
        # This is the signed URL for the callback.
        error = False,
        form = form
    )

@action('init_table', method=["GET","POST"])
@action.uses('init_table.html', url_signer)
def init_table():
    print(courses)
    redirect(URL('add_table'))
    return dict(
        # This is the signed URL for the callback.
        error = False,
        form = form
    )

@action('change_perm/<perm>', method=["GET","POST"])
@action.uses('change_perm.html', url_signer)
def change_perm(perm = "instructor"):
    db(db.admin.email == get_user_email()).update(permission = perm)
    redirect(URL('index'))
    return

@action('table/<table_id:int>')
@action.uses('table.html', url_signer)
def table(table_id = None):
    planner = db(db.planners.id == table_id).select().as_list()[0]

    # instructors = db(db.users.name == get_user_name()).select().as_list()
    # for instructor in instructors:
    #     instructor['classes'] = ''
    #     s = db(db.classes.contact_id == instructor['id']).select()

    return dict(
        # This is the signed URL for the callback.
        planner = planner,
        # instructors = instructors,
        load_classes_url = URL('load_classes', table_id, signer=url_signer),
        load_instructors_url = URL('load_instructors', table_id, signer=url_signer),
        add_class_url = URL('add_class', table_id, signer=url_signer),
        add_instructors_url = URL('add_instructor', table_id, signer=url_signer),
        delete_class_url = URL('delete_class', signer=url_signer),
        edit_class_url = URL('edit_class', signer=url_signer),
        edit_classes_url = URL('edit_classes', signer=url_signer),
        edit_instructor_url = URL('edit_instructor', signer=url_signer),
        update_tables_url = URL('update_tables', signer=url_signer)
    )

@action('archive/<table_id:int>')
@action.uses('archive.html', url_signer)
def archive(table_id = None):
    db(db.planners.id == table_id).update(status = False)
    redirect(URL('index'))

@action('unarchive/<table_id:int>')
@action.uses('unarchive.html', url_signer)
def unarchive(table_id = None):
    db(db.planners.id == table_id).update(status = True)
    redirect(URL('index'))

# This is our very first API function.
@action('load_classes/<table_id:int>')
@action.uses(url_signer.verify(), db)
def load_classes(table_id = None):
    rows = db(db.classes.planner_id == table_id).select().as_list()
    return dict(rows=rows)

@action('load_instructors/<table_id:int>')
@action.uses(url_signer.verify(), db)
def load_instructors(table_id = None):
    rows = db(db.instructors.planner_id == table_id).select().as_list()
    return dict(rows=rows)

@action('add_class/<table_id:int>', method="POST")
@action.uses(url_signer.verify(), db)
def add_class(table_id = None):
    print(request.json)
    id = db.classes.insert(
        class_name=request.json.get('class_name'),
        class_type=request.json.get('class_type'),
        planner_id = table_id
    )
    return dict(id=id)

@action('add_instructor/<table_id:int>', method="POST")
@action.uses(url_signer.verify(), db)
def add_instructor(table_id = None):
    print("REQUEST",request.json)
    id = db.instructors.insert(
        email=request.json.get('email'),
        name=request.json.get('name'),
        planner_id = table_id
    )
    print(id, table_id)
    return dict(id=id)

# def parse_instr_classlist(class_list):
#     class_list = class_list.split(', ')

#     return class_list

@action('edit_class', method="POST")
@action.uses(url_signer.verify(), db)
def edit_class():
    # update class table
    id = request.json.get('id')
    field = request.json.get('field')  # quarter
    value = request.json.get('value')  # instr name
    db(db.classes.id == id).update(**{field: value})   

    # update instructor table
    instructor_name = db(db.classes.id == id).select().as_list()[0][field]
    instructor_entry = db(db.instructors.name == value).select().as_list()
    quarter = instructor_entry[0][field]
    class_name = db(db.classes.id == id).select().as_list()[0]['class_name']
    if quarter is None:
        db(db.instructors.name == value).update(**{field: class_name})
    else:
        class_list = quarter.split(', ')
        if class_name not in class_list:
            class_list.append(class_name)
            class_list = '%s' % ', '.join(map(str, class_list))
            db(db.instructors.name == value).update(**{field: class_list})

    time.sleep(1)
    return "ok"

@action('edit_classes')
@action.uses('edit_classes.html', url_signer)
def edit_classes():
    pass
    # instructor = db(db.instructors.id == instructor_id).select().as_list()
    
    # return dict(
    #     name = name,
    #     classes = classes
    # )

@action('edit_instructor', method="POST")
@action.uses(url_signer.verify(), db)
def edit_instructor():
    # update class table
    # id = request.json.get('id')
    # field = request.json.get('field')  # quarter
    # value = request.json.get('value')  # class name
    # db(db.instructors.id == id).update(**{field: value})

    # print('request: {}, {}'.format(field, value))

    # time.sleep(1)
    return "ok"

@action('delete_class')
@action.uses(url_signer.verify(), db)
def delete_class():
    id = request.params.get('id')
    assert id is not None
    db(db.classes.id == id).delete()
    return "ok"

@action('update_tables', method="POST")
@action.uses(url_signer.verify(), db)
def update_tables():
    changes_list = request.json.get('changes_list').values()
    # print(changes_list)
    for change in list(changes_list):
        # CHANGE TO CLASSES TAB
        if change['table'] == 'classes':
            # update class table
            db(db.classes.id == change['id']).update(**{change['key']: change['value']})
            
            # cross-reference and update instr table
            instructor_name = db(db.classes.id == change['id']).select().as_list()[0][change['key']]
            instructor_entry = db(db.instructors.name == change['value']).select().as_list()
            quarter = instructor_entry[0][change['key']]
            class_name = db(db.classes.id == change['id']).select().as_list()[0]['class_name']
            if quarter is None:
                db(db.instructors.name == change['value']).update(**{change['key']: class_name})
            else:
                class_list = quarter.split(', ')
                if class_name not in class_list:
                    class_list.append(class_name)
                    class_list = '%s' % ', '.join(map(str, class_list))
                    db(db.instructors.name == change['value']).update(**{change['key']: class_list})
        # CHANGE TO INSTRUCTORS TAB
        elif change['table'] == 'instr':
            # update instr
            instructor_entry = db(db.instructors.id == change['id']).select().as_list()
            instructor_name = instructor_entry[0]['name']
            # class_list = instructor_entry[0][change['key']]
            # if class_list not None:
            #     class_list = class_list.split(', ')  # current classes

            new_class_list = change['value'].split(', ')
            new_class_entry = '%s' % ', '.join(map(str, new_class_list))
            # print(change['key'], new_class_list)
            db(db.instructors.id == change['id']).update(**{change['key']: new_class_entry})
            
            # TODO: cross-reference and classes table
            # print('new list: {}'.format(new_class_list))
            for new_class in new_class_list:
                # check CLASS table,
                class_check = db(db.classes.class_name == new_class).select().as_list()
                # if no isntr listed:
                if class_check[0][change['key']] is None:
                    # update with this instr
                    db(db.classes.class_name == new_class).update(**{change['key']: instructor_name})
                # elif class has different instr:
                elif class_check[0][change['key']] is not instructor_name:
                    pass
                    # add new (duplicate) class with this instr
                # elif no such class:
                    # add class with this instr

    time.sleep(1)
    return "ok"
