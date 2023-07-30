    

$(document).ready(function (){
    function renderChart(id, data, labels){
        const ctx = document.getElementById(id);
        new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
            label: 'Sales',
            data: data,
            backgroundColor: 'rgba(75, 13, 132, 0.3)',
            borderColor: 'rgba(75, 13, 132, 1)',
            fill: true,
            lineTension: 0.4,        
            radius: 6  ,
            borderWidth: 1
            }]
        },
        options: {
            scales: {
            y: {
                beginAtZero: true
            }
            }
        }
        });
    }
    function getSalesData(id, type){
        var url ="{% url 'sales_ajax_data' %}"
        var data = {
            type : type,
        }
        $.ajax({
            url : url,
            data : data,
            type : 'GET',
            beforeSend :function () {
                
            },
            success :function (response) {
                console.log(response)
                renderChart(id , response.data, response.labels)
            }, error: function(error){
                $.alert("an error ocur.")
            }
        });
    }

    //getSalesData('this_week_sales','week')
    //getSalesData('4_week_sales', '4weeks')

    var chartsToRender = $(".cfc-render-chart")
    $.each(chartsToRender, function(index, html){
        var Sthis = $(this)
        if(Sthis.attr('id') && Sthis.attr('data-type')){
            getSalesData(Sthis.attr('id') , Sthis.attr('data-type'))
        }
    })
    
    //$.ajax({
    //    url : url,
    //    data : data,
    //    type : 'GET',
    //    beforeSend :function () {
    //        
     //   },
    //    success :function (response) {
    //        console.log(response)
    //        renderChart('this_week_sales' , response.data, response.labels)
    //    }, error: function(error){
    //        $.alert("an error ocur.")
    //    }
    //});
    //end ajax

    // ajax 2
    
    //var url2 ="{% url 'sales_ajax_data' %}"
    //var data2 = {
    //    type : '4weeks'
    //}
    //$.ajax({
    //    url : url2,
    //    data : data2,
    //    type : 'GET',
    //    beforeSend :function () {
    ///        
    //    },
    //    success :function (response) {
    //        console.log(response)
    //        renderChart('4_week_sales' , response.data, response.labels)
    //        
    //   }, error: function(error){
    //        $.alert("an error ocur.")
    //    }
    //});
    //end ajax
});