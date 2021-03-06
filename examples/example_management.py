#  (C) Catchoom Technologies S.L.
#  Licensed under the MIT license.
#  https://github.com/catchoom/catchoom-python/blob/master/LICENSE
#  All warranties and liabilities are disclaimed.

from optparse import OptionParser
from pprint import pprint
import catchoom

"""
Demonstrates listing, creation, updating and deletion of every type of object
(i.e. collection, item, reference image, and collection token).

- Requires an account at https://crs.catchoom.com
- The @api_key is your management api key. Get it at
https://crs.catchoom.com/accounts/apis/
- The @filename is a valid reference image filename.
- Don't set the @hostname, unless you are using a custom platform.
"""


def run_management(api_key, filename, items_per_page=5, hostname=None):
    """
    Basic example of listing, creating, updating and finally deleting
    each type of object, using the Catchoom Management API.
    """

    if hostname:
        catchoom.settings.MANAGEMENT_HOSTNAME = hostname

    print "\n- Retrieving first %s collections..." % items_per_page
    collection_list = catchoom.get_collection_list(
        api_key,
        limit=items_per_page,
        offset=0,
    )
    for collection in collection_list:
        print "%s: %s" % (collection["uuid"], collection["name"])

    print "\n- Creating collection..."
    collection = catchoom.create_collection(
        api_key,
        name="My API collection",
    )
    collection_uuid = collection["uuid"]
    pprint(collection)

    print "\n- Retrieving collection..."
    collection = catchoom.get_collection(
        api_key,
        uuid=collection_uuid,
    )
    pprint(collection)

    print "\n- Updating collection..."
    new_name = "My edited API collection"
    success = catchoom.update_collection(
        api_key,
        uuid=collection_uuid,
        name=new_name,
    )
    print "Updated: %s, name: '%s'" % (success, new_name)

    print "\n- Retrieving collection..."
    collection = catchoom.get_collection(
        api_key,
        uuid=collection_uuid,
    )
    pprint(collection)

    print "\n- Retrieving first %s tokens..." % items_per_page
    token_list = catchoom.get_token_list(
        api_key,
        limit=items_per_page,
        offset=0,
        collection=collection_uuid,
    )
    for t in token_list:
        print "Collection: %s Token: %s" % (t["collection"], t["token"])

    print "\n- Creating token..."
    token = catchoom.create_token(
        api_key,
        collection=collection_uuid,
    )
    token_id = token["token"]
    pprint(token)

    print "\n- Deleting token..."
    success = catchoom.delete_token(
        api_key,
        token=token_id,
    )
    print "Deleted: %s" % success

    print "\n- Retrieving first %s items..." % items_per_page
    item_list = catchoom.get_item_list(
        api_key,
        limit=items_per_page,
        offset=0,
        collection=collection_uuid,
    )
    for i in item_list:
        print "%s: %s" % (i["uuid"], i["name"])

    print "\n- Creating item..."
    item = catchoom.create_item(
        api_key,
        name="My API item",
        collection=collection_uuid,
        url="http://example.com",
        custom="Lorem Ipsum",
    )
    item_uuid = item["uuid"]
    pprint(item)

    print "\n- Retrieving first %s items..." % items_per_page
    item_list = catchoom.get_item_list(
        api_key,
        limit=items_per_page,
        offset=0,
        collection=collection_uuid,
    )
    for i in item_list:
        print "%s: %s" % (i["uuid"], i["name"])

    print "\n- Retrieving item..."
    item = catchoom.get_item(
        api_key,
        uuid=item_uuid,
    )
    pprint(item)

    print "\n- Updating item..."
    new_name = "My edited API item"
    success = catchoom.update_item(
        api_key,
        uuid=item_uuid,
        name=new_name,
        custom="New Lorem Ipsum",
    )
    print "Updated: %s, name: '%s'" % (success, new_name)

    print "\n- Retrieving item..."
    item = catchoom.get_item(
        api_key,
        uuid=item_uuid,
    )
    pprint(item)

    print "\n- Retrieving first %s images..." % items_per_page
    image_list = catchoom.get_image_list(
        api_key,
        limit=items_per_page,
        offset=0,
        item=item_uuid,
    )
    for i in image_list:
        print "%s: %s" % (i["uuid"], i["name"])

    print "\n- Uploading image..."
    image = catchoom.create_image(
        api_key,
        item=item_uuid,
        filename=filename,
    )
    image_uuid = image["uuid"]
    pprint(image)

    print "\n- Retrieving image..."
    image = catchoom.get_image(
        api_key,
        uuid=image_uuid,
    )
    print "uuid: %s" % image["uuid"]
    pprint(image)

    print "\n- Deleting image..."
    success = catchoom.delete_image(
        api_key,
        uuid=image_uuid,
    )
    print "Deleted: %s" % success

    print "\n- Deleting item..."
    success = catchoom.delete_item(
        api_key,
        uuid=item_uuid,
    )
    print "Deleted: %s" % success

    print "\n- Deleting collection..."
    success = catchoom.delete_collection(
        api_key,
        uuid=collection_uuid,
    )
    print "Deleted: %s" % success


if __name__ == '__main__':
    usage = "usage: %prog -a API_KEY -f FILENAME [-H HOSTNAME]"
    parser = OptionParser(usage, version="%prog 1.0")
    parser.add_option('-a', '--api_key',
                      dest='api_key',
                      help="Management API key.")
    parser.add_option('-f', '--filename',
                      dest='filename',
                      help='Reference image that will be uploaded')
    parser.add_option('-H', '--hostname',
                      dest='hostname',
                      default=False,
                      help='Hostname of the Catchoom Recognition Platform')
    (options, args) = parser.parse_args()

    if not options.api_key:
        parser.error("Missing parameter: -a API_KEY")

    if not options.filename:
        parser.error("Missing parameter: -f FILENAME")

    run_management(api_key=options.api_key, filename=options.filename,
                   hostname=options.hostname)
