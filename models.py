"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_name():
    return auth.current_user.get('name') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

OLIVE_KINDS = {'k': 'Kalamata', 'l': 'Ligurian'}

db.define_table(
    'classes',
    Field('class_name'),
    Field('class_type'),
    Field('class_num'),

    Field('quarter_1'),
    Field('quarter_1_TA'),
    Field('quarter_1_size'),

    Field('quarter_2'),
    Field('quarter_2_TA'),
    Field('quarter_2_size'),

    Field('quarter_3'),
    Field('quarter_3_TA'),
    Field('quarter_3_size'),

    Field('summer_1'),
    Field('summer_2'),
    Field('course_time_sections'),
    Field('actual_times'),
    Field('planner_id'),

    # Field('instructor_id', 'reference instructors'),

    # some optional fields, idk if we will use them all or not
    Field('default_inst'),
    Field('default_quarters'),
    Field('class_sub'),
    Field('href'),
    Field('class_desc'),   
)

db.define_table(
    'instructors',
    Field('email'),
    Field('name'),
    Field('quarter_1'),
    Field('quarter_2'),
    Field('quarter_3'),
    Field('summer_1'),
    Field('summer_2'),
    Field('department'),
    Field('label'), # professor, lecturer, etc
    Field('access'), #can they access the DB or not
    Field('planner_id'),
)

db.define_table(
    'admin',
    Field('email'),
    Field('name'),
    Field('permission'),
    Field('true_permission')
)

db.define_table(
    'planners',
    Field('name'),
    Field('status'),
    Field('class_num'),
    Field('instruct_num')
)

# This should not appear in forms.
# db.olives.id.readable = db.olives.id.writable = False

# db.olives.olive_name.label = T("Name")
# db.olives.olive_name.requires = IS_LENGTH(minsize=2)

# db.olives.olive_kind.requires = IS_IN_SET(OLIVE_KINDS)
# db.olives.olive_kind.default = 'k'

# db.olives.weight_tot.label = "Weight (gross)"
# db.olives.weight_tot.requires=IS_FLOAT_IN_RANGE(
#         0, 1000, error_message=T("Please enter a weigh in grams between 0 and 1Kg"))

# db.olives.weight_net.label = "Weight (net, dry)"
# db.olives.weight_net.requires=IS_FLOAT_IN_RANGE(
#         0, 1000, error_message=T("Please enter a weigh in grams between 0 and 1Kg"))

db.commit()
