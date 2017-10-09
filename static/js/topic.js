var initedEditor = function () {
    var e = new Editor()
    var element = $('.editor').get(0)
    e.render(element)
    return e
}

var __main = function () {
    initedEditor()
}

$(document).ready(function () {
    __main()
})