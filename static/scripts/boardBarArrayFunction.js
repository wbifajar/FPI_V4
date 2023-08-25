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
        index,
        materialid,
        materialname,
        verscale,
        horscale,
        thickness,
        specificgravity,
        price,
        fromnum_verscale,
        fromnum_horscale, //10
        fromnum_exposed,
        fromnum_margin, 
        numver,
        numhor,
        qtypersheet, //15
        weightfromnum,
        qtyfromnumber, 
        weightperqty,
        pricefromnum,
        weightfromnum2, //20
        fromnum_materialcost, 
        boldmaterialcost,
        exposedfrompart,
        marginfrompart,
        weightfrompart, //25
        pricefrompart,
        weightfrompart2,
        materialcostfrompart,
        boldmaterialcostfrompart
    ]

    // update value board array
    target = findIndexOfMaterialId(boardArr, materialid)
    boardArr[target] = arrBoardInputFieldValue
    $('#BoardArr').val(boardArr)
}



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
        index,
        materialid,
        materialname,
        bar_partscale,
        bar_diameter,
        bar_specgravity,
        bar_price,
        bar_calcnum_exposed,
        bar_calcnum_round_ba,
        bar_calcnum_edge_loss,
        bar_material_cost,
        bar_num,
        bar_scala,
        bar_used_qty,
        bold_material_cost,
        bar_kerf_loss,
        bar_used_qty_from_scale,
        bar_from_scale_material_cost,
    ]

    // update value board array
    target = findIndexOfMaterialId(barArr, index)
    barArr[target] = arrBarInputFieldValue

    $('#BarArr').val(barArr)
}

//delete board arr by index
function updateBoardArrayDelete(index){
    boardArr.splice(index, 1);
}