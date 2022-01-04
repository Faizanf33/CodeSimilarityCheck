"use strict";

var fileInput = document.getElementById('fileToUpload');
fileInput.addEventListener('change', function(e) {
    var fileList = e.target.files;

    for (var i = 0; i < fileList.length; i++) {
        var file = new FileData(fileList[i].name);
        files.append(file);
        multipleFiles.push(fileList[i]);
    }

    createTable(files);
});

function uploadFiles() {
    var formData = new FormData();
    console.log("Files to send: " + multipleFiles.length);

    if (multipleFiles.length > 1) {
        for (var i = 0; i < multipleFiles.length; i++) {
            formData.append('fileToUpload', multipleFiles[i]);
        }

        var request = postRequest(formData);
        createProgressBarsIndeterminate(files);

        request.onreadystatechange = function() {
            if (request.readyState == 4 && request.status == 200) {
                console.log("Request finished");

                var response = JSON.parse(request.responseText);

                if ('error' in response) {
                    console.log("failure - json");
                    console.log(response)

                    createProgressBarsValued(files);

                    for (let file of response.error.files) {
                        highlightTableRow(files.indexOf(file));
                    }

                    showSnackbar("Invalid Syntax (remove file(s) to continue)", 5000, function() {
                        for (let file of response.error.files)
                            removeFile(files, files.indexOf(file), false);

                        createTable(files)
                        return uploadFiles();

                    }, 'Remove', 'chocolate');

                } else {
                    console.log("success - json");
                    console.log(response);
                    // readLoadJSON('static/json/results.json');
                    readLoadJSON(response)
                    createProgressBarsValued(files);
                    showSnackbar( "Progress Saved To History Page", 3000, function() {
                        window.location.href = "/history";
                    }, "Open History", 'cadetblue');
                }
            }
        }

    } else {
        showSnackbar("Clear And Upload Again! ", 3000, function() {
            return clearFiles();
            }, "Clear", 'chocolate');
    }

}


function createTable(files) {

    document.getElementById('tableData').innerHTML = createRows(files);
    createProgressBarsValued(files);

    var file_count = document.getElementById('files');

    document.getElementById('max-index').innerHTML = files.getMaxIndex() + "%";
    document.getElementById('avg-index').innerHTML = files.getAvgIndex() + "%";

    var interval_f = setInterval(function() {
        if ( file_count.innerText > files.length() ) file_count.innerText--;
        else if ( file_count.innerText < files.length() ) file_count.innerText++;
        else clearInterval(interval_f);
    }, 50);


    if (files.length() > 1) {
        document.getElementById('form-submit').disabled = false;
        document.getElementById('form-clear').disabled = false;


    } else {
        document.getElementById('form-submit').disabled = true;
    }

    if (files.length() == 0) {
        document.getElementById('tableData').innerHTML = '<tr><td colspan="5" class="mdl-data-table__cell--non-numeric">No file selected</td></tr>';
        document.getElementById('form-clear').disabled = true;
    }

    updateLSData(FILES_KEY, files)
}

function createRows(files) {
    var inner = "";
    for (var i = 0; i < files.length(); i++) {
        inner += '<tr id="tr' + i + '">';
        inner += '<td class="mdl-data-table__cell--non-numeric">' + (i+1) + '</td>';
        inner += '<td class="mdl-data-table__cell--non-numeric">' + files.getFile(i).name + '</td>';
        inner += '<td class="mdl-data-table__cell--non-numeric">' + files.getFile(i).max_index;
        inner += '<div id="progress' + i + '" class="mdl-progress mdl-js-progress" style="width:100%">';
        inner += '</div></td>';
        inner += '<td class="mdl-data-table__cell--non-numeric">';
        inner += '<div id="saveBtn' + i + '" class="mdl-spinner mdl-js-spinner">';
        inner += '<button class="mdl-button mdl-js-button mdl-button--icon mdl-js-ripple-effect" style="color: cadetblue;" onclick="save(' + i + ')">'
        inner += '<i class="material-icons">file_download</i>'
        inner += '</button>'
        inner += '</div>'
        inner += '</td>'
        inner += '<td class="mdl-data-table__cell--non-numeric">'
        inner += '<button class="mdl-button mdl-js-button mdl-button--icon mdl-js-ripple-effect" style="color: chocolate;" onclick="removeFile(' + i + ')">'
        inner += '<i class="material-icons">delete</i>'
        inner += '</button>'
        inner += '</td>'
        inner += '</tr>'
    }

    return inner;
}

function readLoadJSON(json) {
    for (var i = 0; i < files.length(); i++) {
        var file = files.getFile(i).name;
        files.getFile(i).max_index = json[file].at(-1);
        files.getFile(i).average_index = json[file].at(-2);

        files.getFile(i).compared_with = json[file]
    }

    updateLSData(FILES_KEY, files);
    createTable(files);

    history.addHistory(files);
    updateLSData(HISTORY_KEY, history);


    for (var i = 0; i < files.length(); i++) {
        var file = files.getFile(i).name;
    }
}


function highlightTableRow(index) {
    let tr = document.getElementById('tr'+index);
    tr.style.backgroundColor = '#ffcdd2';
}


function createProgressBarsValued(files) {
    for (var i = 0; i < files.length(); i++) {
        var progress = document.querySelector('#progress' + i)
        
        progress.classList.remove('mdl-progress__indeterminate');
        
        progress.addEventListener('mdl-componentupgraded', 
            function() {
                this.MaterialProgress.setProgress(parseInt(files.getFile(i).calcMaxInd() * 100));
        });

        componentHandler.upgradeElement(progress);        
    }
}

function createProgressBarsIndeterminate(files) {
    for (var i = 0; i < files.length(); i++) {
        // mdl-progress__indeterminate
        var progress = document.querySelector('#progress' + i)        
        progress.classList.add('mdl-progress__indeterminate');
        // upgrade element
        componentHandler.upgradeElement(progress);        
        
    }
}

function save(i) {
    var filename = files.getFile(i).name;
    if (files.getFile(i).length == 0) {
        showSnackbar("Error: Missing file - " + files.getFile(i).getFileName('pdf'), 3000, function() {
            return uploadFiles();
            // do nothing
        } , 'Ok', 'chocolate');
        return;
    }
    
    // Add mdl spinner instead of button and upgrade element
    var saveBtn = document.getElementById('saveBtn' + i);
    saveBtn.innerHTML = '<div class="mdl-spinner mdl-js-spinner is-active" style="background-color: transparent; color:white;"></div>';
    componentHandler.upgradeElement(saveBtn.querySelector('.mdl-spinner'));
 
    console.log(files.getFile(i).compared_with);
    var request = postRequest(JSON.stringify(files.getFile(i).compared_with), 'text/plain');
    
    console.log("Saving file: " + filename);

    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200) {

            var response = JSON.parse(request.responseText);

            let inner = ''
            inner += '<div id="saveBtn' + i + '" class="mdl-spinner mdl-js-spinner">'
            inner += '<button class="mdl-button mdl-js-button mdl-button--icon mdl-js-ripple-effect" style="color: cadetblue;" onclick="save(' + i + ')">'
            inner += '<i class="material-icons">file_download</i>'
            inner += '</button>'
            inner += '</div>'

            if ('success' in response) {
                console.log("success - pdf");
                console.log(response);
                saveBtn.innerHTML = inner;

                // responseText.file is file read in binary mode and is a string                
                var blob = new Blob([response.file], {type: "application/pdf;base64"});

                // open a new window with the PDF file and set the filename.
                var fileURL = URL.createObjectURL(blob);
                window.open(fileURL, files.getFile(i).getFileName('pdf'));
                
                // var link = document.createElement('a');
                // link.href = window.URL.createObjectURL(blob);
                // link.download = files.getFile(i).getFileName('pdf');
                // link.click();

                // var relative_filename = files.getFile(i).getFilePath('pdf');            
                // console.log("Saved file " + filename + " to " + relative_filename);
                // saveFile(relative_filename, i);

            } else {
                console.log("error - pdf");
                saveBtn.innerHTML = inner;

                showSnackbar(response.error.message + ': ' + response.error.files, 3000, function() {
                    clearFiles();
                }, 'Clear', 'chocolate');
            }
   
        }
    };
}


function saveFile(file, i) {
    fetch(file).then(response => response.blob()).then(blob => {

        var isIE = false || !!document.documentMode;
        if (isIE) {
            window.navigator.msSaveBlob(blob, files.getFile(i).getFileName('pdf'));

        } else {
            var url = window.URL || window.webkitURL;
            var link = url.createObjectURL(blob);
            var a = document.createElement("a");
            a.setAttribute("download", files.getFile(i).getFileName('pdf'));
            a.setAttribute("href", link);
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    });
} 

function removeFile(index, re_create=true) {
    files.splice(index, 1);
    multipleFiles.splice(index, 1);
    if (re_create) createTable(files);
}


function clearFiles() {
    files.clear();
    length = multipleFiles.length;
    for (var i = 0; i < length; i++) {
        multipleFiles.pop();
    }
    createTable(files);
}


// At load
createTable(files);