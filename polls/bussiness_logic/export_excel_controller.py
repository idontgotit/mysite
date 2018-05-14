from io import BytesIO  # for modern python

import pandas as pd
from traitlets import Bunch
from xlsxwriter import worksheet


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
        for index in writer.sheets:
            sheet = writer.sheets.get(index)
            sheet.write_formula(0, 15, "=COUNTIFS(K:K\|K4)/COUNTIFS(K:K\|K1)")
            sheet.write_formula(1, 15, "=AVERAGEIFS(E:E\|K:K\|K4)")
            sheet.write_formula(2, 15, "=AVERAGEIFS(E:E\|K:K\|K4)")
            sheet.write_formula(3, 15, "=Q3/SUM($Q$3:$Q$5)")
            sheet.write_formula(4, 15, "=Q4/SUM($Q$3:$Q$5)")
            sheet.write_formula(5, 15, "=Q5/SUM($Q$3:$Q$5)")

            sheet.write_formula(2, 16, '=COUNTIFS(K:K\|K4|E:E\|"<5")')
            sheet.write_formula(3, 16, '=COUNTIFS(K:K\|K4;E:E\|">5"\|E:E\|"<10")')
            sheet.write_formula(4, 16, '=COUNTIFS(K:K\|K4;E:E\|">10")')
        writer.save()
        output.seek(0)
        return output

    @staticmethod
    def build_data_pandas_from_input_file(data):
        # build data from 8am-23pm
        data_excel = data.file
        name_split = data.name.split('.')
        format_file = name_split[len(name_split) - 1]
        if '.csv' in format_file:
            df = pd.read_csv(data_excel, header=0, skip_blank_lines=True,
                             skipinitialspace=True, encoding='utf8')
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
