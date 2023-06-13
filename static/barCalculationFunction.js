 // function setValuePreviewBar(){
//     var halfkerf1 = document.getElementById("#BarFromScalePreviewHalfKerf1");
//     var halfkerf2 = document.getElementById("#BarFromScalePreviewHalfKerf2");
//     var diameter = document.getElementById("#BarFromScalePreviewDiameter");
//     var partscale = document.getElementById("#BarFromScalePreviewPartScale");
//     halfkerf1.innerHTML = "0";
//     halfkerf2.innerHTML = "0";
//     diameter.innerHTML = "0";
//     partscale.innerHTML = "0";
// }

function disableButtonBar(buttonId) {
    var buttonKGBar = document.getElementById('buttonKGBar');
    var buttonSheetBar = document.getElementById('buttonSheetBar');

    if (buttonId === 'buttonKGBar') {
        buttonKGBar.disabled = true;
        buttonSheetBar.disabled = false;

    } else if (buttonId === 'buttonSheetBar') {
        buttonKGBar.disabled = false;
        buttonSheetBar.disabled = true;
    }
}

function getPartBar(val){
    var partName = document.getElementById('BarMaterialName').value;
    var part = '{{partjs|safe}}';
    const obj = JSON.parse(part);
    var selectedPart = obj.find(element => element.name == partName);


    console.log(selectedPart);
    $('#BarMaterialId').val(selectedPart.idPart);
    $('#BarMaterialSpesificGravity').val(selectedPart.spesificGravity);
    $('#BarMaterialPrice').val(selectedPart.price);

    calculateFunctionsBar();
    getFromNumPreviewValues();
}

function calculateFunctionsBar(){
    calculateNumOfQty();
    calculateFromScale();
    updateBarArray();
}

function calculateFromScale(){
    var bar_partscale = document.getElementById("BarPartScaleMaterial").value
    bar_partscale = bar_partscale == '' ? 0 : parseFloat(bar_partscale)
    var bar_diameter = document.getElementById("BarDiameterMaterial").value
    bar_diameter = bar_diameter == '' ? 0 : parseFloat(bar_diameter)

    var bar_specgravity = document.getElementById("BarMaterialSpesificGravity").value
    bar_specgravity = bar_specgravity == '' ? 0 : parseFloat(bar_specgravity)
    var bar_price = document.getElementById("BarMaterialPrice").value
    bar_price = bar_price == '' ? 0 : parseFloat(bar_price)

    var bar_kerf_loss = document.getElementById("BarFromScaleKerfLoss").value
    bar_kerf_loss = bar_kerf_loss == '' ? 0 : parseFloat(bar_kerf_loss) 

    var used_qty = 3.14 * (Math.pow((bar_diameter/2), 2)) * ((bar_partscale + bar_kerf_loss)) * bar_specgravity
    used_qty = used_qty / 1000000
    $('#BarFromScaleUsedQty').val(used_qty);

    var bar_material_cost = used_qty * bar_price
    bar_material_cost = bar_material_cost.toFixed(2);
    $('#BarFromScaleMaterialCost').val(bar_material_cost);

    var half_bar_kerf_loss = bar_kerf_loss / 2
    $('#BarFromScalePreviewHalfKerf1').val(half_bar_kerf_loss);
    $('#BarFromScalePreviewHalfKerf2').val(half_bar_kerf_loss);
    $('#BarFromScalePreviewDiameter').val(bar_diameter);
    $('#BarFromScalePreviewPartScale').val(bar_partscale);
    updateBarArray();
}

function calculateNumOfQty(){
    var bar_partscale = document.getElementById("BarPartScaleMaterial").value
    bar_partscale = bar_partscale == '' ? 0 : parseFloat(bar_partscale)
    var bar_diameter = document.getElementById("BarDiameterMaterial").value
    bar_diameter = bar_diameter == '' ? 0 : parseFloat(bar_diameter)

    var bar_specgravity = document.getElementById("BarMaterialSpesificGravity").value
    bar_specgravity = bar_specgravity == '' ? 0 : parseFloat(bar_specgravity)
    var bar_price = document.getElementById("BarMaterialPrice").value
    bar_price = bar_price == '' ? 0 : parseFloat(bar_price)

    var bar_calcnum_exposed = document.getElementById("BarCalcNumExposed").value
    bar_calcnum_exposed = bar_calcnum_exposed == '' ? 0 : parseFloat(bar_calcnum_exposed)
    var bar_calcnum_round_ba = document.getElementById("BarCalcNumRoundBa").value
    bar_calcnum_round_ba = bar_calcnum_round_ba == '' ? 0 : parseFloat(bar_calcnum_round_ba)
    var bar_calcnum_edge_loss = document.getElementById("BarCalcNumEdgeLoss").value
    bar_calcnum_edge_loss = bar_calcnum_edge_loss == '' ? 0 : parseFloat(bar_calcnum_edge_loss)

    var bar_kerf_loss = document.getElementById("BarFromScaleKerfLoss").value
    bar_kerf_loss = bar_kerf_loss == '' ? 0 : parseFloat(bar_kerf_loss)

    var bar_material_cost = ((3.14 * (Math.pow((bar_diameter/2), 2)) * bar_calcnum_round_ba * bar_specgravity)/1000000) * bar_price
    $('#BarCalcNumMtrlCost').val(bar_material_cost);

    
    $('#Exposed2').val(bar_calcnum_exposed);
    $('#Scala2').val(bar_partscale);
    $('#EdgeLoss2').val(bar_calcnum_edge_loss);
    $('#DiameterBar2').val(bar_calcnum_round_ba);
    $('#OutlineScalePart').val(bar_partscale);
    $('#OutlineScaleDiameter').val(bar_diameter);

    var bar_num = (bar_calcnum_round_ba - bar_calcnum_exposed - bar_calcnum_edge_loss) / (bar_partscale + bar_kerf_loss)
    bar_num = bar_num < 0 ? 0 : Math.floor(bar_num)
    $('#BarCalcNumNum').val(bar_num);
    
    $('#BarCalcNumScla').val(bar_partscale);

    var bar_used_qty = bar_material_cost / bar_num / bar_price
    $('#BarCalcNumUsedQty').val(bar_used_qty);

    var bold_material_cost = bar_material_cost / bar_num
    $('#BarCalcNumBoldMaterialCost').val(bold_material_cost)

    // $('#BarCalcNumPreviewExposed').text(bar_calcnum_exposed)
    // $('#BarCalcNumPreviewScla').text(bar_partscale)
    // $('#BarCalcNumPreviewEdgeLoss').text(bar_calcnum_edge_loss)
    // $('#BarCalcNumPreviewRoundBa').text(bar_calcnum_round_ba)
    updateBarArray();
}