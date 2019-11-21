import json

from django.http import HttpResponse
from django.shortcuts import render

from polls.bussiness_logic.export_excel_controller import ExportExcelController, HandleExcelController


def index(request):
    if "GET" == request.method:
        return render(request, 'polls/index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        # data_input = ExportExcelController.build_data_pandas_from_input_file(excel_file)
        # # data_output = ExportExcelController.calculate_results(data_input)
        # output = ExportExcelController.export_excel(data_input)
        # response_data = HttpResponse(output.read(),
        #                              content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response_data['Content-Disposition'] = 'attachment; filename=%s' % 'results.xlsx'

        handle_controller = HandleExcelController(data_input=excel_file, sheet_name="Input data")
        error = handle_controller.validate_data(fields_validate=["name", "primary_category"])
        if len(error):
            return render(request, 'polls/index.html', {'error': error})
        output = handle_controller.export_json_data(default_value="null")
        response_data = HttpResponse(json.dumps(output),
                                     content_type='application/json')
        response_data['Content-Disposition'] = 'attachment; filename={}'.format("data.json")
        return response_data
