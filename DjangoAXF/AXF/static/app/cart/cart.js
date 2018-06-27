$(function () {

    // 数量 +1
    $('.add_num').click(function () {

        var that = this;

        // 获取当前点击的购物车id
        cartid = $(this).parents('li').attr('cartid');
        // console.log(cartid)
        // 让后台将当前购物车的num+1
        $.getJSON('/axf/addnum/', {'cartid': cartid}, function (data) {
            // console.log(data);
            if (data.status == 1) {
                // 成功
                $(that).parent().find('.num').html(data.num)

                if (parseInt(data.num) > 1) {
                    $(that).parent().find('.sub_num').prop('disabled', false);  // 解除禁用
                    $(that).parent().find('.sub_num').css('background', 'white');
                }
            }
            // 重新计算总价
            calculateTotalPrice()

        });

    });

    // 数量 -1
    $('.sub_num').click(function () {

        var that = this;

        // 判断数量是否为1
        // 1, 如果为1,则禁用'减少'的按钮
        // 2, 如果大于1，则应该解除禁用
        var num = $(this).parent().find('.num').html();

        if (parseInt(num) > 1) {

            // 获取当前点击的购物车id
            cartid = $(this).parents('li').attr('cartid');

            // 让后台将当前购物车的num-1
            $.getJSON('/axf/subnum/', {cartid: cartid}, function (data) {
                // console.log(data);
                if (data.status == 1) {
                    // 成功
                    $(that).parent().find('.num').html(data.num)

                    if (parseInt(data.num) <= 1) {
                        $(that).prop('disabled', true);  // 禁用
                        $(that).css('background', '#ccc')
                    }

                }
                // 重新计算总价
                calculateTotalPrice()

            });
        }


    })

    // 勾选/取消勾选
    $('.is_choice').click(function () {
        cartid = $(this).parents('li').attr('cartid');
        var that = this;

        // 请求服务器，将勾选状态改变
        $.get('/axf/changeselectstate/', {cartid: cartid}, function (data) {
            // console.log(data)
            if (data.status == 1) {
                if (data.select) {
                    $(that).find('span').html('√')
                }
                else {
                    $(that).find('span').html('')

                }
            }
            // 更新'全选'按钮的选中状态
            isAllSelected();
        })

    })

    //删除
    $('.delbtn').click(function () {
        cartid = $(this).parents('li').attr('cartid');
        var that = this;

        // 让服务器删除购物车中指定的商品
        $.get('/axf/cartdelgoods/', {cartid: cartid}, function (data) {
            // console.log(data)
            if (data.status == 1) {
                $(that).parents('li').remove()
            }
            // 更新'全选'按钮的选中状态
            isAllSelected();

        })
    });

    // 全选/全不选
    $('#all_select').click(function () {

        // 1.如果当前全部勾选了，则执行'全不选'操作
        // 2.如果存在没有勾选的，执行'全选'操作

        // 先获取勾选的和未勾选的cartid
        selects = [];
        unselects = [];

        $('.menuList').each(function () {
            var gou = $(this).find('.is_choice').find('span').html();

            // 勾选的
            if (gou) {
                selects.push($(this).attr('cartid'))
            }
            // 未勾选的
            else {
                unselects.push($(this).attr('cartid'))
            }
        });
        // 全不选
        if (unselects.length == 0) {

            // 请求服务器，将selects中所有的cartid上传给服务器
            $.get('/axf/cartchangeselect/', {selects: selects.join('#'), action: 'unselect'}, function (data) {

                if (data.status == 1) {
                    $('.is_choice').find('span').html('')
                }
                // 更新'全选'按钮的选中状态
                isAllSelected();
            })
        }
        // 全选
        else {
            // 请求服务器，将unselects中所有的cartid上传给服务器
            $.get('/axf/cartchangeselect/', {selects: unselects.join('#'), action: 'select'}, function (data) {
                if (data.status == 1) {
                    $('.is_choice').find('span').html('√')
                }
                // 更新'全选'按钮的选中状态
                isAllSelected();

            })
        }

    })

    // 检查是否全选了
    isAllSelected();

    function isAllSelected() {

        count = 0;
        $('.is_choice').each(function () {
            if ($(this).find('span').html()) {
                count++;
            }
        });

        // 全选
        if (count == $('.is_choice').length) {
            $('#all_select_icon').html('√')
        }
        // 未全选
        else {
            $('#all_select_icon').html('')
        }
        // 重新计算总价
        calculateTotalPrice()

    }

    // 计算总价
    calculateTotalPrice();

    function calculateTotalPrice() {
        // 总价
        totalprice = 0;

        // 遍历每个购物车商品
        $('.menuList').each(function () {

            // 如果是选中的
            if ($(this).find('.is_choice span').html()) {
                price = $(this).find('.price').html();
                num = $(this).find('.num').html();
                totalprice += parseFloat(price) * parseFloat(num);
            }

        })
        // 显示总价
        $('#totalprice').html(totalprice.toFixed(2));
    }


    // 结算
    $('#calculate').click(function () {

        selects = [];
        // 遍历购物车中所有的商品，提取出选中的商品，并将cartid存入selects中
        $('.menuList').each(function () {
            if ($(this).find('.is_choice span').html()) {
                selects.push($(this).attr('cartid'))
            }
        });
            if (selects.length == 0){
            alert('请先选择商品');
            return
        }


        //请求服务器，将选中商品cartid提交，并让服务器生成订单
        $.get('/axf/generateorder/', {selects: selects.join('#')}, function (data) {
            // console.log(data)
            // 生成订单成功
            if (data.status == 1) {
                location.href = '/axf/orderinfo/' + data.orderid + '/'
            }
            // 没有登录
            else if (data.status == -1) {
                alert(data.msg)
            }

        })

    })

});
