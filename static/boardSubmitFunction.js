$('#submit-board-cost-from-number').on('click', function(){
    var material_id = $('#board-modal-content').attr('data-bs-index');
    var cost_value = $('#BoldMaterialCostFromNumber').val()
    
    $('table#materialTable > tbody tr').each(function(index, value){

   
        if(material_id == $(value).find('input.material-id').val() ){
            console.log(index);
            $(value).find('input.material-used-process').val(cost_value)
            var price = $(value).find('p.material-price').text()
            console.log("Price = ", price);
            $(value).find('input.material-cost-price').val(cost_value * price)
            return false;
        }
    })
});