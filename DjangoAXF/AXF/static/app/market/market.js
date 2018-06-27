$(function () {
    // 点击‘全部类型’
    $('#all_type').click(function () {
        $("#all_type_container").toggle()  // 显示和隐藏
        $("#all_type_icon").toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        // $('#sort_rule_container').hide()
        // $('#sort_rule_icon').toggleClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        $('#sort_rule_container').triggerHandler('click')

    });

    $("#all_type_container").click(function () {
        $(this).hide() // 隐藏
        $("#all_type_icon").toggleClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

    });

    // 点击'综合排序'
    $('#sort_rule').click(function () {
        $('#sort_rule_container').toggle()
        $('#sort_rule_icon').toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        $('#all_type_container').triggerHandler('click')


    });
        $("#sort_rule_container").click(function () {
        $(this).hide() // 隐藏
        $("#sort_rule_icon").toggleClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        });

    // 商品数量的增加
    $('.addnum').click(function () {
        numNode = $(this).parent().find('.num');
        num = parseInt(numNode.html())+1;
        numNode.html(num)
    });
    // 商品数量的减少
    $('.subnum').click(function () {
        numNode = $(this).parent().find('.num');
        num = parseInt(numNode.html())-1;
        if (num<1){
            num=1
        }
        numNode.html(num)
    });

    // 加入购物车
    $('.addtocart').click(function () {
        //获取当前点击加入购物车的商品id
        goodsid = $(this).attr('goodsid');
        // //获取当前商品的数量
        // index = $(this).index('.addtocart');
        // numNode = $('.num').eq(index);
        // num = parseInt(numNode.html());
        numNode = $(this).prev().find('.num')
        num = parseInt(numNode.html());

        // ajax请求后台，将当前商品加入到购物车中
        $.get('/axf/addtocart/',{'goodsid':goodsid, 'num':num}, function (data) {

            // 添加成功
            if (data.status == 1){
                alert("加入购物车成功")
            }

            // 没有登录
            else if (data.status == -1){
                res = confirm("请先登录");
                if (res){
                    //跳转到登录页面
                    location.href = '/axf/login/'
                }
            }
            else{
                alert('加入购物车失败')

            }
        });
    });

});

