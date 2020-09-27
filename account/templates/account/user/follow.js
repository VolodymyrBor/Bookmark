$('a.follow').click(function (e) {
    e.preventDefault()
    $.post('{% url "user_follow" %}',
        {
            id: $(this).data('id'),
            action: $(this).data('action'),
        },
        function (data) {
            if (data['status'] === 'ok') {
                let previous_action = $('a.follow').data('action')
                $('a.follow').data('action', previous_action === 'follow' ? 'unfollow': 'follow')
                $('a.follow').text(previous_action === 'follow' ? 'Unfollow': 'Follow')

                let previous_followers = parseInt($('span.count').text())
                $('span.count').text(previous_action === 'follow' ? previous_followers + 1: previous_followers - 1)
            }
        })
})