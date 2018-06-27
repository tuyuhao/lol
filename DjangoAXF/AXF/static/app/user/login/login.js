$(function () {
    // console.log(1111)
    $('form').submit(function () {
        $('#password').val(md5($('#password').val()))
    })
    
})