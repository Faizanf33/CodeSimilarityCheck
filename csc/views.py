from django.http.response import HttpResponse
from django.shortcuts import render
from .form import UploadFileForm
from csc.functions.functions import handle_uploaded_file, compare_files, generate_report
from django.contrib import messages
from .add_to import add
from json import dumps, loads

from datetime import datetime
import os


def dashboard(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def history(request):
    return render(request, 'history.html')

# define function that reads files and returns a list of files in the directory


def upload_multiple_files(request):
    results = {
        'files': ["Hello", "World", "from", "upload_multiple_files"]
    }

    if request.method == 'POST':
        print("POST request was called")
        # form = UploadFileForm(request.POST, request.FILES)
        # check request content type is application/x-www-form-urlencoded

        if request.content_type == 'multipart/form-data':
            print("request.content_type: ", request.content_type)
            files = request.FILES.getlist('fileToUpload')
            print("request.FILES: ", len(files))

            for f in files:
                handle_uploaded_file(f)

            results = compare_files()

        elif request.content_type == 'text/plain':
            print("request.content_type: ", request.content_type)
            # print("request.body: ", request.body)

            # Parse request JSON body
            decoded = request.body.decode('utf-8')
            # print("decoded: ", decoded)

            json_data = loads(decoded)
            # print("json_data: ", json_data)

            # Key is the name of the file
            filename = json_data['filename']
            results = {
                filename: json_data['targets']
            }

            results = generate_report(filename, results)

    else:
        print("GET request was called")

    return HttpResponse(dumps(results))

    # return render(request, 'index.html', results)
