##parameters=

mcat = context.portal_messages

block_types=context.get_task_block_types()
block_keys = []

items = block_types.items()

trans_types = {}
for key, value in items:
    block_keys.append((key, mcat(value['title'])), )
    compatible_types = []
    slots_nb = len(value['slots'])
    trans_types[key] = compatible_types
    for key2, value2 in items:
        if value2.get('invisible'):
            continue
        if len(value2['slots']) != slots_nb:
            continue
        ok = 1
        for slot in value['slots']:
            ok_for_this_one = 0
            for slot2 in value2['slots']:
                if slot['id'] == slot2['id']:
                    if slot['type'] != slot2['type']:
                        break
                    ok_for_this_one = 1
            if not ok_for_this_one:
                ok = 0
                break
        if ok:
            compatible_types.append(
              {'id': key2, 'title': mcat(value2['title'])}
            )

def cmp_keys(a, b):
    return (a[1] > b[1] and 1) or (a[1] < b[1] and -1) or 0

block_keys.sort(cmp_keys)
block_keys = [a[0] for a in block_keys]

return {
    'block_keys': block_keys,
    'block_types': block_types,
    'trans_types': trans_types,
}
