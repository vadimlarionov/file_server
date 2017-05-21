import csv
import io
import os
import random
from abc import abstractclassmethod
from enum import Enum

import pdfkit
from django.template import Context
from django.template.loader import get_template

from admin_app.group.groups import Group
from admin_app.user.user import User


class ReportType(Enum):
    users_csv = 1
    groups_csv = 2
    users_pdf = 3
    groups_pdf = 4


class Report:
    @abstractclassmethod
    def get_report(self):
        pass


class UsersReport(Report):
    @abstractclassmethod
    def get_report(self):
        pass

    def __init__(self):
        self.__headers = ['id', 'username', 'password', 'is_admin', 'created']

    def get_headers(self):
        return self.__headers

    @staticmethod
    def get_data():
        records = User.get_all_users()
        result = []
        for record in records:
            row = [record.id, record.username, record.password, record.is_admin, record.created]
            result.append(row)
        return result


class UsersReportCSV(UsersReport):
    def get_report(self):
        return ReportRender.create_csv(self.get_headers(), self.get_data())


class UsersReportPDF(UsersReport):
    def get_report(self):
        return ReportRender.create_pdf(self.get_headers(), self.get_data())


class GroupsReport(Report):
    @abstractclassmethod
    def get_report(self):
        pass

    def __init__(self):
        self.__headers = ['id', 'title', 'created', 'is_deleted']

    def get_headers(self):
        return self.__headers

    @staticmethod
    def get_data():
        records = Group.get_all_groups()
        result = []
        for record in records:
            row = [record.id, record.title, record.created, record.is_deleted]
            result.append(row)
        return result


class GroupsReportCSV(GroupsReport):
    def get_report(self):
        return ReportRender.create_csv(self.get_headers(), self.get_data())


class GroupsReportPDF(GroupsReport):
    def get_report(self):
        return ReportRender.create_pdf(self.get_headers(), self.get_data())


class ReportFactory:
    def __init__(self):
        self.cache = dict()

    def create_report(self, report_type):
        if report_type in self.cache:
            return self.cache[report_type]

        if report_type == ReportType.users_csv:
            report = UsersReportCSV()
        elif report_type == ReportType.users_pdf:
            report = UsersReportPDF()
        elif report_type == ReportType.groups_csv:
            report = GroupsReportCSV()
        elif report_type == ReportType.groups_pdf:
            report = GroupsReportPDF()
        else:
            raise ValueError('Unexpected report_type = ' + str(report_type))
        self.cache[report_type] = report
        return report


class ReportRender:
    @staticmethod
    def create_pdf(headers, data):
        template = get_template('admin/report.html')
        context = Context({'data': data, 'headers': headers})
        html = template.render(context)
        pdf_file = 'out' + str(random.randint(0, 1000)) + 'pdf'
        pdfkit.from_string(html, pdf_file)
        with open(pdf_file, 'rb') as pdf:
            result = pdf.read()
        os.remove(pdf_file)
        return result

    @staticmethod
    def create_csv(headers, data):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
        return output.getvalue()
