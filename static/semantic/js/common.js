//顶部搜索栏搜索方法
function search_click() {
    //alert('sdf');
    var keywords = $('#indexPage_keywords').val();
    var request_url = '';
    if (keywords == '') {
        return
    }
    else {

        request_url = "?keywords=" + keywords
        window.location.href = request_url
    }

}

//顶部搜索栏搜索点击事件
$('#indexPage_search').on('click', function () {
    search_click();
});


//收藏heart点击事件
$(".extra.content a").on('click', function () {
    var item_id = $(this).attr("id");
    add_fav($(this), item_id);

});

//收藏页面heart点击事件
$("#blogPage_fav").on('click', function () {
    var item_arr = window.location.pathname.split('/');
    var item_id = item_arr[item_arr.length - 2]
    //alert(item_id);
    add_fav($(this), item_id);

});


//检查login表单
function check_login() {

    var form = document.forms["login_form"];

    for (var i = 0; i < form.length - 1; i++) {

        if (form[i].value == '') {
            $('.error').css('display', 'block');
            $('.error').text('请输入' + form[i].title);
            form[i].focus();
            return false;
            break;
        }

    }

    document.login_form.submit();

};

//检查register表单
function check_register() {
    var form = document.forms["register_form"];


    for (var i = 0; i < form.length - 1; i++) {
        if (!form[i].value) {
            $('.error').css('display', 'block');
            $('.error').text(form[i].title + '不能为空');
            form[i].focus();
            return false;
            break;
        }


    }

    if (!form[form.length - 2].checked) {
        $('.error').css('display', 'block');
        $('.error').text('阅读本站条款,并勾选同意才可提供服务');
        return false;
    }


    document.register_form.submit();
}

//检查reset表单
function check_reset() {
    var form = document.forms["reset_form"];
    for (var i = 0; i < form.length - 1; i++) {

        if (!form[i].value) {
            $('.error').css('display', 'block');
            $('.error').text(form[i].title + '不能为空');
            form[i].focus();
            return false;
            break;
        }


    }

    document.reset_form.submit();
}
