function like(slug, id) {
    var element = document.getElementById('like')
    var counter = document.getElementById('counter')
    $.get(`/products/like/${slug}/${id}`).then(response => {
        if (response['response'] === 'liked') {
            element.className = 'fa fa-heart'
            counter.innerText = Number(counter.innerText) + 1
        } else {
            element.className = 'fa fa-heart-o'
            counter.innerText = Number(counter.innerText) - 1
        }
    })
}