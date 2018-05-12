from io import BytesIO  # for modern python

import pandas as pd
from traitlets import Bunch


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
                             skipinitialspace=True, encoding='utf8', sep=',')
        else:
            df = pd.read_excel(data_excel, header=0, skip_blank_lines=True,
                               skipinitialspace=True, encoding='utf8', sep=',')

        date_current = str(df['date'][0]).split(' ')[0]
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
