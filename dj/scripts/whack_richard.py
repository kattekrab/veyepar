# whack_richard
# removes test data from a ricard

import pprint
import slumber
import pw

# test data is defined by this list of categories:
test_categories = [ 
    'carlcon-2012',
    'test_show', 
    'chipy_aug_2012',
    'scipy_2012']

host_user = 'willkg'
# host_user = 'test'

host = pw.richard[host_user]
pprint.pprint(host)

api = slumber.API(host['url'])

# hunt down any previous data that looks like the data we are working with
# and kill it.
print "deliting...", test_categories
cats = api.category.get()
for cat in cats['objects']:
    # print "found", cat['slug'],
    if cat['slug']  in test_categories:
        cat_id = cat['id']
        print "found", cat_id, cat['slug'], 'deletted:',
        print api.category(cat_id).delete(
                username=host['user'], 
                api_key=host['api_key'])

