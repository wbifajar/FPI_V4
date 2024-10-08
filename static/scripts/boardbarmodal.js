
const modal1 = document.getElementById('exampleModal1')

modal1.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute('data-bs-index')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    const modalTitle = modal1.querySelector('.modal-title')

    modalTitle.textContent = `New message to ${recipient}`
 
    console.log($('#show-modal-board'));
    $('#show-modal-board').attr('data-bs-index', recipient)
    $('#show-modal-bar').attr('data-bs-index', recipient)
})

const modal2 = document.getElementById('exampleModal2')
const modal3 = document.getElementById('exampleModal3')



// find index of material id in array of board input value (if existed) if not return -1
function findIndexOfMaterialId(arr, num){
    for(var i = 0; i < arr.length; i++){
        console.log("ADSADASD = ", arr[i][0], num)
        if(  arr[i][0] == num){
            console.log("sama = ", arr[i][0], num)
            return i
        }
    }
    return -1
}

modal2.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget

    // id modal board yang akan dibuka oleh button ini
    const recipient = button.getAttribute('data-bs-index')
    const modalTitle = modal2.querySelector('.modal-title')

    modalTitle.textContent = `This is modal with id : ${recipient}`
    // set attribute data-bs-index ke modal board yang akan dibuka
    $('#board-modal-content').attr('data-bs-index', recipient);

    // when board modal triggered,
    // fill value in board modal if already existed before
    var index = findIndexOfMaterialId(boardArr, recipient)

    $('#BoardMaterialId').val( boardArr[index][1] )
    $('#BoardMaterialName').val( boardArr[index][2] )

    $("#VerticalScaleMaterial").val( boardArr[index][3] )
    $("#HorizontalScaleMaterial").val( boardArr[index][4] )
    $("#ThicknessMaterial").val( boardArr[index][5] )

    $("#MaterialSpesificGravity").val( boardArr[index][6] )
    $("#MaterialPrice").val( boardArr[index][7] )

    // === FROM NUMBER OF PART =====
    $("#VerticalScaleFromNumber").val( boardArr[index][8] )
    $("#HorizontalScaleFromNumber").val( boardArr[index][9] )

    $("#ExposedFromNumber").val( boardArr[index][10] )
    $("#MarginFromNumber").val( boardArr[index][11] )

    $('#NumVerFromNumber').val( boardArr[index][12] );
    $('#NumHorFromNumber').val( boardArr[index][13] );
    $('#QtyPerSheetFromNumber').val( boardArr[index][14] );

    $('#WeightFromNumber').val( boardArr[index][15] );
    $('#QtyFromNumber').val( boardArr[index][16] );
    $('#WeightPerQtyFromNumber').val( boardArr[index][17] );

    $('#PriceFromNumber').val( boardArr[index][18] )
    $('#WeightFromNumber2').val( boardArr[index][19] );
    $('#MaterialCostFromNumber').val( boardArr[index][20] );
    
    $('#BoldMaterialCostFromNumber').val( boardArr[index][21] );

    // === END FROM NUMBER OF PART =====

    // ==== FROM PART OF PART =====
    $("#ExposedFromPart").val(boardArr[index][22])
    $("#MarginFromPart").val(boardArr[index][23])    

    $('#WeightFromPart').val(boardArr[index][24]);

    $('#PriceFromPart').val(boardArr[index][25]);
    $('#WeightFromPart2').val(boardArr[index][26]);
    $('#MaterialCostFromPart').val(boardArr[index][27])

    $('#BoldMaterialCostFromPart').val(boardArr[index][28])
    

})

function updateBoardArray(){
    var index = $('#board-modal-content').attr('data-bs-index')
    var materialid = $('#BoardMaterialId').val()
    var materialname = $('#BoardMaterialName').val()

    var verscale = $("#VerticalScaleMaterial").val()
    var horscale = $("#HorizontalScaleMaterial").val()
    var thickness = $("#ThicknessMaterial").val()

    var specificgravity = $("#MaterialSpesificGravity").val()
    var price = $("#MaterialPrice").val()

    // === FROM NUMBER OF PART =====
    var fromnum_verscale = $("#VerticalScaleFromNumber").val()
    var fromnum_horscale = $("#HorizontalScaleFromNumber").val()

    var fromnum_exposed = $("#ExposedFromNumber").val()
    var fromnum_margin = $("#MarginFromNumber").val()

    var numver = $('#NumVerFromNumber').val();
    var numhor = $('#NumHorFromNumber').val();
    var qtypersheet = $('#QtyPerSheetFromNumber').val();

    var weightfromnum = $('#WeightFromNumber').val();
    var qtyfromnumber =  $('#QtyFromNumber').val();
    var weightperqty = $('#WeightPerQtyFromNumber').val();

    var pricefromnum = $('#PriceFromNumber').val()
    var weightfromnum2 = $('#WeightFromNumber2').val();
    var fromnum_materialcost = $('#MaterialCostFromNumber').val();
    
    var boldmaterialcost = $('#BoldMaterialCostFromNumber').val();

    // === END FROM NUMBER OF PART =====

    // ==== FROM PART OF PART =====
    var exposedfrompart = $("#ExposedFromPart").val()
    var marginfrompart = $("#MarginFromPart").val()    

    var weightfrompart =  $('#WeightFromPart').val();

    var pricefrompart =  $('#PriceFromPart').val();
    var weightfrompart2 =  $('#WeightFromPart2').val();
    var materialcostfrompart = $('#MaterialCostFromPart').val()

    var boldmaterialcostfrompart =  $('#BoldMaterialCostFromPart').val()
    // ==== END FROM PART OF PART =====
    var arrBoardInputFieldValue = [
        index, //0
        materialid, //1
        materialname, //2
        verscale, //3
        horscale, //4
        thickness, //5
        specificgravity, //6
        price, //7
        fromnum_verscale, //8
        fromnum_horscale, //9
        fromnum_exposed, //10
        fromnum_margin, //11
        numver, //12
        numhor, //13
        qtypersheet, //14
        weightfromnum, //15
        qtyfromnumber, //16
        weightperqty, //17
        pricefromnum, //18
        weightfromnum2, //19
        fromnum_materialcost, //20
        boldmaterialcost, //21
        exposedfrompart, //22
        marginfrompart, //23
        weightfrompart, //24
        pricefrompart, //25
        weightfrompart2, //26
        materialcostfrompart, //27
        boldmaterialcostfrompart //28
    ]

    // update value board array
    target = findIndexOfMaterialId(boardArr, index)
    boardArr[target] = arrBoardInputFieldValue
    $('#BoardArr').val(boardArr)

}

//delete board arr by index
function updateBoardArrayDelete(index){
    boardArr.splice(index, 1);
}


modal3.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget

    // id modal board yang akan dibuka oleh button ini
    const recipient = button.getAttribute('data-bs-index')
    const modalTitle = modal3.querySelector('.modal-title')

    modalTitle.textContent = `This is modal with id : ${recipient}`
    // set attribute data-bs-index ke modal board yang akan dibuka
    $('#bar-modal-content').attr('data-bs-index', recipient);

    // when board modal triggered,
    // fill value in bar modal if already existed before
    var index = findIndexOfMaterialId(barArr, recipient)
    if( index != -1 ){
        console.log('ISII INI MODAL FIELD INPUTNYA', index);
        $('#BarMaterialId').val( barArr[index][1] )
        $('#BarMaterialName').val( boardArr[index][2] )

        $("#BarPartScaleMaterial").val( barArr[index][3] )
        $("#BarDiameterMaterial").val( barArr[index][4] )

        $("#BarMaterialSpesificGravity").val( barArr[index][5] )
        $("#BarMaterialPrice").val( barArr[index][6] )
        
        $("BarCalcNumExposed").val( barArr[index][7] )
        $("BarCalcNumRoundBa").val( barArr[index][8] )
        $("BarCalcNumEdgeLoss").val( barArr[index][9] )

        $('#BarCalcNumMtrlCost').val( barArr[index][10] );
        $('#BarCalcNumNum').val( barArr[index][11] );
        $('#BarCalcNumScla').val( barArr[index][12] );
        $('#BarCalcNumUsedQty').val( barArr[index][13] );

        $('#BarCalcNumBoldMaterialCost').val( barArr[index][14] )

        $("BarFromScaleKerfLoss").val( barArr[index][15] )
        $('#BarFromScaleUsedQty').val( barArr[index][16] );
        $('#BarFromScaleMaterialCost').val( barArr[index][17] );
    }else{
        $('#BarMaterialId').val( '')
        $('#BarMaterialName').val( '' )

        $("#BarPartScaleMaterial").val( '' )
        $("#BarDiameterMaterial").val( '' )

        $("#BarMaterialSpesificGravity").val( '' )
        $("#BarMaterialPrice").val( '' )
        
        $("#BarCalcNumExposed").val( '' )
        $("#BarCalcNumRoundBa").val( '' )
        $("#BarCalcNumEdgeLoss").val( '' )

        $('#BarCalcNumMtrlCost').val( '' );
        $('#BarCalcNumNum').val( '' );
        $('#BarCalcNumScla').val( '' );
        $('#BarCalcNumUsedQty').val( '' );

        $('#BarCalcNumBoldMaterialCost').val( '' )

        $("BarFromScaleKerfLoss").val( '' )
        $('#BarFromScaleUsedQty').val( '' );
        $('#BarFromScaleMaterialCost').val( '' );
    }

})


function updateBarArray(){
    var index = $('#bar-modal-content').attr('data-bs-index')
    var materialid = $('#BarMaterialId').val()
    var materialname = $('#BarMaterialName').val()

    var bar_partscale = $("#BarPartScaleMaterial").val()
    var bar_diameter = $("#BarDiameterMaterial").val()

    var bar_specgravity = $("#BarMaterialSpesificGravity").val()
    var bar_price = $("#BarMaterialPrice").val()
    
    var bar_calcnum_exposed =$("#BarCalcNumExposed").val()
    var bar_calcnum_round_ba =$("#BarCalcNumRoundBa").val()
    var bar_calcnum_edge_loss =$("#BarCalcNumEdgeLoss").val()

    var bar_material_cost = $('#BarCalcNumMtrlCost').val();
    var bar_num = $('#BarCalcNumNum').val();
    var bar_scala = $('#BarCalcNumScla').val();
    var bar_used_qty = $('#BarCalcNumUsedQty').val();

    var bold_material_cost = $('#BarCalcNumBoldMaterialCost').val()

    var bar_kerf_loss = $("#BarFromScaleKerfLoss").val()
    var bar_used_qty_from_scale = $('#BarFromScaleUsedQty').val();
    var bar_from_scale_material_cost = $('#BarFromScaleMaterialCost').val();
    
    // ==== END FROM PART OF PART =====
    var arrBarInputFieldValue = [
        index, //0
        materialid, //1
        materialname, //2
        bar_partscale, //3
        bar_diameter, //4
        bar_specgravity, //5
        bar_price, //6
        bar_calcnum_exposed, //7
        bar_calcnum_round_ba, //8
        bar_calcnum_edge_loss, //9
        bar_material_cost, //10
        bar_num, //11
        bar_scala, //12
        bar_used_qty, //13
        bold_material_cost, //14
        bar_kerf_loss, //15
        bar_used_qty_from_scale, //16
        bar_from_scale_material_cost, //17
    ]

    // update value board array
    target = findIndexOfMaterialId(barArr, index)
    barArr[target] = arrBarInputFieldValue

    $('#BarArr').val(barArr)
    console.log(barArr);
}