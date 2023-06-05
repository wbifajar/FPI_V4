function updateTotalMaterialCostOnModal(){
  
    var total = 0
    
    $('table#materialTable > tbody tr').each(function(index, value){
    
        var num = $(value).find('input.material-cost-price').val() 
        total +=  parseInt(num);

        // break loop before last row (last row is for showing total material cost)
        if( index == $('table#materialTable > tbody tr').length - 2 ){
            return false;
        }
    });

    if($('table#materialTable > tbody tr').length == 1){
        total = 0
    }
    
    $('#total-material-cost').text(total)
}

$('#submit-board-cost-from-number').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BoldMaterialCostFromNumber').val()
    
    // looping buat nyari index ke berapa yg di 
    // harus di update di material table
    $('table#materialTable > tbody tr').each(function(index, value){

        if(material_id == $(value).find('input.material-id').val() ){
            
            // update used quantity di material table
            $(value).find('input.material-used-process').val(cost_value)

            // update material cost di material table dari used quantity * price
            var price = $(value).find('p.material-price').text()
            $(value).find('input.material-cost-price').val(cost_value * price)
            return false;
        }
    });

    updateTotalMaterialCostOnModal();
});

$('#submit-board-cost-from-part-scale').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BoldMaterialCostFromPart').val()
    
    // looping buat nyari index ke berapa yg di 
    // harus di update di material table
    $('table#materialTable > tbody tr').each(function(index, value){

        if(material_id == $(value).find('input.material-id').val() ){
            
            // update used quantity di material table
            $(value).find('input.material-used-process').val(cost_value)

            // update material cost di material table dari used quantity * price
            var price = $(value).find('p.material-price').text()
            $(value).find('input.material-cost-price').val(cost_value * price)
            return false;
        }
    });

    updateTotalMaterialCostOnModal();
});



$('#submit-bar-cost-from-num').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BarCalcNumBoldMaterialCost').val()
    
    // looping buat nyari index ke berapa yg di 
    // harus di update di material table
    $('table#materialTable > tbody tr').each(function(index, value){

        if(material_id == $(value).find('input.material-id').val() ){
            
            // update used quantity di material table
            $(value).find('input.material-used-process').val(cost_value)

            // update material cost di material table dari used quantity * price
            var price = $(value).find('p.material-price').text()
            $(value).find('input.material-cost-price').val(cost_value * price)
            return false;
        }
    });

    updateTotalMaterialCostOnModal();
});


$('#submit-bar-cost-from-scale').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BarFromScaleMaterialCost').val()
    
    // looping buat nyari index ke berapa yg di 
    // harus di update di material table
    $('table#materialTable > tbody tr').each(function(index, value){

        if(material_id == $(value).find('input.material-id').val() ){
            
            // update used quantity di material table
            $(value).find('input.material-used-process').val(cost_value)

            // update material cost di material table dari used quantity * price
            var price = $(value).find('p.material-price').text()
            $(value).find('input.material-cost-price').val(cost_value * price)
            return false;
        }
    });

    updateTotalMaterialCostOnModal();
});