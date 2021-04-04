from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import *
from datetime import datetime, timedelta
import pytz
from itertools import chain

# CUSTOM VALIDATORS
goal_types = ['day', 'week', 'month']

def validate_timeperiod(value):
    if value not in goal_types:
        raise ValidationError(
            _('%(value)s is not a goal type'),
            params={'value': value},
        )

# CUSTOM METHODS
def to_dict(model_array):
  dict_array = []
  for instance in model_array:
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    dict_array.append(data)
  return dict_array

def create_check_array(checks):
  array = [0, 1, 2, 3, 4, 5, 6]
  for check in checks:
    array[check['timestamp'].weekday()] = check
  return array


def one_week_ago():
  one_week_ago = datetime.today() - timedelta(days=7)
  one_week_ago_tzaware = one_week_ago.replace(tzinfo=pytz.UTC)
  return one_week_ago_tzaware

def one_month_ago():
  one_month_ago = datetime.today() - relativedelta(month=-1)
  one_month_ago_tzaware = one_month_ago.replace(tzinfo=pytz.UTC)
  return one_month_ago_tzaware

def clear_empty_obj_values(obj):
  for i in list(obj):
        if obj[i] == '':
          del obj[i]
  return obj