$(document).ready(function () {
    // Setup - add a text input to each header cell
    $('#example thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#example thead');

    var table = $('#example').DataTable({
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
            url: '/api/campaigns',
            dataSrc: function (json) {
                return Array.isArray(json) ? json : [json];
            }
        },
        columns: [
            { data: 'table_id', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'responden_id', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'entry_time', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'responden_name', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'campaign_name', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'start_date', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'end_date', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'unit', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'brand', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'program', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'jenis_paket', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'nilai_paket', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'revenue_prorate', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'total_real_cost', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'breakdown_cost', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'breakdown_kpi', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'activity_type', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'list_benefit', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'detail_brief', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'timeline_benefit', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'product_knowledge', className: 'text-nowrap text-sm dark:text-white' },
            { data: 'key_visual_design', className: 'text-nowrap text-sm dark:text-white' },
            {
                data: null,
                className: 'text-nowrap text-sm dark:text-white',
                render: function (data, type, row) {
                    return `
                        <button data-id="${row.table_id}" data-action="view" class="m-1 rounded-lg bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 px-2 py-1 text-center text-sm font-medium text-white shadow-lg shadow-blue-500/50 hover:bg-gradient-to-br focus:outline-none focus:ring-4 focus:ring-blue-300 dark:shadow-lg dark:shadow-blue-800/80 dark:focus:ring-blue-800">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button data-id="${row.table_id}" data-action="edit" class="m-1 rounded-lg bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 px-2 py-1 text-center text-sm font-medium text-white shadow-lg shadow-teal-500/50 hover:bg-gradient-to-br focus:outline-none focus:ring-4 focus:ring-teal-300 dark:shadow-lg dark:shadow-teal-800/80 dark:focus:ring-teal-800">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button data-id="${row.table_id}" data-action="pdf" class="m-1 rounded-lg bg-gradient-to-r from-green-400 via-green-500 to-green-600 px-2 py-1 text-center text-sm font-medium text-white shadow-lg shadow-green-500/50 hover:bg-gradient-to-br focus:outline-none focus:ring-4 focus:ring-green-300 dark:shadow-lg dark:shadow-green-800/80 dark:focus:ring-green-800">
                            <i class="fas fa-file-pdf"></i>
                        </button>
                        <button data-id="${row.table_id}" data-action="delete" class="m-1 rounded-lg bg-gradient-to-r from-red-400 via-red-500 to-red-600 px-2 py-1 text-center text-sm font-medium text-white shadow-lg shadow-red-500/50 hover:bg-gradient-to-br focus:outline-none focus:ring-4 focus:ring-red-300 dark:shadow-lg dark:shadow-red-800/80 dark:focus:ring-red-800">
                            <i class="fas fa-trash"></i>
                        </button>
                    `;
                }
            }
        ],
        initComplete: function () {
            var api = this.api();

            // For each column
            api.columns().eq(0).each(function (colIdx) {
                if (colIdx === api.columns().nodes().length - 1) {
                    var cell = $('.filters th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    $(cell).html('<span class="text-xs text-gray-500 dark:text-gray-400">Search Filter Toggled</span>');
                    return;
                }
                var cell = $('.filters th').eq(
                    $(api.column(colIdx).header()).index()
                );
                var title = $(cell).text();
                $(cell).html('<input type="text" placeholder="Filter" class="block w-full p-1 text-xs text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />');

                // On keyup in the filter input
                $('input', $('.filters th').eq($(api.column(colIdx).header()).index()))
                    .off('keyup change')
                    .on('keyup change', function (e) {
                        e.stopPropagation();
                        // Get the search value
                        $(this).attr('title', $(this).val());
                        var regexr = '({search})';

                        var cursorPosition = this.selectionStart;
                        // Search the column for that value
                        api
                            .column(colIdx)
                            .search(
                                this.value != ''
                                    ? regexr.replace('{search}', '(((' + this.value + ')))')
                                    : '',
                                this.value != '',
                                this.value == ''
                            )
                            .draw();

                        $(this)
                            .focus()[0]
                            .setSelectionRange(cursorPosition, cursorPosition);
                    });
            });

            // Initially hide filters
            $('.filters').addClass('hidden');

            // Add toggle filters button functionality
            $('#btn-toggle-filters').on('click', function () {
                const button = $(this);
                const isEnabled = button.attr('aria-checked') === 'true';
                const circle = button.find('.size-5');
                const xIcon = circle.find('span').first();
                const checkIcon = circle.find('span').last();

                $('.filters').toggleClass('hidden');

                // Update button state with sky blue color when active
                button.attr('aria-checked', !isEnabled);
                button.toggleClass('bg-gray-200 dark:bg-gray-700 bg-sky-500');

                // Handle translation
                circle.toggleClass('translate-x-0 translate-x-5');

                // Update icon colors - change to sky blue
                if (isEnabled) {
                    checkIcon.removeClass('opacity-100').addClass('opacity-0');
                    setTimeout(() => xIcon.removeClass('opacity-0').addClass('opacity-100'), 100);
                } else {
                    xIcon.removeClass('opacity-100').addClass('opacity-0');
                    setTimeout(() => {
                        checkIcon.removeClass('opacity-0').addClass('opacity-100');
                        checkIcon.find('svg').removeClass('text-indigo-600').addClass('text-sky-500');
                    }, 100);
                }
            });
        },
    });

    $('#dt-length-0').addClass(`
            bg-gray-50 border border-gray-300 text-gray-900 rounded-lg 
            focus:ring-blue-500 focus:border-blue-500 p-2.5 
            dark:border-gray-600 
            dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500
            w-40
        `);
    $('label[for="dt-length-0"]').addClass(`
            dark:text-white    
        `);
    $('#dt-length-0 option').addClass(`
            dark:text-white
        `);

    // $('[data-modal-toggle="popup-modal"]').click(function () {
    //     var $modal = $('#popup-modal');
    //     // Check if the modal is currently shown or hidden
    //     if ($modal.hasClass('hidden')) {
    //         // Modal is being opened, remove the hidden class
    //         $modal.removeClass('hidden');
    //         $modal.attr('aria-hidden', 'false');
    //     } else {
    //         // Modal is being closed, add the hidden class
    //         $modal.addClass('hidden');
    //         $modal.attr('aria-hidden', 'true');

    //         // Ensure no element inside the modal retains focus
    //         $modal.find(':focus').blur();
    //     }
    // });

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.attributeName === 'aria-hidden') {
                const target = mutation.target;
                console.log('aria-hidden detected on:', target);
                $(target).removeAttr('aria-hidden');
                console.log('aria-hidden removed.');
            }
        });
    });

    $('[data-modal-target]').each(function () {
        const modalId = $(this).data('modal-target');
        const $modal = $('#' + modalId);

        if ($modal.length > 0) {
            observer.observe($modal[0], {
                attributes: true, // Observe attribute changes
            });
            console.log(`Observer attached to modal: #${modalId}`);
        } else {
            console.warn(`Modal not found: #${modalId}`);
        }
    });

    // Standard modal toggle functionality
    $('[data-modal-toggle]').click(function () {
        const modalId = $(this).data('modal-target');
        const $modal = $('#' + modalId);

        // Toggle the modal visibility
        $modal.toggleClass('hidden');
    });

    function close_add_new_data_modal_confirmation() {
        const modal = document.getElementById('popup-modal-add-new-data');
        modal.classList.add('opacity-0', 'scale-100', 'pointer-events-none');
    }

    function open_add_new_data_modal_confirmation() {
        const modal = document.getElementById('popup-modal-add-new-data');
        modal.classList.remove('opacity-0', 'scale-100', 'pointer-events-none');
    }

    function open_add_new_data_modal_form() {
        const modal = document.getElementById('form-modal-add-new-data');
        modal.classList.remove('opacity-0', 'scale-100', 'pointer-events-none');
        $('#responden-name').focus();
    }

    function close_add_new_data_modal_form() {
        const modal = document.getElementById('form-modal-add-new-data');
        modal.classList.add('opacity-0', 'scale-100', 'pointer-events-none');
        // clear form
        $('#add-campaign-form')[0].reset();

    }

    $('#btn-add-new-data').click(function () {
        open_add_new_data_modal_confirmation()
    });

    $('#close-modal-add-new-data').click(function () {
        close_add_new_data_modal_confirmation()
    });

    $('#cancel-modal-add-new-data').click(function () {
        close_add_new_data_modal_confirmation()
    });

    $('#popup-modal-add-new-data').click(function (event) {
        if (event.target === this) {
            close_add_new_data_modal_confirmation()
        }
    });

    $('#confirm-modal-add-new-data').click(function () {
        close_add_new_data_modal_confirmation()
        open_add_new_data_modal_form()
    });

    $('#close-form-modal-add-new-data').click(function () {
        close_add_new_data_modal_form()
    });

    $('#cancel-form-add-new-data').click(function () {
        close_add_new_data_modal_form()
    });

    $('#form-modal-add-new-data').click(function (event) {
        if (event.target === this) {
            close_add_new_data_modal_form()
        }
    });

    // Add this function to update the badge count
    function updateFilterCount() {
        const table = $('#example').DataTable();
        const activeFilters = table.columns().search().filter(function (value) {
            return value !== '';
        }).length;

        const badge = $('#filter-count');
        if (activeFilters === 0) {
            badge.addClass('hidden');
        } else {
            badge.removeClass('hidden').text(activeFilters);
        }
    }

    // Listen to DataTables search event
    $('#example').DataTable().on('search.dt', function () {
        updateFilterCount();
    });

    $('#btn-clear-filters').on('click', function () {
        $('.filters input').val('');
        var table = $('#example').DataTable();
        table.search('').columns().search('').draw();
        updateFilterCount();
    });

    // Add form submission handler
    $('#add-campaign-form').submit(function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());
        
        // Add these debug logs
        console.log('Selected jenis_paket value:', $('#jenis-paket').val());
        console.log('FormData entries:', Object.fromEntries(formData.entries()));
        console.log('Final data object:', data);

        $.ajax({
            url: '/api/campaign',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function () {
                console.log('Sending data:', data);
            },
            success: function (response) {
                // Show success message
                // alert('Campaign data added successfully!');

                // Reset form and close modal
                // $('#add-campaign-form')[0].reset();
                close_add_new_data_modal_form();

                // Refresh the DataTable
                $('#example').DataTable().ajax.reload();
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('Failed to add campaign data. Please try again.');
            }
        });
    });

    // Add click handler for refresh button
    $('#btn-refresh-table').on('click', function () {
        table.ajax.reload();
        // If that doesn't work, try:
        // table.draw();
    });

    // After DataTable initialization
    $('#example tbody').on('click', 'button', function () {
        var id = $(this).data('id');
        var action = $(this).data('action');

        switch (action) {
            case 'view':
                $.ajax({
                    url: `/api/campaigns/action/view/${id}`,
                    method: 'GET',
                    success: function (response) {
                        console.log('View response:', response);
                        // Format currency values
                        const formatCurrency = (value) => {
                            return new Intl.NumberFormat('id-ID', {
                                style: 'currency',
                                currency: 'IDR'
                            }).format(value);
                        };

                        console.log('Response:', response);

                        // Populate the view modal with data
                        $('#view-responden-name').text(response.responden_name || '-');
                        $('#view-campaign-name').text(response.campaign_name || '-');
                        $('#view-unit').text(response.unit || '-');
                        $('#view-brand').text(response.brand || '-');
                        $('#view-program').text(response.program || '-');
                        $('#view-jenis-paket').text(response.jenis_paket || '-');
                        $('#view-nilai-paket').text(formatCurrency(response.nilai_paket) || '-');
                        $('#view-revenue-prorate').text(formatCurrency(response.revenue_prorate) || '-');
                        $('#view-total-real-cost').text(formatCurrency(response.total_real_cost) || '-');
                        $('#view-breakdown-cost').text(response.breakdown_cost || '-');
                        $('#view-breakdown-kpi').text(response.breakdown_kpi || '-');
                        $('#view-activity-type').text(response.activity_type || '-');
                        $('#view-list-benefit').text(response.list_benefit || '-');
                        $('#view-detail-brief').text(response.detail_brief || '-');
                        $('#view-timeline-benefit').text(response.timeline_benefit || '-');
                        $('#view-product-knowledge').text(response.product_knowledge || '-');
                        $('#view-key-visual-design').text(response.key_visual_design || '-');

                        // Update date handling - display as strings
                        $('#view-start-date').text(response.start_date || '-');
                        $('#view-end-date').text(response.end_date || '-');

                        // Open the modal
                        open_view_data_modal();
                    },
                    error: function (xhr, status, error) {
                        console.error('Error fetching campaign data:', error);
                        alert('Failed to fetch campaign data. Please try again.');
                    }
                });
                break;

            case 'edit':
                $.ajax({
                    url: `/api/campaigns/action/view/${id}`,
                    method: 'GET',
                    success: function (response) {
                        // Populate the edit form with existing data
                        $('#edit-table-id').val(response.table_id);
                        $('#edit-responden-name').val(response.responden_name);
                        $('#edit-campaign-name').val(response.campaign_name);
                        $('#edit-datepicker-range-start').val(response.start_date);
                        $('#edit-datepicker-range-end').val(response.end_date);
                        $('#edit-unit').val(response.unit);
                        $('#edit-brand').val(response.brand);
                        $('#edit-program').val(response.program);
                        $('#edit-jenis-paket').val(response.jenis_paket);
                        $('#edit-nilai-paket').val(response.nilai_paket);
                        $('#edit-revenue-prorate').val(response.revenue_prorate);
                        $('#edit-total-real-cost').val(response.total_real_cost);
                        $('#edit-breakdown-cost').val(response.breakdown_cost);
                        $('#edit-breakdown-kpi').val(response.breakdown_kpi);
                        $('#edit-activity-type').val(response.activity_type);
                        $('#edit-list-benefit').val(response.list_benefit);
                        $('#edit-detail-brief').val(response.detail_brief);
                        $('#edit-timeline-benefit').val(response.timeline_benefit);
                        
                        // Handle radio buttons
                        if (response.product_knowledge === 'yes') {
                            $('#edit-product-knowledge-yes').prop('checked', true);
                        } else if (response.product_knowledge === 'no') {
                            $('#edit-product-knowledge-no').prop('checked', true);
                        }
                        
                        if (response.key_visual_design === 'yes') {
                            $('#edit-key-visual-yes').prop('checked', true);
                        } else if (response.key_visual_design === 'no') {
                            $('#edit-key-visual-no').prop('checked', true);
                        }

                        // Open the modal
                        open_edit_data_modal();
                    }
                });
                break;

            case 'pdf':
                $.ajax({
                    url: `/api/campaigns/action/pdf/${id}`,
                    method: 'GET',
                    xhrFields: {
                        responseType: 'blob'  // Important: handle binary data
                    },
                    success: function (response, status, xhr) {
                        // Create blob link to download
                        const blob = new Blob([response], { type: 'application/pdf' });
                        const url = window.URL.createObjectURL(blob);
                        
                        // Create temporary link and trigger download
                        const link = document.createElement('a');
                        link.href = url;
                        
                        // Get filename from Content-Disposition header
                        const contentDisposition = xhr.getResponseHeader('Content-Disposition');
                        const filename = contentDisposition.split('filename=')[1].replace(/"/g, '');
                        link.download = filename;
                        
                        link.click();
                        
                        // Cleanup
                        window.URL.revokeObjectURL(url);
                    },
                    error: function (xhr, status, error) {
                        console.error('Error generating PDF:', error);
                        alert('Failed to generate PDF. Please try again.');
                    }
                });
                break;

            case 'delete':
                if (confirm('Are you sure you want to delete this item?')) {
                    $.ajax({
                        url: `/api/campaigns/action/delete/${id}`,
                        method: 'DELETE',
                        success: function () {
                            table.ajax.reload();
                        }
                    });
                }
                break;
        }
    });

    // Add modal close handlers
    $('#close-form-modal-view-data, #close-view-data').click(function () {
        close_view_data_modal();
    });

    // Close modal when clicking outside
    $('#form-modal-view-data').click(function (event) {
        if (event.target === this) {
            close_view_data_modal();
        }
    });

    // Add these functions after your existing modal functions
    function open_view_data_modal() {
        const modal = document.getElementById('form-modal-view-data');
        modal.classList.remove('opacity-0', 'scale-100', 'pointer-events-none');
    }

    function close_view_data_modal() {
        const modal = document.getElementById('form-modal-view-data');
        modal.classList.add('opacity-0', 'scale-100', 'pointer-events-none');
    }

    // Add these functions for edit modal
    function open_edit_data_modal() {
        const modal = document.getElementById('form-modal-edit-data');
        modal.classList.remove('opacity-0', 'scale-100', 'pointer-events-none');
    }

    function close_edit_data_modal() {
        const modal = document.getElementById('form-modal-edit-data');
        modal.classList.add('opacity-0', 'scale-100', 'pointer-events-none');
    }

    // Add form submission handler for edit
    $('#edit-campaign-form').submit(function (e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());
        const id = data.table_id;  // Get the ID from the hidden input
        
        $.ajax({
            url: `/api/campaigns/action/edit/${id}`,
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function (response) {
                close_edit_data_modal();
                $('#example').DataTable().ajax.reload();  // Refresh the table
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('Failed to update campaign data. Please try again.');
            }
        });
    });

    // Add modal close handlers
    $('#close-form-modal-edit-data, #cancel-form-edit-data').click(function () {
        close_edit_data_modal();
    });

    // Close modal when clicking outside
    $('#form-modal-edit-data').click(function (event) {
        if (event.target === this) {
            close_edit_data_modal();
        }
    });

    // Add CSV export button handler
    $('#btn-export-csv').click(function() {
        window.location.href = '/api/campaigns/export-to-csv';
    });

})