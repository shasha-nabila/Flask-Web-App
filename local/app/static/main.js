$(document).ready(function () {

    // Function to filter posts based on the search query
    function filterPosts(query) {
        // Convert query to lowercase for case-insensitive search
        query = query.toLowerCase();

        // Loop through each post and check if it contains the search query
        $('#posts .card').each(function () {
            var postText = $(this).find('.card-body .card-text').text().toLowerCase();
            if (postText.indexOf(query) === -1) {
                // Hide posts that don't match the search query
                $(this).hide();
            } else {
                // Show posts that match the search query
                $(this).show();
            }
        });
    }

    // Event listener for form submission
    $('#search-form').submit(function (e) {
        e.preventDefault();
        var searchTerm = $('#search-input').val();
        filterPosts(searchTerm);
    });

    // Function to filter posts by meal type
    function filterByMealType(mealType) {
        // Loop through each post and check for matching meal type
        $('#posts .card').each(function () {
            var postMealType = $(this).find('.card-header .meal-type').text();
            if (postMealType !== mealType) {
                // Hide posts that don't match the selected meal type
                $(this).hide();
            } else {
                // Show posts that match the selected meal type
                $(this).show();
            }
        });
    }

    // Event listener for meal type tags
    $('.meal-type').on('click', function () {
        var selectedMealType = $(this).text();
        filterByMealType(selectedMealType);
    });

    // Like Button
    $('.like-btn').on('click', function (e) {
        e.preventDefault();
        var post_id = $(this).data('post-id');
        var button = $(this); // Reference to the button clicked

        $.ajax({
            type: 'POST',
            url: '/like-post/' + post_id,
            success: function (response) {
                if (response.success) {
                    // Check the response from the server to update the button icon
                    if (response.liked) {
                        button.html('<i class="fas fa-heart" style="color: #ff0000;"></i>');
                    } else {
                        button.html('<i class="far fa-heart" style="color: #ff0000;"></i>');
                        location.reload();
                    }
                }
            }
        });
    });

    // Create Post Button
    const exampleModal = document.getElementById('exampleModal');

    if (exampleModal) {
        exampleModal.addEventListener('show.bs.modal', event => {
            const modalTitle = exampleModal.querySelector('.modal-title');
            const modalBodyInput = exampleModal.querySelector('.modal-body input');

            modalTitle.textContent = `New message`;
            modalBodyInput.value = '';
        });
    }

});
