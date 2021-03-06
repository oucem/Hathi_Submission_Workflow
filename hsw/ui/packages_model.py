import warnings

from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from hsw.package_list import PackagesList
from hsw.packages import Package
from collections import namedtuple
from collections import abc

HeaderMap = namedtuple("HeaderMap", ("column_header", "data_entry", "editable"))


class NameAdapter(abc.Sized):
    def __init__(self):
        self._column_header2data_entry = {}
        self._data_entry2column_header = {}

    def __len__(self):
        assert len(self._column_header2data_entry) == len(self._data_entry2column_header)
        return len(self._column_header2data_entry)

    def add(self, column_header, data_entry):
        if column_header in self._column_header2data_entry:
            raise AttributeError("{} already maps to {}".format(column_header,
                             self._column_header2data_entry[column_header]))
        if data_entry in self._data_entry2column_header:
            raise AttributeError("{} already maps to {}".format(data_entry,
                             self._data_entry2column_header[data_entry]))

        self._column_header2data_entry[column_header] = data_entry
        self._data_entry2column_header[data_entry] = column_header

    def get_column_header(self, data_entry):
        return self._data_entry2column_header[data_entry]

    def get_data_entry(self, column_header):
        return self._column_header2data_entry[column_header]


class PackageModel(QAbstractTableModel):

    public_headers = {
        0: HeaderMap(column_header="Package", data_entry="package_name", editable=False),
        1: HeaderMap(column_header="Title Page", data_entry="title_page", editable=True),
    }

    def __init__(self, packages: PackagesList) -> None:
        warnings.warn("USE PackageModel2 instead", DeprecationWarning)
        super().__init__()
        self._name_lookup = self.setup_name_lookup()
        self._packages = packages

    @staticmethod
    def setup_name_lookup():
        name_lookup = NameAdapter()
        for _, header_map in PackageModel.public_headers.items():
            name_lookup.add(column_header=header_map.column_header, data_entry=header_map.data_entry)
        return name_lookup

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._packages)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(PackageModel.public_headers)

    def headerData(self, index, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            try:
                return PackageModel.public_headers[index].column_header
            except IndexError:
                return ""
        super().headerData(index, orientation, role)

    def setData(self, index, data, role=None):
        if role == Qt.EditRole:
            mapping = PackageModel.public_headers[index.column()]
            if mapping.editable:
                self._packages[index.row()].metadata[mapping.data_entry] = data
        return super().setData(index, data, role)

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            try:
                data_name = PackageModel.public_headers[column].column_header
                header_name = self._name_lookup.get_data_entry(data_name)
                data = self._get_data(row, header_name)
                return data
            except KeyError as e:
                print("ERROR finding data for key: {}".format(e))
                return ""

        return QVariant()

    def _get_data(self, row: int, field: str) -> str:
        try:
            data = self._packages[row].metadata[field]
        except KeyError as e:
            data = "Invalid metadata {}".format(e)

        return data

    def flags(self, index):
        column = index.column()
        if PackageModel.public_headers[column].editable:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled
        return super().flags(index)


class PackageModel2(QAbstractTableModel):
    public_headers = {
        0: HeaderMap(column_header="Object", data_entry="id", editable=False),
        # 0: HeaderMap(column_header="Package", data_entry="id", editable=False),
        1: HeaderMap(column_header="Title Page", data_entry="title_page", editable=True),
    }

    def __init__(self, packages):
        super().__init__()
        self._name_lookup = self.setup_name_lookup()
        self._packages = packages

    @staticmethod
    def setup_name_lookup():
        name_lookup = NameAdapter()
        for _, header_map in PackageModel2.public_headers.items():
            name_lookup.add(column_header=header_map.column_header, data_entry=header_map.data_entry)
        return name_lookup


    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._packages)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.public_headers)

    def headerData(self, index, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            try:
                return self.public_headers[index].column_header
            except IndexError:
                return ""
        super().headerData(index, orientation, role)

    def setData(self, index, data, role=None):
        if role == Qt.EditRole:
            mapping = self.public_headers[index.column()]
            if mapping.editable:
                self._packages[index.row()].metadata[mapping.data_entry] = data
        return super().setData(index, data, role)

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            try:
                data_name = self.public_headers[column].column_header
                header_name = self._name_lookup.get_data_entry(data_name)
                data = self._get_data(row, header_name)
                return data
            except KeyError as e:
                print("ERROR finding data for key: {}".format(e))
                return ""

        return QVariant()

    def _get_data(self, row: int, field: str) -> str:
        try:
            data = self._packages[row].metadata[field]
        except KeyError as e:
            data = "Invalid metadata {}".format(e)

        return data

    def flags(self, index):
        column = index.column()
        if self.public_headers[column].editable:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled
        return super().flags(index)