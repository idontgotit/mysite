from io import BytesIO  # for modern python

import pandas as pd
from traitlets import Bunch
from xlsxwriter import worksheet
import numpy as np
from datetime import datetime


class ExportExcelController:
    @staticmethod
    def export_excel(data_input):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        # data_input.df_filter8.to_excel(writer, '8', index=False, header=False)
        count = 8
        for item in data_input.df_filter8:
            item.to_excel(writer, str(count), index=False, header=False)
            count += 1
        # for index in writer.sheets:
        #             sheet = writer.sheets.get(index)
        #             sheet.write(4, 10, 'END_CLICKBUTTON_LS')
        #             sheet.write(0, 15, "=COUNTIFS(K:K|K4)/COUNTIFS(K:K|K1)")
        #             sheet.write(1, 15, "=AVERAGEIFS(E:E|K:K|K4)")
        #             sheet.write(2, 15, "=AVERAGEIFS(E:E|K:K|K4)")
        #             sheet.write(3, 15, "=Q3/SUM($Q$3:$Q$5)")
        #             sheet.write(4, 15, "=Q4/SUM($Q$3:$Q$5)")
        #             sheet.write(5, 15, "=Q5/SUM($Q$3:$Q$5)")

        #             sheet.write(2, 16, '=COUNTIFS(K:K|K4|E:E|"<5")')
        #             sheet.write(3, 16, '=COUNTIFS(K:K|K4;E:E|">5"|E:E|"<10")')
        #             sheet.write(4, 16, '=COUNTIFS(K:K|K4;E:E|">10")')

        workbook = writer.book
        worksheet = workbook.add_worksheet(name='total')
        writer.save()
        output.seek(0)
        return output

    @staticmethod
    def build_data_pandas_from_input_file(data):
        # build data from 8am-23pm
        data_excel = data.file
        name_split = data.name.split('.')
        format_file = name_split[len(name_split) - 1]
        if 'csv' in format_file:
            df = pd.read_csv(data_excel, header=0, encoding='utf8')
        else:
            df = pd.read_excel(data_excel, header=0, encoding='utf8')

        date_current = str(df['date'][0]).split(' ')[0]
        # df['number'] = df['number'].replace('.', ',')
        df_filter8 = [df[(df['date'] > date_current + ' 07:00:00') & (df['date'] < date_current + ' 09:00:00')]]
        for i in range(9, 23):
            df_filter8.append(
                df[(df['date'] > date_current + ' ' + str(i).zfill(2) + ':00:00') & (
                    df['date'] < date_current + ' ' + str(i + 1).zfill(2) + ':00:00')])
        df_filter8.append(
            df[(df['date'] > date_current + ' ' + str(23).zfill(2) + ':00:00') & (
                df['date'] < date_current + ' ' + str(23).zfill(2) + ':59:59')])
        data_input = Bunch()
        data_input.df_filter8 = df_filter8
        return data_input

    @staticmethod
    def calculate_results(data):
        results = []
        index = 0
        for item in data.df_filter8:
            value = pd.Series(['x', 'y', 'z'])
            item.insert(loc=11, column='P', value=value)
            results.append(item)
        data_output = Bunch()
        data_output.df_filter8 = results
        return data_output


ERROR_STRING = "Column: {} in row: {} is required"
PLUS_VALUE_HEADER_EXCEL = 2


class BaseExcelController:
    def __init__(self, data_input, sheet_name):
        self.data = pd.read_excel(data_input.file, sheet_name=sheet_name, encoding='utf8')
        self.empty_line = []

    def __update_default_value(self, data_frame, default_value):
        list_header_name = list(data_frame)
        for index_header in list_header_name:
            data_frame[index_header] = data_frame[index_header].fillna(default_value)
        return data_frame

    def validate_data(self, fields_validate):
        error = []
        null_array = []
        empty_line = []
        validate_error = {}
        df = self.data
        for field in fields_validate:
            temp_null = np.where(pd.isnull(df[field]))[0].tolist()
            validate_error[field] = temp_null
            null_array += temp_null
        for i in set(null_array):
            if df.iloc[i].notnull().values.any():
                for key, value in validate_error.items():
                    if i in value:
                        error.append(ERROR_STRING.format(key, i + PLUS_VALUE_HEADER_EXCEL))
            else:
                empty_line.append(i)
        self.empty_line = empty_line
        return error

    def export_json_data(self, default_value):
        result = []
        empty_line = self.empty_line
        data_frame = self.data
        list_header_name = list(data_frame)
        data_frame = self.__update_default_value(data_frame, default_value)
        for index in range(0, len(data_frame.index)):
            if index in empty_line:
                continue
            temp_item = {}
            for index_header in list_header_name:
                temp_item.update({
                    index_header: data_frame[index_header].get(index)
                })
            result.append(temp_item)
        return result


class HandleExcelController(BaseExcelController):
    def export_json_data(self, default_value):
        data = super(HandleExcelController, self).export_json_data(default_value)
        return {
            "data": data,
            "updated_at": round(datetime.now().timestamp() * 1000)
        }
