$('#searchInput').on('input', function() {
                    console.log('Input event triggered');
                    // Rest of the code
                });
                $(document).ready(function() {
                    $('#searchInput').on('input', function() {
                        var input = $(this).val();
                        if (input) {
                            $.ajax({
                                type: 'GET',
                                url: 'http://127.0.0.1:8000/search-services/',
                                data: {
                                    'input': input
                                },
                                success: function(data) {
                                    $('#searchOptions').empty(); // Clear previous options
                                    if (data.services.length > 0) {
                                        var optionsHtml = '';
                                        data.services.forEach(function(service) {
                                            optionsHtml += '<div>' + service + '</div>';
                                        });
                                        $('#searchOptions').html(optionsHtml); // Add new options
                                    } else {
                                        $('#searchOptions').html('<div>No matching services found</div>');
                                    }
                                }
                            });
                        } else {
                            $('#searchOptions').empty(); // Clear options when input is empty
                        }
                    });
                });