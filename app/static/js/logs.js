"use strict";

const storage = {};

function getLogs() {
    const params = getSearchParams();
    fetch(params);
}

function clearSearchParams() {
    $('#type').val('');
    $('#user').val('');
    $('#action').val(''); 
    setInitialDate();
    getLogs();   
}

function getSearchParams() {
    return {
        'type': $('#type').val(),
        'user': $('#user').val(),
        'action': $('#action').val(),
        'date_gt': $('#dateGt').data('value'),
        'date_lt': $('#dateLt').data('value')
    }
}

function beforeFetch() {
    $('#loader').show();
    $('#logs-empty').hide();
}

function afterFetch() {
    $('#loader').hide();
    if (!storage.logs || storage.logs.length == 0) {
        $('#logs-empty').show();
    }
}

function fetch(data) {
    $.ajax({
        url: '/logs/',
        method: 'post',
        data: data || {},
        beforeSend: () => {
            beforeFetch();
        },
        success: (response) => {
            if (response.logs) {
                storage.logs = response.logs.map((value) => {
                    value.created_at = new Date(value.created_at);
                    return value;
                });
                renderTable();
            }
        },
        error: () => {
            alert('error while fetching data from a server');
        },
        complete: () => {
            afterFetch();
        }
    })
}

function getTableTemplate(logs) {
    let html = '';
    for (const log of logs) {
        html += `
            <tr>
                <td>${log.user_id}</td>
                <td>${log.email}</td>
                <td>${log.type}</td>
                <td>${log.action}</td>
                <td>${log.url}</td>
                <td>${moment(log.created_at).format('DD.MM.YYYY HH:mm:ss')}</td>
            </tr>    
        `
    }
    return html;
}

function renderTable() {
    if (!storage.logs || storage.logs.length == 0) {
        $('#logs-empty').show();
        $('#table-content').empty();
        $('#pagination-control').empty();
    } else {
        $('#pagination-control').pagination({
            dataSource: storage.logs,
            pageSize: 10,
            callback: function(data, pagination) {
                const html = getTableTemplate(data);
                $('#table-content').html(html);
            }
        });
    }
}

function asc(x, y) {
    if (this.type == 'number' || this.type == 'date') {
        return x[this.field] - y[this.field];
    } else if (this.type == 'string') {
        if (x[this.field] < y[this.field]) return -1;
        if (x[this.field] > y[this.field]) return 1;
        return 0;
    }
}

function dsc(x, y) {
    if (this.type == 'number' || this.type == 'date') {
        return y[this.field] - x[this.field];
    } else if (this.type == 'string') {
        if (y[this.field] < x[this.field]) return -1;
        if (y[this.field] > x[this.field]) return 1;
        return 0;
    }
}

function sortByField(obj) {
    const $obj = $(obj);

    let sortFunc = null;
    if ($obj.data('sorted') == 'asc') {
        sortFunc = dsc;
        $obj.data('sorted', 'dsc');
    } else {
        sortFunc = asc;
        $obj.data('sorted', 'asc');
    }
    const ctx = {
        field: $obj.data('field'),
        type: $obj.data('type')
    }

    storage.logs.sort(sortFunc.bind(ctx));
    renderTable();
}

function setInitialDate() {
    const start = moment().startOf('month');
    const end = moment().endOf('month');
    const dateGt = $('#dateGt');
    const dateLt = $('#dateLt');
    dateGt.val(start.format('DD.MM.YYYY'));
    dateLt.val(end.format('DD.MM.YYYY'));
    dateGt.data('value', start.format('YYYY-MM-DD'));
    dateLt.data('value', end.format('YYYY-MM-DD'));
}

function transformDateForSearchQuery(obj) {
    const $obj = $(obj);
    const date = $obj.val().split('.');
    if (date.length == 3) {
        const transformed = `${date[2]}-${date[1]}-${date[0]}`;
        $(obj).data('value', transformed);
    }
}