from django.http import HttpResponse
from django.shortcuts import render

from polls.bussiness_logic.export_excel_controller import ExportExcelController


def index(request):
    if "GET" == request.method:
        return render(request, 'polls/index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        data = excel_file.file
        data_input = ExportExcelController.build_data_pandas_from_csv(data)
        output = ExportExcelController.export_excel(data_input)
        response_data = HttpResponse(output.read(),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response_data['Content-Disposition'] = 'attachment; filename=%s' % 'results.xlsx'
        return response_data
