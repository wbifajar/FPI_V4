$('#submit-board-cost-from-number').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BoldMaterialCostFromNumber').val()
    
    $('table#materialTable > tbody tr').each(function(index, value){

   
        if(material_id == $(value).find('input.material-id').val() ){
            console.log(index);
            $(value).find('input.material-used-process').val(cost_value)
            return false;
        }
    })
});