from io import BytesIO  # for modern python

import pandas as pd
from traitlets import Bunch


class ExportExcelController:
    @staticmethod
    def export_excel(data_input):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        data_input.df_filter8.to_excel(writer, '8', index=False, header=False)
        count = 9
        for item in data_input.data_from9:
            item.to_excel(writer, str(count), index=False, header=False)
            count += 1
        writer.save()
        output.seek(0)
        return output

    @staticmethod
    def build_data_pandas_from_csv(data):
        # build data from 8am-23pm
        df = pd.read_csv(data, header=0, skip_blank_lines=True,
                         skipinitialspace=True, encoding='utf8', sep='delimiter')
        date_current = df['0'][0].split(' ')[0]
        df_filter8 = df[(df['0'] > date_current + ' 07:00:00') & (df['0'] < date_current + ' 09:00:00')]
        data_from9 = []
        for i in range(9, 23):
            data_from9.append(
                df[(df['0'] > date_current + ' ' + str(i).zfill(2) + ':00:00') & (
                    df['0'] < date_current + ' ' + str(i + 1).zfill(2) + ':00:00')])
        data_input = Bunch()
        data_input.df_filter8 = df_filter8
        data_input.data_from9 = data_from9
        return data_input
