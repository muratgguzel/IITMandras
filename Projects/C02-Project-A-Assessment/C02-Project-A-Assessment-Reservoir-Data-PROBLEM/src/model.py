from sys import settrace
from database import Database
from bson.objectid import ObjectId

class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_device_id(self, device_id):
        self.latest_error = ''

        # 1.A KEY TO RETRIEVE A SINGLE DEVICE BY SPECIFYING DEVICE ID

        key = {"device_id": device_id}
        document=self.__find(key)
        if (document):
            return document
        else:
            self.latest_error = f'Device id {device_id} not found!'
            return -1

    def find_by_object_id(self, object_id):
        key = {'_id': ObjectId(object_id)}
        return self.__find(key)

    def __find(self, key):

        document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)

        if (document):
            return document
        else:
            self.latest_error = f'Device id with Key: {key} not found!'
            return -1


    def insert(self, device_id, desc, type, manufacturer):
        self.latest_error = ''
        document = self.find_by_device_id(device_id)

        if (document!=-1):
            self.latest_error = f'Device id {device_id} already exists!'
            return -1

        device_data = {
            'device_id': device_id,
            'desc': desc,
            'type': type,
            'manufacturer': manufacturer
        }

        object_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
        print(f"Object_Id:{object_id} Device Data:{device_data} document Inserted Successfully,")
        return self.find_by_object_id(object_id)


class ReservoirDataModel:
    RESERVOIR_DATA_COLLECTION = 'reservoir_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
        
    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error
    
    def find_by_device_id_and_timestamp(self, device_id, timestamp):

        #1.B QUERY TAKES A DEVICE ID AND TIMESTEPM TO RETRIEV DESIRED DOCUMENT
        key = {"device_id": device_id,"timestamp":timestamp}
        document = self.__find(key)
        if (document):
            return document
        else:
            self.latest_error = f'Device id with Key: {key} not found!'
            return -1


    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    def find_all(self):
        key = {}
        return self.__find_multiple(key)
    
    def aggregate(self, pipeline):
        documents = self._db.aggregate(ReservoirDataModel.RESERVOIR_DATA_COLLECTION, pipeline)
        return documents
    
    def __find(self, key):

        documents = self._db.get_single_data(ReservoirDataModel.RESERVOIR_DATA_COLLECTION, key)
        return documents

    def __find_multiple(self, key):
        documents = self._db.get_multiple_data(ReservoirDataModel.RESERVOIR_DATA_COLLECTION, key)
        return documents
    
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        document = self.find_by_device_id_and_timestamp(device_id, timestamp)
        
        if (document):
            self.latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        
        reservoir_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        object_id = self._db.insert_single_data(ReservoirDataModel.RESERVOIR_DATA_COLLECTION, reservoir_data)
        return self.find_by_object_id(object_id)


class DailyReportModel:
    DAILY_REPORT_COLLECTION = 'daily_report'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error
    
    def find_by_device_id_and_date(self, device_id, date):

        #2.A TAKES A DEVICE ID AND PARTICULAR DATE RETURNS DOCUMENT
        key = {"device_id": device_id, "date": date}
        document_list = self.__find(key)

        if (document_list[0]):
            return document_list[0]
        else:
            self.latest_error = f'Device id with Key: {key} not found!'
            return -1

    def find_by_device_id_and_date_range(self, device_id, from_date, to_date):

        # 2.B TAKES A DEVICE ID AND DATE RANGE RETURNS DOCUMENT LIST
        key = {"device_id": device_id, "date": {"$gte": from_date,"$lte": to_date}}
        documentlist = self.__find(key)

        if (documentlist[0]):
            return documentlist
        else:
            self.latest_error = f'Record with Key: {key} not found!'
            return -1

    def find_first_anomaly_by_date_range(self, device_ids, threshold, from_date, to_date):

        # 3.A-B TAKES A DEVICE IDS , Threshold and Query dates , return first anomaly greated than threshold
        key = {"date": {"$gte": from_date, "$lte": to_date}, "device_id": {"$in": device_ids}, "max_value": {"$gt": threshold}}

        documentlist = self.__find(key)

        #Get first
        if (documentlist[0]):
            return documentlist[0]
        else:
            self.latest_error = f'Record with Key: {key} not found!'
            return -1

    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    def __find(self, key):

        documents_list=[]
        cursor = self._db.get_multiple_data(DailyReportModel.DAILY_REPORT_COLLECTION, key)
        for document in cursor:
            documents_list.append(document)

        return documents_list


    def __find_multiple(self, key):
        daily_report_documents = self._db.get_multiple_data(DailyReportModel.DAILY_REPORT_COLLECTION, key)
        return daily_report_documents

    def insert(self, device_id, avg_value, min_value, max_value, date):
        self.latest_error = ''

        daily_report_document = self.find_by_device_id_and_date(device_id, date)
        if (daily_report_document):
            self.latest_error = f'Report for date {date} for device id {device_id} already exists'
            return -1
        
        daily_report_data = {
            'device_id': device_id, 
            'avg_value': avg_value, 
            'min_value': min_value, 
            'max_value': max_value, 
            'date': date
            }

        object_id = self._db.insert_single_data(DailyReportModel.DAILY_REPORT_COLLECTION, daily_report_data)
        
        return self.find_by_object_id(object_id)

    def insert_multiple(self, dr_docs):
        object_ids = self._db.insert_multiple_data(DailyReportModel.DAILY_REPORT_COLLECTION, dr_docs)
        
        return object_ids
