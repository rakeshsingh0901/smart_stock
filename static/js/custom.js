$(document).ready(function(){
  $(".bookmark").on('change', function(){
    let value = this.value.split('-')
    let bookmark_id = value[0]
    let symbol = value[1]
    $.ajax({
      type: "get",
      url: `/stocks/add/bookmark/${bookmark_id}/item/${symbol}`,
      success: function(data){
        console.log("Added", data)
      }
    })
  })
});