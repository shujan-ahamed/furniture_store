$(document).ready(function (){
    $('.ajaxLoader').hide();
    $(".filter-checkbox, .priceRangeBtn").on('click', function (){
        var _filterObj = {};
        var _min = $('#maxAmount').attr('min');
        var _max = $('#maxAmount').val();
        _filterObj.maxPrice = _max;
        _filterObj.minPrice = _min;
        console.log(_filterObj)
        $(".filter-checkbox").each(function(index,ele){
			var _filterVal=$(this).val();
			var _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
			    return el.value;
			});
		});
        // run ajax 
        $.ajax({
            url : '/marketplace/filter_data',
            data : _filterObj,
            dataType : 'json',
            beforeSend :function () {
                $('.ajaxLoader').show();
            },
            success :function (result) {
                $("#filtered_products").html(result.data);
                $('.ajaxLoader').hide();
            }
        });
        //end ajax
    });
});

