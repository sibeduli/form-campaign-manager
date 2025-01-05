$(document).ready(function () {
    var table = $('#formLinksTable').DataTable({
        orderCellsTop: true,
        fixedHeader: true,
        scrollCollapse: true,
        scrollY: '450px',
        scrollX: true,
        fixedColumns: {
            start: 3,
            end: 1
        },
        ajax: {
            url: '/api/form-link-manager',
            dataSrc: function (json) {
                return Array.isArray(json) ? json : [json];
            }
        },
        columns: [
            { data: 'id', className: 'text-nowrap text-sm dark:text-white' },
            {
                data: 'status',
                className: 'text-nowrap text-sm dark:text-white',
                render: function (data, type, row) {
                    if (data === 'unopened') {
                        return `<span
                                class="rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-medium text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300">
                                Unopened
                                </span>`;
                    } else if (data === 'viewed') {
                        return `<span
                                class="rounded-full bg-violet-100 px-2.5 py-0.5 text-xs font-medium text-violet-800 dark:bg-violet-900 dark:text-violet-300">
                                Viewed
                                </span>`;
                    } else if (data === 'submitted') {
                        return `<span
                                class="rounded-full bg-pink-100 px-2.5 py-0.5 text-xs font-medium text-pink-800 dark:bg-pink-900 dark:text-pink-300">
                                Submitted
                                </span>`;
                    } else {
                        return `<span
                                class="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800 dark:bg-gray-900 dark:text-gray-300">
                                ${data}
                                </span>`;
                    }
                }
            },
            { data: 'created_time', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'viewed_time', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'submitted_time', className: 'text-nowrap text-sm dark:text-white' },
            {
                data: null,
                className: 'text-nowrap text-sm dark:text-white',
                render: function (data, type, row) {
                    return `
                        <button data-id="${row.id}" data-action="delete" class="m-1 rounded-lg bg-gradient-to-r from-red-400 via-red-500 to-red-600 px-2 py-1 text-center text-sm font-medium text-white shadow-lg shadow-red-500/50 hover:bg-gradient-to-br focus:outline-none focus:ring-4 focus:ring-red-300 dark:shadow-lg dark:shadow-red-800/80 dark:focus:ring-red-800">
                            <i class="fas fa-trash"></i>
                        </button>
                        <button data-id="${row.id}" data-action="copy" class="m-1 rounded-lg bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 px-2 py-1 text-center text-sm font-medium text-white shadow-lg shadow-teal-500/50 hover:bg-gradient-to-br focus:outline-none focus:ring-4 focus:ring-teal-300 dark:shadow-lg dark:shadow-teal-800/80 dark:focus:ring-teal-800">
                            <i class="fas fa-link"></i>
                        </button>
                    `;
                }
            }
        ]
    });
    
    function reloadTable() {
        table.ajax.reload();
    }

    $('#formLinksTable tbody').on('click', 'button', function () {
        var id = $(this).data('id');
        var action = $(this).data('action');

        switch (action) {
            case 'delete':
                $.ajax({
                    url: `/api/form-link-manager/action/delete/${id}`,
                    method: 'DELETE',
                    success: function (response) {
                        reloadTable();
                    }
                });
                break;
            case 'copy':
                $.ajax({
                    url: `/api/form-link-manager/action/copy/${id}`,
                    method: 'POST',
                    success: function (response) {
		            if (navigator.clipboard) {
		                navigator.clipboard.writeText(response.url_link)
		                    .then(() => {
		                        alert('Form link copied to clipboard');
		                    })
		                    .catch((err) => {
		                        console.error('Failed to copy text: ', err);
		                    });
		            } else {
		                // Fallback for browsers that don't support the Clipboard API
		                const textArea = document.createElement('textarea');
		                textArea.value = response.url_link;
		                document.body.appendChild(textArea);
		                textArea.select();
		                document.execCommand('copy');
		                document.body.removeChild(textArea);
		                alert('Form link copied to clipboard (fallback method)');
		            }
			}
                });
        }
    });

    $('#btn-add-new-form-link').click(function () {
        $.ajax({
            url: '/api/form-link-manager/add',
            method: 'POST',
            data: {
                timestamp: new Date().getTime()
            },
            success: function (response) {
                console.log(response);
                reloadTable();
            },
            error: function (xhr, status, error) {
                console.error('Error adding new form link:', error);
            }
        });
    });

    $('#btn-copy-last-form-link').click(function () {
        $.ajax({
            url: '/api/form-link-manager/action/get-last-form-link',
            method: 'GET',
            success: function (response) {
                console.log(response);
                // TODO: copy the url_link to clipboard
                navigator.clipboard.writeText(response.url_link);
                alert('Form link copied to clipboard');
            }
        });
    });

    $('#btn-refresh-table').click(function () {
        reloadTable();
    });

    function updateFormLinkCard(data) {
        $('#last-form-id-created').text(data.last_form_id_created);
        $('#unopened-form-count').text(data.unopened_form_count);
        $('#last-form-id-submitted').text(data.last_form_id_submitted);
        $('#last-form-id-viewed').text(data.last_form_id_viewed);
    }
 
    function setupFormLinkEventSource() {
        const eventSource = new EventSource('/api/form-link-manager/status');
        eventSource.onmessage = function (event) {
            const data = JSON.parse(event.data);
            updateFormLinkCard(data);
        };

        eventSource.onerror = function () {
            eventSource.close();
            setTimeout(setupFormLinkEventSource, 5000);
        };

        return eventSource;
    }

    let eventSource = setupFormLinkEventSource();

    $('#dt-length-0').addClass(`
        bg-gray-50 border border-gray-300 text-gray-900 rounded-lg 
        focus:ring-blue-500 focus:border-blue-500 p-2.5 
        dark:border-gray-600 
        dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500
        w-40
    `);
});
