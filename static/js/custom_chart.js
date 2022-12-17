$( document ).ready(function() {
  var value = ''
  var url = ''
  var range = '1y'
  var interval = '1d'
  $(".show_chart").on('click', function(){
    value = $(this).attr('data-symbol')
    url = $(this).attr('data-url')
    let container_id = document.getElementsByTagName("svg")[0]
    document.getElementById(container_id.id).id = "container"+value
    d3.select("#hello").remove()
    get_data(value, range, interval)
  })
  $(".chart_range").on('click', function(){
    range = $(this).attr('data-range')
    get_data(value, range, interval)
    d3.select("#hello").remove()
  })

  $(".chart_interval").on('click', function(){
    interval = $(this).attr('data-interval')
    get_data(value, range, interval)
    d3.select("#hello").remove()
  })
});

function get_data(symbol, range, interval){
  $.ajax({
    type: "get",
    url: `/stocks/chart-data/${symbol}/${interval}/${range}`,
    success: function(data){
      $.getScript("/static/js/candle_chart.js", function(){
        chart(data, symbol)
      })

    }
  })
}