function convertToSlug(Text) {
    return Text
        .toLowerCase()
        .replace(/ /g, '-')
        .replace(/[^\w-]+/g, '')
        ;
}

$("#add-cat-btn").click(function (e) {
    e.preventDefault();
    let name = $("#add-cat-input").val();
    let slug = convertToSlug(name);
    let api_url = `http://127.0.0.1:8000/categories/api/add_category/${slug}`;

    $.ajax({
        url: api_url,
        method: "GET",
        data: {},
        success: function (data) {
            if (data.created) {
                $('#category-choice').append($('<option>', {
                    value: data.pk,
                    text: name
                }));
                $("#add-cat-input").val("");
            }
        },
        error: function (error) {
            $("label[for='other']").text("You have to specify a new category before adding it")
        }
    })
});
