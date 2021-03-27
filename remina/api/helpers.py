def clear_empty_obj_values(obj):
  for i in list(obj):
        if obj[i] == '':
          del obj[i]
  return obj