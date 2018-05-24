"use strict";
(function () {
    $(document).ready(function () {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true
        })
        .on('changeDate', function (e) {
            $(this).focus();
        });
        $('.rd-range__pointer-1 > div').bind('DOMSubtreeModified', function () {
            var value = $(this).html();
            if (value) {
                $('#search_min_price').val(value);
            }
        });
        $('.rd-range__pointer-2 > div').bind('DOMSubtreeModified', function () {
            var value = $(this).html();
            if (value) {
                $('#search_max_price').val(value);
            }
        });

        $('#tour_sort_select').change(function () {
            var value = $(this).val();
            $.post(window.location.pathname, {
                'csrfmiddlewaretoken': csrf_token,
                'tour_sort': value
            });
            window.location.reload(true);
        })
    });
}());
