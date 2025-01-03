$(document).ready(function () {
    var table = $('#logHistoryTable').DataTable({
        orderCellsTop: true,
        fixedHeader: true,
        scrollCollapse: true,
        scrollY: '450px',
        scrollX: true,
        order: [[1, 'desc']],
        ajax: {
            url: '/api/log-history',
            dataSrc: function (json) {
                return Array.isArray(json) ? json : [json];
            }
        },
        columns: [
            { data: 'id', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'timestamp', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'ip_address', className: 'text-nowrap text-sm dark:text-white' },
            {
                data: 'status',
                className: 'text-nowrap text-sm dark:text-white',
                render: function (data, type, row) {
                    switch (data) {
                        case 'Success':
                            return `<span class="rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-medium text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300">Success</span>`;
                        case 'Error':
                            return `<span class="rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-800 dark:bg-red-900 dark:text-red-300">Error</span>`;
                        case 'Warning':
                            return `<span class="rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">Warning</span>`;
                        case 'Info':
                            return `<span class="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800 dark:bg-blue-900 dark:text-blue-300">Info</span>`;
                        default:
                            return `<span class="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800 dark:bg-gray-900 dark:text-gray-300">Unknown</span>`;
                    }
                }
            },
            { data: 'error_message', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'category', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'activity', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'details', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'browser', className: 'text-nowrap text-sm dark:text-white' },
        ]
    });

    $('#dt-length-0').addClass(`
        bg-gray-50 border border-gray-300 text-gray-900 rounded-lg 
        focus:ring-blue-500 focus:border-blue-500 p-2.5 
        dark:border-gray-600 
        dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500
        w-40
    `);
});