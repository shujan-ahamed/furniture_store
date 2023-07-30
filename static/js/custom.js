

$(document).ready(function (){
    $("#loadmore").on('click', function (){
        var _current_products = $('.product-box').length;
        var _limit = $(this).attr('data-limit')
        var _total = $(this).attr('data-total')
        // run ajax 
        $.ajax({
            url : '/marketplace/load_more_products',
            data : {
                limit : _limit,
                ofset : _current_products,
            },
            dataType : 'json',
            beforeSend :function () {
                $("#loadmore").attr('disabled', true);
                $('#icon-rotate').addClass('fa-spin');
            },
            success :function (result) {
                $('#icon-rotate').removeClass('fa-spin');
                $('#filtered_products').append(result.data);
                $("#loadmore").attr('disabled', false);
                
                var total_showing = $('.product-box').length;
                if(total_showing == _total){
                $("#loadmore").remove();
                }
            }
        });
        //end ajax
        
    });

    // min max price filter 
    $('#maxAmount').on('blur', function () {
        var _min = $(this).attr('min');
        var _max = $(this).attr('max');
        var _value = $(this).val();
        // console.log(_min, _max, _value)
        if (_value<parseInt(_min) ||  _value> parseInt(_max)){
            alert('Value should be'+_min+' to '+_max);
            $(this).val(_min);
            $(this).focus();
            $('#priceRange').val(_min);
            return false;
        }
    })

    // Product variation 
    $('.choose-size').hide();

    $(".colour-checkbox").on('click', function (){
        var _selected_colour = $(this).attr('data-colour');

        var _vm = $('#vari-product-price');
        var index = _vm.attr('data-index');
        

        $('.choose-size').hide();
        $('.size-input').prop('checked', false);
        $('.colour'+_selected_colour).show();

        var colour = $(this).attr('data-val');
        $('.var-colour-'+index).val(colour);
        console.log(colour);

        $('#colour'+_selected_colour).prop('checked', true);

        //getting first size price on color click
        var _price = $('#colour'+_selected_colour).val();
        $('.vari-product-price-'+index).text(_price);

        //discount
        var _discount_data = $('#colour'+_selected_colour).attr('data-dis-price')
        $('.dis-product-price-'+index).text(_discount_data);
        //product price mark as cross
        
        console.log(_discount_data);
        console.log(_dicount_price);
        console.log(_price)
    });
    

     // show firt variation checked 
    $('.colour-checkbox').first().attr("checked", "checked");
    var _colour = $('.colour-checkbox').attr('data-colour');
    $('.colour'+_colour).show();
    $('#colour'+_colour).first().prop('checked', true);

     // show price variation
    $(".size-input").on('click', function (){
        var _vm = $(this);
        var index = _vm.attr('data-index');

        $('.size-input').prop('checked', false);
        var _price = $(this).val();
        $('.vari-product-price-'+index).text(_price);

        var size = $(this).attr('data-val');
        $('.var-size-'+index).val(size);

        $(this).prop('checked', true);

        //discount
        var _discount_data = $(this).attr('data-dis-price');
        $('.dis-product-price-'+index).text(_discount_data);
        
        console.log(_discount_data);
        console.log(_dicount_price);
        console.log(size);
        console.log(_price);
    });

    // add to cart 
    $(document).on('click', ".addToCArtBtn", function (e){
        e.preventDefault();
        var _vm = $(this);
        var index = _vm.attr('data-index');
        var _qty = $('.prdouct_qty-'+index).val();
        var _product_id =$('#product_id-'+index).val();
        var _product_image =$('.product_image-'+index).val();
        var _product_url =$('#product_url').val();
        var _product_title =$('#product_title-'+index).val();

        var _or_product_price =$('.vari-product-price-'+index).text();
        var _product_price =$('#price_to_add_in_cart-'+index).text();

        var _product_size =$('#product_size-'+index).val();
        var _product_colour =$('#product_colour-'+index).val();
        

        console.log(_product_colour, _product_size);
        console.log('title',_product_title);
        //ajax start
        url = $(this).attr('data-url');
        
        data = {
            'qty': parseInt(_qty),
            'id' : _product_id,
            'product_url' : _product_url,
            'product_size' : _product_size,
            'product_colour' : _product_colour,
            'image' : _product_image,
            'title' : _product_title,
            'price' : parseInt(_product_price),
            'or_price' : parseInt(_or_product_price),
        }
        // run ajax 
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            dataType : 'json',
            beforeSend :function () {
            },
            success :function (response) {
                console.log(response.total_cart_items);
                console.log(typeof response.total_cart_items);
                $('.total-cart').text(response.total_cart_items);
                $('.total-cart').text(response.total_cart_items);
                console.log(response)

                if (response.status == 'success'){
                    Swal.fire({
                        icon: 'success',
                        title: response.message,
                        showConfirmButton: false,
                        timer: 800
                    })
                    }else{
                        Swal.fire({
                            icon: 'error',
                            title: response.message,
                            showConfirmButton: false,
                            timer: 800
                        })
                    };
            }
        });
        //end ajax
    });
    
    //delete cart item
    $(document).on('click', '.delete-item', function (e) {
        e.preventDefault();

        var _product_id = $(this).attr('data-item');
        var _qty = $('#cart_qty').val();
        console.log(_qty);
        console.log(_product_id);


        //ajax start
        url = $(this).attr('data-url');
        data = {
            'id' : _product_id,
            'qty': _qty,
        }
        // run ajax 
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            dataType : 'json',
            beforeSend :function () {
            },
            success :function (response) {
                $('.total-cart').text(response.total_cart_items);
                $('#cart-list').html(response.data);

                if (response.status == 'success'){
                    Swal.fire({
                        icon: 'success',
                        title: response.message,
                        showConfirmButton: false,
                        timer: 800
                    })
                    }else{
                        Swal.fire({
                            icon: 'error',
                            title: response.message,
                            showConfirmButton: false,
                            timer: 800
                        })
                    };
            }
        });
        //end ajax
    });

    //decrease cart item
    $(document).on('click', '.dec-item', function (e) {
        e.preventDefault();

        var _product_id = $(this).attr('data-item');
        //ajax start
        url = $(this).attr('data-url');
        data = {
            'id' : _product_id,
        }
        // run ajax 
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            dataType : 'json',
            beforeSend :function () {
            },
            success :function (response) {
                $('.total-cart').text(response.total_cart_items);
                $('#cart-list').html(response.data);

                if (response.status == 'success'){
                    Swal.fire({
                        icon: 'success',
                        title: response.message,
                        showConfirmButton: false,
                        timer: 800
                    })
                };
            }
        });
        //end ajax
    });

    //increase cart item
    $(document).on('click', '.incr-item', function (e) {
        e.preventDefault();

        var _product_id = $(this).attr('data-item');
        //ajax start
        url = $(this).attr('data-url');
        data = {
            'id' : _product_id,
        }
        // run ajax 
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            dataType : 'json',
            beforeSend :function () {
            },
            success :function (response) {
                $('.total-cart').text(response.total_cart_items);
                $('#cart-list').html(response.data);
            }
        });
        //end ajax
    });

    //change iput btn default django
    // $('.input-btn').addClass('removeValue');

    //Add Review & Ratings 
    $('#AddReview').on('submit', function (e) {
        var url = $(this).attr('action');
        console.log('working');
        // run ajax 
        $.ajax({
            url : url,
            type : "POST",
            data : $(this).serialize(),
            dataType : 'json',
            success :function (response) {
                console.log(response);

                //show review in html
                    var _html = '<div class="review_item"><div class="media" id="review_list">'
                    _html += '<div class="d-flex"><img src="'+response.data.profile_pic+'" alt="" width="80px" height="80px" style="border-radius: 50%;" /></div>';
                    _html += '<div class="media-body">';
                    _html += '<h4>'+response.data.user+'</h4>';
                    _html += '<div class="rating-star">';
                    _html += '<span><i class="fa fa-star{% if '+response.data.rating+' == 0.5 %}-half-o{% elif '+response.data.rating+' < 1 %}-o {% endif %}" aria-hidden="true"></i><i class="fa fa-star{% if '+response.data.rating+' == 1.5 %}-half-o{% elif '+response.data.rating+' < 2 %}-o {% endif %}" aria-hidden="true"></i><i class="fa fa-star{% if '+response.data.rating+' == 2.5 %}-half-o{% elif '+response.data.rating+' < 3 %}-o {% endif %}" aria-hidden="true"></i><i class="fa fa-star{% if '+response.data.rating+' == 3.5 %}-half-o{% elif '+response.data.rating+' < 4 %}-o {% endif %}" aria-hidden="true"></i><i class="fa fa-star{% if '+response.data.rating+' == 4.5 %}-half-o{% elif '+response.data.rating+' < 5 %}-o {% endif %}" aria-hidden="true"></i></span>';

                    _html += '</div></div></div>';
                    _html += '<div class="3"><h6>'+response.data.subject+'</h6><p>'+response.data.review+'</p>	</div>';
                
                    //prepend data into html
                    $('.review_list').prepend(_html)

                    //show avgr review
                    $('.avg_rat').text(response.avarage_rat.average)
                    $('.total_rat').text(response.total.count)

                    //stop making work again
                    $('.review_btn').prop('type', 'button');
                    e.preventDefault();
                    e.stopPropagation();
            }
        });
        //end ajax
        e.preventDefault();
    });

    // add product on wish list
    $(document).on('click', '#wish_list', function (e) {
        url = $(this).attr('data-url');
        
        // run ajax 
        $.ajax({
            type : 'GET',
            url : url,
            dataType : 'json',
            beforeSend :function () {
            },
            success :function (response) {
                console.log(response,'added');
                
                if (response.status == 'success'){
                Swal.fire({
                    icon: 'success',
                    title: response.message,
                    showConfirmButton: false,
                    timer: 800
                })
                }else{
                    Swal.fire({
                        icon: 'error',
                        title: response.message,
                        showConfirmButton: false,
                        timer: 800
                    })
                };
            }
        });
        //end ajax
        e.preventDefault();
    });

    //add shipping bill to checkout view
    $(document).on('click', '.ship', function (e) {
        e.preventDefault();
        _id = $(this).attr('data-cost');
        console.log(_id)
        _url = $(this).attr('data-url');

        //css
        $('.ship').removeClass('active');
        $('#ship-'+_id).addClass('active');

        data = {
            'id' : _id,
        }
        // run ajax 
        $.ajax({
            type : 'GET',
            url : _url,
            data : data,
            dataType : 'json',
            beforeSend :function () {
                $('.grand_total').text('Calculating...');
            },
            success :function (response) {
                console.log(response,response.grand_total);
                $('.grand_total').text('$'+response.grand_total);
                
            }
        });
        //end ajax
    });

});

