def qs_sort(original_order, new_order, limit):
    for idx, item in enumerate((original_order), 1):
        item.position_temp = new_order.index(item.position) + 1
        item.position = idx + limit
        item.save()

    for item in original_order:
        item.position = item.position_temp
        item.position_temp = None
        item.save()

    return {'success': True}
