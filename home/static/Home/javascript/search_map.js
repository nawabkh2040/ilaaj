$('#cityInput').on('input', function() {
     var input = $(this).val();
     if (input) {
         $.ajax({
             type: 'GET',
             url: 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + input + '.json?access_token=pk.eyJ1IjoibmF3YWJraDIwNDAiLCJhIjoiY2x0aWwydmY2MGRhYzJxbzBnb3ZkZGFwYyJ9.pOki1d8O8P4SW9xX9BrPXA',
             success: function(data) {
                 // Process the data and populate the dropdown options
                 $('#cityInput').empty(); // Clear previous options
                 $('#cityInput').append('<option value="" selected disabled>Select your location...</option>');
                 data.features.forEach(function(feature) {
                     $('#cityInput').append('<option value="' + feature.place_name + '">' + feature.place_name + '</option>');
                 });
             }
         });
     } else {
         $('#cityInput').empty(); // Clear options if input is empty
         $('#cityInput').append('<option value="" selected disabled>Select your location...</option>');
     }
 });