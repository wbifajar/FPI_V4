function updateMaterialCostOnModal(material_id, cost_value){
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
}

$('#submit-board-cost-from-number').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BoldMaterialCostFromNumber').val()
    
    updateMaterialCostOnModal(material_id, cost_value);
    updateTotalMaterialCostOnModal();
});

$('#submit-board-cost-from-part-scale').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BoldMaterialCostFromPart').val()
    
    updateMaterialCostOnModal(material_id, cost_value);
    updateTotalMaterialCostOnModal();
});


$('#submit-bar-cost-from-num').on('click', function(){
    var material_id = $('#bar-modal-content').attr('data-bs-index');
    var cost_value = $('#BarCalcNumBoldMaterialCost').val()
    
    updateMaterialCostOnModal(material_id, cost_value);
    updateTotalMaterialCostOnModal();
});


$('#submit-bar-cost-from-scale').on('click', function(){
    var material_id = $('#bar-modal-content').attr('data-bs-index');
    var cost_value = $('#BarFromScaleMaterialCost').val()
    
    updateMaterialCostOnModal(material_id, cost_value);
    updateTotalMaterialCostOnModal();
});