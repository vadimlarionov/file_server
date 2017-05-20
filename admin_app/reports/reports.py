from abc import abstractclassmethod
from enum import Enum

from admin_app.user.user import UserActiveRecord


class ReportType(Enum):
    users = 1
    groups = 2


class Report:
    @abstractclassmethod
    def get_headers(self):
        pass

    @abstractclassmethod
    def get_data(self):
        pass


class UsersReport(Report):
    def __init__(self):
        self.headers = ['id', 'username', 'password', 'is_admin', 'created']

    def get_headers(self):
        return self.headers

    def get_data(self):
        records = UserActiveRecord.get_users()
        result = []
        for record in records:
            row = [record.id, record.username, record.password, record.is_admin, record.created]
            result.append(row)
        return result


class GroupsReport(Report):
    def get_headers(self):
        pass

    def get_data(self):
        pass


class ReportFactory:
    def __init__(self):
        self.cache = dict()

    def create_report(self, report_type):
        if report_type in self.cache:
            return self.cache[report_type]

        if report_type == ReportType.users:
            report = UsersReport()
        elif report_type == ReportType.groups:
            report = GroupsReport()
        else:
            raise ValueError('Unexpected report_type = ' + str(report_type))
        self.cache[report_type] = report
        return report
