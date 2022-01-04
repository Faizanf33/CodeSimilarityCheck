import os
from csc.functions.ast_comparison import compare_many
from csc.functions.pdf_report import PDFReport
from csc.functions.custom_exception import CustomException

from multiprocessing import Process
from json import dumps


def handle_uploaded_file(f):
    if os.getcwd().endswith('static'):
        os.chdir('..')

    path = os.path.join(os.getcwd(), 'static', 'dataset')
    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, f.name), 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def compare_files():

    if os.getcwd().endswith('static'):
        os.chdir('..')

    # save current working directory
    current_dir = os.getcwd()

    # get all files from 'dataset' directory
    path = os.path.join(current_dir, 'static', 'dataset')

    # change working directory to 'dataset'
    os.chdir(path)

    files = os.listdir()
    print("Comparing {} files".format(len(files)))

    results = {}
    try:
        results = compare_many(files)

    except CustomException as e:
        print(e)
        results = {
            'error': {
                'message': str(e),
                'files': e.args
            }
        }

    # change working directory to current directory

    print("Done comparing files")

    # remove all files from 'dataset' directory
    for file in files:
        os.remove(file)

    print("Removed all files from 'dataset' directory")

    # change working directory to current directory
    os.chdir(current_dir)

    return results


def generate_report(filename, results):
    # save current working directory

    if os.getcwd().endswith('static'):
        os.chdir('..')

    current_dir = os.getcwd()

    print("Current directory: ", current_dir)

    path = os.path.join(current_dir, 'static', 'json')
    if not os.path.exists(path):
        os.makedirs(path)

    targets = []

    try:
        # # Save results to a json file
        with open(os.path.join(path, filename.split('.')[0] + '.json'), 'w') as f:
            json_data = dumps(results)
            f.write(json_data)

        targets = results[filename]

    except (FileNotFoundError, KeyError) as e:
        print("Error " + str(e))
        results = {
            'error': {
                'message': "File Not Found!",
                'files': [filename]
            }
        }

        return results

    # change working directory to 'static'
    path = os.path.join(current_dir, 'static')

    os.chdir(path)

    if not os.path.exists('pdf'):
        os.makedirs('pdf')

    print("Generating report for {}".format(filename))
    print("{} targets found".format(len(targets)))

    # create a new PDFReport object
    pdf = PDFReport(filename, targets[0],
                    (targets[-2], targets[-1]), out_dir='pdf')
    # pdf.generate_report()

    # generate report using multiprocessing
    p = Process(target=pdf.generate_report)
    p.start()
    p.join()

    print("Saved report to {}".format(os.path.join(path, 'pdf')))

    # If file exists open it in new tab of current browser
    if os.path.exists(os.path.join(path, 'pdf', filename.split('.')[0] + '.pdf')):
        print("File exists")
        os.system('open -a "Google Chrome" {}'.format(os.path.join(path,
                  'pdf', filename.split('.')[0] + '.pdf')))

    # change working directory to current directory
    os.chdir(current_dir)

    results = {
        'success': {
            'message': 'Report generated successfully',
            'files': [filename]
        }
    }

    return results
