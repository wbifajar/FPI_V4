function updateTotalMaterialCost(){
  
    var total = 0

    $('table#materialTable > tbody tr').each(function(index, value){
    
        var num = $(value).find('input.material-cost-price').val() 
        total +=  parseInt(num) ;

        // break loop before last row (last row is for showing total material cost)
        if( index == $('table#materialTable > tbody tr').length - 2 ){
            return false;
        }
    });
    $('#total-material-cost').text(total)
}

$('#submit-board-cost-from-number').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BoldMaterialCostFromNumber').val()
    
    $('table#materialTable > tbody tr').each(function(index, value){

        if(material_id == $(value).find('input.material-id').val() ){
            
            $(value).find('input.material-used-process').val(cost_value)
            var price = $(value).find('p.material-price').text()
            $(value).find('input.material-cost-price').val(cost_value * price)
            return false;
        }
    });

    updateTotalMaterialCost();
});