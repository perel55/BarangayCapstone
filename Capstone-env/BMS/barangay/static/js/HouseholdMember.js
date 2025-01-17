    $(document).ready(function () {
        $(".autocomplete-resident").select2({
            ajax: {
                url: "{% url 'resident_autocomplete' %}",
                dataType: "json",
                delay: 250,  // Delay for typing
                data: function (params) {
                    return {
                        term: params.term,  // Search query
                    };
                },
                processResults: function (data) {
                    return {
                        results: data,
                    };
                },
            },
            placeholder: "Search for a resident...",
            allowClear: true,
            minimumInputLength: 1,  // Start searching after one character
        });
    });

