import json
from typing import List

from controllers.controller import Controller
from models.image_collection import ImageCollection
from services.images_provider import ImagesProvider


def save_collections(collections_list: List[ImageCollection]):
    print("collections list:",collections_list,len(collections_list))
    saved_collections_paths = []
    if len(collections_list)>0:
        for collection in collections_list:
            saved_collections_paths.append({'name': collection.name,
                                            'path': save_collection(collection)})
    with open('./coll.json', "w") as outfile:
        json.dump(saved_collections_paths, outfile)
    # raise IOError


def save_collection(collection: ImageCollection) -> str:
    collection_save_form = {'name': collection.name}
    # print(collection_save_form['name'])
    collection_save_form['effects'] = collection.effects.values
    print(collection_save_form['effects'])
    collection_save_form['images'] = []
    for img in collection.collection:
        if (img.page_info != None):
            collection_save_form['images'].append({'path': img.path,
                                                   'page_info': {
                                                       'text_lines': img.page_info.text_lines,
                                                       'letters': img.page_info.letters,
                                                       'lines': img.page_info.lines,
                                                       'text_block': img.page_info.text_block
                                                   },
                                                   'stains':img.stains,
                                                   'name': img.name})
        else:
            collection_save_form['images'].append({'path': img.path,
                                                   'name': img.name,
                                                   'stains':img.stains})
    filename = collection.detail_file_name + '.json'
    # print(collection_save_form)
    # print(collection.detail_file_name)
    with open('./colldet/' + filename, "w") as outfile:
        json.dump(collection_save_form, outfile)
        return filename
    # raise IOError


def save_view_config(image_provider: ImagesProvider):
    view_data = {}
    view_data['current_collection_index'] = image_provider.current_collection_index
    view_data['current_image_index'] = image_provider.current_image_index
    with open('./viewcfg.json', "w") as outfile:
        json.dump(view_data, outfile)
    # raise IOError


def write_style_config(style):
    with open('config.json') as json_file:
        data = json.load(json_file)
    data['style'] = style
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)