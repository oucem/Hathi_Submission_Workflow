import abc
import logging
import os
import typing

from hsw.collection import Instantiation, Item, Collection, Package
from . import collection


class AbsStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_collection(self, root) -> collection.Collection:
        pass


class BrittleBooksStrategy(AbsStrategy):
    def build_collection(self, root) -> collection.Collection:
        # TODO inline this function
        return build_bb_collection(root)


class DSStrategy(AbsStrategy):
    def build_collection(self, root) -> collection.Collection:
        new_collection = Collection(root)
        new_collection.component_metadata["path"] = root
        new_collection.component_metadata["package_type"] = "DS HathiTrust Submission Package"
        # for folder in filter(lambda i: i.is_dir(), os.scandir(root)):
        self._build_ds_packages(parent_collection=new_collection, path=root)
        return new_collection

    def _build_ds_packages(self, parent_collection, path):
        for folder in filter(lambda i: i.is_dir(), os.scandir(path)):
            new_package = Package(parent=parent_collection)
            new_package.component_metadata["path"] = folder.path
            self._build_ds_items(new_package, path=folder.path)

    def _build_ds_items(self, package, path):
        logger = logging.getLogger(__name__)
        files = sorted(set(map(lambda item: os.path.splitext(item)[0], os.listdir(path))))
        for unique_item in files:
            logger.debug(unique_item)
            new_item = Item(parent=package)
            new_item.component_metadata["item_name"] = unique_item
            self.build_ds_instance(new_item, name=unique_item, path=path)

    def build_ds_instance(self, item, name, path):
        new_instantiation = Instantiation(category="access", parent=item)
        for file in filter(lambda i: i.is_file(), os.scandir(path)):
            if os.path.splitext(os.path.basename(file))[0] == name:
                new_instantiation.files.append(file.path)


class BuildPackage:
    def __init__(self, strategy: AbsStrategy) -> None:
        self._strategy = strategy

    def build_package(self, root):
        return self._strategy.build_collection(root)


def build_bb_instance(new_item, path, name):
    new_instantiation = Instantiation(category="access", parent=new_item)
    for file in filter(lambda i: i.is_file(), os.scandir(path)):
        if os.path.splitext(os.path.basename(file))[0] == name:
            new_instantiation.files.append(file.path)


def build_bb_package(new_package, path):
    logger = logging.getLogger(__name__)
    files = set(map(lambda item: os.path.splitext(item)[0], os.listdir(path)))
    for unique_item in sorted(files):
        logger.debug(unique_item)
        new_item = Item(parent=new_package)
        new_item.component_metadata["item_name"] = unique_item
        build_bb_instance(new_item, name=unique_item, path=path)


def build_bb_collection(root) -> Collection:
    logger = logging.getLogger(__name__)
    new_collection = Collection(root)
    for directory in filter(lambda i: i.is_dir(), os.scandir(root)):
        logger.debug("scanning {}".format(directory.path))
        new_package = Package(parent=new_collection)
        new_package.component_metadata['path'] = directory.path
        new_package.component_metadata["package_type"] = "Brittle Books HathiTrust Submission Package"
        build_bb_package(new_package, path=directory.path)
    return new_collection
