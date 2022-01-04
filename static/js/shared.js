"use strict";
// Predefined keys for LS
const FILES_KEY = "currentCategoryIndex";
const HISTORY_KEY = "history";

class FileData {
    constructor(name, max_index = -1, path='/static/') {
        this._name = name;
        this._path = path;
        this._max_index = max_index;
        this._average_index = -1;
        this._maximal_index = 0;
        this._compared_with = [];
    }

    getFilePath(ext) {
        let filename = this.getFileName(ext);
        return this._path + ext + '/' + filename;
    }

    getFileName(ext) {
        return this._name.split('.')[0] + '.' + ext;
    }

    removeFromComparison(file_name) {
        for (let i = 0; i < this._compared_with.length; i++) {
            if (this._compared_with[i][0] === file_name) {
                this._compared_with.splice(i, 1);
                return;
            }
        }
    }

    calcAvgInd() {
        let sum_avg = 0;
        for (let i = 0; i < this._compared_with.length; i++) {
            sum_avg += this._compared_with[i][1];
        }

        if (sum_avg <= 0) {
            return -1;
        }

        return sum_avg / this._compared_with.length;
    }

    calcMaxInd() {
        let max = -1;
        for (let i = 0; i < this._compared_with.length; i++) {
            if (this._compared_with[i][1] > max) {
                max = this._compared_with[i][1];
            }
        }

        return max;
    }

    get compared_with() {

        return {
            'filename': this._name,
            'targets': [this._compared_with, this.calcAvgInd(), this.calcMaxInd()]
        }
    }

    set compared_with(value) {
        this._compared_with = [];
        for (let i = 0; i < value.length - 2; i++) {
            var file = [];

            file.push(value[i][0]); // file name
            file.push(value[i][1]); // index
            file.push(value[i][2]); // nodes

            this._compared_with.push(file);
        }

        this._average_index = value[value.length - 2];
        this._maximal_index = value[value.length - 1];
    }

    get length() {
        return this._compared_with.length;
    }

    get path() {
        return this._path;
    }

    set path(value='/static/pdf/') {
        this._path = value;
    }
    
    get name() {
        return this._name;
    }
    
    set name(value) {
        this._name = value;
    }

    get max_index() {
        if (this._max_index == -1) {
            return "";

        } else {
            return "<b>" + Math.fround(this._max_index * 100).toFixed(2) + "%</b>";
        }
    }

    set max_index(value) {
        this._max_index = value;
        this._maximal_index = value;
    }

    get maximal_index() {
        return this._maximal_index;
    }

    get average_index() {
        return this._average_index;
    }

    set average_index(value) {
        this._average_index = value;
    }

    /**
     * Retrieves the file data from local storage
     */
    fromData(data) {
        this._name = data._name;
        this._path = data._path;
        this._max_index = data._max_index;
        this._average_index = data._average_index;
        this._maximal_index = data._maximal_index;

        for (let i = 0; i < data._compared_with.length; i++) {
            var file = [];

            file.push(data._compared_with[i][0]);
            file.push(data._compared_with[i][1]);
            file.push(data._compared_with[i][2]);

            this._compared_with.push(file);
        }
    }
}

class Files {
    constructor() {
        this._files = [];
        }

    get files() {
        return this._files;
    }

    getFile(index) {
        return this._files[index];
    }

    getMaxIndex() {
        let max = -1;
        for (let i = 0; i < this._files.length; i++) {
            if (this._files[i].maximal_index > max) {
                max = this._files[i].maximal_index;
            }
        }

        if (max == -1) {
            return Math.fround(0.0 * 100).toFixed(2);
        } else {
            return Math.fround(max * 100).toFixed(2);
        }
    }

    getAvgIndex() {
        let sum_avg = 0;
        for (let i = 0; i < this._files.length; i++) {
            sum_avg += this._files[i].average_index;
        }


        if (sum_avg <= 0) {
            return Math.fround(0.0 * 100).toFixed(2);
        } else {
            return Math.fround(sum_avg / this._files.length * 100).toFixed(2);
        }
    }

    length() {
        return this._files.length;
    }

    splice(index, count) {
        this._files.splice(index, count);
    }

    indexOf(file) {        
        for (let i = 0; i < this._files.length; i++) {
            if (this._files[i].name == file) {
                return i;
            }
        }

        return -1;
    }

    append(files) {
        this._files.push(files);
    }

    clear() {
        length = this._files.length;
        for (let i = 0; i < length; i++) {
            var file = this._files.pop();
            file = null;
        }
    }

    /**
     * Retrieves the file data from local storage
     */
    fromData(data) {
        let f = data._files;
        for (let i = 0; i < f.length; i++) {
            let file = new FileData('');
            file.fromData(f[i]);
            
            this.append(file);
        }
    }
}

class History {
    constructor() {
        this._history = [];
    }

    get history() {
        return this._history;
    }

    set history(value) {
        this._history = value;
    }

    get length() {
        return this._history.length;
    }

    addHistory(data) {
        console.log("Creating history");
        let date = new Date();
        let d = new Files();
        d.fromData(data);

        // Insert the new data to start of the array
        this._history.unshift({
            'timestamp': [ this.getTime(date), this.getDate(date) ],
            'data': d
        });
    }

    getTime(date) {
        // return 12 Hour time
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var seconds = date.getSeconds();
        var ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;

        hours = hours ? hours : 12; // the hour '0' should be '12'


        hours = hours < 10 ? '0' + hours : hours;
        minutes = minutes < 10 ? ('0' + minutes) : minutes;
        seconds = seconds < 10 ? ('0' + seconds) : seconds;

        return hours + ':' + minutes + ':' + seconds + ' ' + ampm;
    }

    getDate(d) {
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        var date = d.getDate();
        date = date < 10 ? '0' + date : date;

        return date + "-" + (months[d.getMonth()]) + "-" + d.getFullYear();
    }
    
    fromData(data) {
        let history = data._history;

        for (let i = 0; i < history.length; i++) {
            let f = new Files();
            f.fromData(history[i].data);

            this._history.push({
                'timestamp': history[i].timestamp,
                'data': f
            });
        }
    }

}

function showSnackbar(message, duration, callback, action, color) {
    document.getElementById('show-snackbar').style.backgroundColor = color;
    var snackbarContainer = document.querySelector('#show-snackbar');

    snackbarContainer.MaterialSnackbar.showSnackbar({
        message: message,
        timeout: duration,
        actionHandler: callback,
        actionText: action
    });
}

function postRequest(data, contentType='undefined') {
    var request = new XMLHttpRequest();
    request.open('POST', '/multiple');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

    if (contentType != 'undefined') {
        request.setRequestHeader("Content-Type", contentType);
    }  

    request.send(data);

    return request;
}

function _base64ToArrayBuffer(base64) {
    var binary_string = atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    
    return bytes.buffer;
}

function saveReport(report, filename) {
    // convert report to array buffer
    var pdf_binary = _base64ToArrayBuffer(report);

    // create blob from array buffer of type pdf
    var blob = new Blob([pdf_binary], {type: "application/pdf"});

    var isIE = false || !!document.documentMode;
    if (isIE) {
        window.navigator.msSaveBlob(blob, filename);

    } else {
        var url = window.URL || window.webkitURL;
        var link = url.createObjectURL(blob);
        var a = document.createElement("a");
        a.setAttribute("download", filename);
        a.setAttribute("href", link);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkLSData(key)
{
    if (localStorage.getItem(key) != null)
    {
        return true;
    }
    return false;
}

function retrieveLSData(key)
{
    let data = localStorage.getItem(key);
    try
    {
        data = JSON.parse(data);
    }
    catch(err){}
    finally
    {
        return data;
    }
}

function updateLSData(key, data)
{
    let json = JSON.stringify(data);
    localStorage.setItem(key, json);
}

let files = new Files();
let history = new History();
let multipleFiles = [];

if (checkLSData(FILES_KEY))
{
    files.fromData(retrieveLSData(FILES_KEY));
}

if (checkLSData(HISTORY_KEY))
{
    history.fromData(retrieveLSData(HISTORY_KEY));
}
