"use strict";

function createAccordion() {
    var accordion = document.getElementById('accordion-list');
    accordion.innerHTML = "";

    if (history.history.length == 0) {
        accordion.innerHTML = '<h5 style="color: cadetblue;">'
        + '<span>You have not submitted any code yet! </span>'
        + '<a href="/">Go to dashboard</a>'
        + '</h5><br>';

        return;

    } else {
        for (var i = 0; i < history.length; i++) {
            let inner = '';
            let h = history.history[i]
            let data = h.data;
            let timestamp = h.timestamp;
    
            inner += '<button class="accordion">';
            inner +=    '<span>Check - ' + (i + 1) + ' performed at ' + timestamp[0] + ' on ' + timestamp[1] + ' among ' + data.length() + ' files</span>';
            inner +=    '<i class="mdl-button mdl-js-button mdl-button--icon mdl-js-ripple-effect material-icons" style="color:white; float:right; width:auto; height:auto" onclick="removeList('+i+')">delete</i>'
            inner += '</button>';
            inner += '<div class="panel" style="width:100%; margin-bottom:5px">';
            inner +=    '<div class="mdl-cell mdl-cell--12-col mdl-cell--12-col-tablet mdl-cell--12-col-phone" style="max-height: 410px; overflow-x: auto; overflow-y: auto;">';
            inner +=        '<table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp" style="width:100%;">';
            inner +=            '<thead>';
            inner +=                '<tr>';
            inner +=                   '<th class="mdl-data-table__cell--non-numeric">#</th>';
            inner +=                   '<th class="mdl-data-table__cell--non-numeric" style="width: 60%;">File Name</th>';
            inner +=                   '<th class="mdl-data-table__cell--non-numeric" style="width: 40%;">Max. Similarity</th>';
            inner +=                   '<th class="mdl-data-table__cell--non-numeric">Report</th>';
            inner +=                   '<th class="mdl-data-table__cell--non-numeric">Remove</th>';
            inner +=                '</tr>';
            inner +=             '</thead>';
            inner +=             '<tbody>';
            inner +=                createTable(data, i);
            inner +=             '</tbody>';
            inner +=        '</table>';
            inner +=    '</div>';
            inner += '</div>';
            
            accordion.innerHTML += inner;
            createProgressBars(data);
            componentHandler.upgradeElement(accordion);
        }
          
    
        for (var i = 0; i < history.length; i++) {
            createTable(history.history[i].data, i);

            document.getElementsByClassName('accordion')[i].addEventListener('click', function() {
                // get this accordion's index
                this.classList.toggle('is-active');
                var panel = this.nextElementSibling;
    
                if (panel.style.maxHeight) {
                    panel.style.maxHeight = null;
                    panel.style.borderBottom = "none";
                }
    
                else {
                    panel.style.maxHeight = panel.scrollHeight + "px";
                    panel.style.borderBottom = "3px solid darkseagreen";
                  }              
            });

            componentHandler.upgradeElement(document.getElementsByClassName('accordion')[i]);
            componentHandler.upgradeDom();                
        }
    }
}

let tempList = [];

function removeList(index) {
  tempList = history.history.splice(index, 1);
  
  showSnackbar('History entry removed', 4000, function() {
    // Insert the removed list back into the history at the same index
    if (tempList.length > 0) {
        history.history.splice(index, 0, tempList[0]);
        updateLSData(HISTORY_KEY, history);
        createAccordion();
        tempList = [];
    }
  }, 'Undo', 'chocolate');
  
  updateLSData(HISTORY_KEY, history);
  createAccordion();
}

function createTable(data, index) {
    console.log("Creating table for " + data.length() + " files");
    
    if (data.length() == 0) {
        return '<tr><td colspan="5" class="mdl-data-table__cell--non-numeric">No file selected</td></tr>';

    } else {    
        return createRows(data, index);
    }
}

function createRows(data, index) {
  var inner = "";
  for (var i = 0; i < data.length(); i++) {
      inner += '<tr id="tr' + i + '">';
      inner += '<td class="mdl-data-table__cell--non-numeric">' + (i+1) + '</td>';
      inner += '<td class="mdl-data-table__cell--non-numeric">' + data.getFile(i).name + '</td>';
      inner += '<td class="mdl-data-table__cell--non-numeric">' + data.getFile(i).max_index;
      inner += '<div id="progress' + i + '" class="mdl-progress mdl-js-progress" style="width:100%">';
      inner += '</div></td>';
      inner += '<td class="mdl-data-table__cell--non-numeric">';
      inner += '<div id="saveBtn' + i + '" class="mdl-spinner mdl-js-spinner">';
      inner += '<button class="mdl-button mdl-js-button mdl-button--icon mdl-js-ripple-effect" style="color: cadetblue;" onclick="saveFile('+ index +','+ i + ')">'
      inner += '<i class="material-icons">file_download</i>'
      inner += '</button>'
      inner += '</div>'
      inner += '</td>'
      inner += '<td class="mdl-data-table__cell--non-numeric">'
      inner += '<button class="mdl-button mdl-js-button mdl-button--icon mdl-js-ripple-effect" style="color: chocolate;" onclick="removeFile('+ index +','+ i + ')">'
      inner += '<i class="material-icons">delete</i>'
      inner += '</button>'
      inner += '</td>'
      inner += '</tr>'
  }

  return inner;
}

function createProgressBars(data) {
    console.log("Creating progress bars for " + data.length() + " files");
    for (var i = 0; i < data.length(); i++) {
        let max_index = parseInt(data.getFile(i).calcMaxInd() * 100);
      
        var progress = document.querySelector('#progress' + i)
        progress.addEventListener('mdl-componentupgraded', 
            function() {
                this.MaterialProgress.setProgress(max_index);
        });
        componentHandler.upgradeElement(progress);
        componentHandler.upgradeDom();
    }
}


function removeFile(hi, index) {
    let data = history.history[hi].data;

    data.splice(index, 1);
    history.history[hi].data = data;

    createTable(data, hi);

    updateLSData(HISTORY_KEY, history);
}


function saveFile(hi, i) {
    var data = history.history[hi].data;
    var filename = data.getFile(i).name;
    
    // Add mdl spinner instead of button and upgrade element
    var saveBtn = document.getElementById('saveBtn' + i);
    saveBtn.innerHTML = '<div class="mdl-spinner mdl-js-spinner is-active" style="background:transparent; color: transparent; display:flex" ></div>';
    componentHandler.upgradeElement(saveBtn.querySelector('.mdl-spinner'));
    componentHandler.upgradeDom();

    var request = postRequest(JSON.stringify(data.getFile(i).compared_with), 'text/plain');
    
    console.log("Saving file: " + filename);

    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200) {

            var response = JSON.parse(request.responseText);

            let inner = ''
            inner += '<div id="saveBtn' + i + '" class="mdl-spinner mdl-js-spinner">'
            inner += '<button class="mdl-button mdl-js-button mdl-button--icon mdl-js-ripple-effect" style="color: cadetblue;" onclick="saveFile('+ hi +','+ i + ')">'
            inner += '<i class="material-icons">file_download</i>'
            inner += '</button>'
            inner += '</div>'

            if ('success' in response) {
                console.log("success - pdf");
                saveBtn.innerHTML = inner;

                var pdf_name = data.getFile(i).getFileName('pdf');

                saveReport(response.success.report, pdf_name);
                                
                console.log("Saved file: " + pdf_name);

            } else {
                console.log("error - pdf");
                saveBtn.innerHTML = inner;
                
                showSnackbar(response.error.message + ': ' + response.error.files, 3000, function() {
                  clearFiles();
                }, 'Clear', 'chocolate');
            }
            componentHandler.upgradeElement(saveBtn.querySelector('.mdl-spinner'));            
        }
    };
}

createAccordion();