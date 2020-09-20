
$('a.like').click(function (e) {
    e.preventDefault()
    $.post('{% url "images:like" %}',
        {
            id: $(this).data('id'),
            action: $(this).data('action'),
        },
        function (data) {
            if (data['status'] === 'ok'){
                let like_button = $('a.like')
                let previous_action = like_button.data('action')
                like_button.data('action', previous_action === 'like' ? 'unlike': 'like')
                like_button.text(previous_action === 'like' ? 'Unlike': 'Like')

                let likes_count = $('span.count')
                let previous_likes = parseInt(likes_count.text())
                console.info(likes_count.text())
                console.info(previous_likes)
                likes_count.text(previous_action === 'like' ? previous_likes + 1 : previous_likes - 1)
            }
        }
        )
})
