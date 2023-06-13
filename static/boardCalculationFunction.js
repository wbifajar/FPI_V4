function calculateFunctionsBoard(){
    calculateFromPartScale();
    calculateFromNum();
    updateBoardArray();
}


function disableButtonBoard(buttonId) {
    var buttonKGBoard = document.getElementById('buttonKGBoard');
    var buttonSheetBoard = document.getElementById('buttonSheetBoard');

    if (buttonId === 'buttonKGBoard') {
        buttonKGBoard.disabled = true;
        buttonSheetBoard.disabled = false;
        document.getElementById("priceBoard").innerHTML = "Price / KG";
        document.getElementById("weightBoard").innerHTML = "Weight (KG)";
        document.getElementById("priceBoardFromNum").innerHTML = "Price / KG";
        document.getElementById("priceBoardFromPartScale").innerHTML = "Price / KG";
    } else if (buttonId === 'buttonSheetBoard') {
        buttonKGBoard.disabled = false;
        buttonSheetBoard.disabled = true;
        document.getElementById("priceBoard").innerHTML = "Price / Sheet";
        document.getElementById("weightBoard").innerHTML = "Weight (Sheet)";
        document.getElementById("priceBoardFromNum").innerHTML = "Price / Sheet";
        document.getElementById("priceBoardFromPartScale").innerHTML = "Price / Sheet";
    }
}

function calculateFromNum(){
    var fromnum_verscale = document.getElementById("VerticalScaleFromNumber").value
    fromnum_verscale = fromnum_verscale == '' ? 0 : parseFloat(fromnum_verscale)
    var fromnum_horscale = document.getElementById("HorizontalScaleFromNumber").value
    fromnum_horscale = fromnum_horscale == '' ? 0 : parseFloat(fromnum_horscale)

    var verscale = document.getElementById("VerticalScaleMaterial").value
    verscale = verscale == '' ? 0 : parseFloat(verscale)
    var horscale = document.getElementById("HorizontalScaleMaterial").value
    horscale = horscale == '' ? 0 : parseFloat(horscale)
    var thickness = document.getElementById("ThicknessMaterial").value
    thickness = thickness == '' ? 0 : parseFloat(thickness)
    var specificgravity = document.getElementById("MaterialSpesificGravity").value
    thickness = thickness == '' ? 0 : parseFloat(thickness)

    var fromnum_exposed = document.getElementById("ExposedFromNumber").value
    fromnum_exposed = fromnum_exposed == '' ? 0 : parseFloat(fromnum_exposed)
    var fromnum_margin = document.getElementById("MarginFromNumber").value
    fromnum_margin = fromnum_margin == '' ? 0 : parseFloat(fromnum_margin)

    var fromnum_price = document.getElementById("PriceFromNumber").value
    fromnum_price = fromnum_price == '' ? 0 : parseFloat(fromnum_price)

    var numver = (fromnum_verscale - fromnum_exposed - (fromnum_margin/2)) / (verscale + fromnum_margin)
    numver = numver < 0 ? 0 : Math.floor(numver)
    $('#NumVerFromNumber').val(numver);

    var numhor = fromnum_horscale / (horscale + fromnum_margin)
    numhor = numhor < 0 ? 0 : Math.floor(numhor)
    $('#NumHorFromNumber').val(numhor);
    
    var qtypersheet = numver * numhor
    $('#QtyPerSheetFromNumber').val(qtypersheet);
    $('#QtyFromNumber').val(qtypersheet);
    
    var weightfromnum = (fromnum_verscale * fromnum_horscale * thickness * specificgravity) / 1000000
    $('#WeightFromNumber').val(weightfromnum);

    var weightperqty = weightfromnum / qtypersheet
    weightperqty = weightperqty.toFixed(2);
    $('#WeightPerQtyFromNumber').val(weightperqty);
    $('#WeightFromNumber2').val(weightperqty);
    $('#WeightFromNumber3').val(weightperqty);
    
    var fromnum_materialcost = fromnum_price * weightperqty
    fromnum_materialcost = fromnum_materialcost.toFixed(2);
    $('#MaterialCostFromNumber').val(fromnum_materialcost);
    $('#BoldMaterialCostFromNumber').val(fromnum_materialcost);
    
    $('#FromNumPreviewMargin1').val(fromnum_margin);
    $('#FromNumPreviewMargin2').val(fromnum_margin);
    var halfmargin = fromnum_margin / 2
    $('#FromNumPreviewHalfMargin1').val(halfmargin);
    $('#FromNumPreviewHalfMargin2').val(halfmargin);
    $('#FromNumPreviewExposed').val(fromnum_exposed);

    
    $('#FromNumPreviewVerScale').val(verscale);
    $('#FromNumPreviewHorScale').val(horscale);
    $('#FromPartPreviewVerScale').val(verscale);
    $('#FromPartPreviewHorScale').val(horscale);

    
    $('#FromNumPreviewVerScale').text(verscale);
    $('#FromNumPreviewHorScale').text(horscale);
    $('#FromPartPreviewVerScale').text(verscale);
    $('#FromPartPreviewHorScale').text(horscale);

    updateBoardArray();
}

function calculateFromPartScale(){
    var verscale = document.getElementById("VerticalScaleMaterial").value
    verscale = verscale == '' ? 0 : parseFloat(verscale)
    var horscale = document.getElementById("HorizontalScaleMaterial").value
    horscale = horscale == '' ? 0 : parseFloat(horscale)
    var thickness = document.getElementById("ThicknessMaterial").value
    thickness = thickness == '' ? 0 : parseFloat(thickness)

    var specificgravity = document.getElementById("MaterialSpesificGravity").value
    thickness = thickness == '' ? 0 : parseFloat(thickness)

    var exposedfrompart = document.getElementById("ExposedFromPart").value
    exposedfrompart = exposedfrompart == '' ? 10 : parseFloat(exposedfrompart)
    var marginfrompart = document.getElementById("MarginFromPart").value
    marginfrompart = marginfrompart == '' ? 20 : parseFloat(marginfrompart)

    var price = document.getElementById("MaterialPrice").value
    price = price == '' ? 0 : parseFloat(price) 

    // WeightFromPart

    var weightfrompart = ((verscale + exposedfrompart) * (horscale + marginfrompart) * thickness * specificgravity) / 1000000
    weightfrompart = weightfrompart.toFixed(2);
    var materialcostfrompart = weightfrompart * price
    materialcostfrompart = materialcostfrompart.toFixed(2);


    $('#FromPartScalePreviewMargin').val(marginfrompart);
    $('#FromPartScalePreviewExposed').val(exposedfrompart);
    var halfscale = marginfrompart / 2;
    $('#FromPartScalePreviewMargin1').val(marginfrompart);
    $('#FromPartScalePreviewHalfMargin').val(halfscale);

    $('#WeightFromPart').val(weightfrompart);
    $('#WeightFromPart2').val(weightfrompart);
    $('#WeightFromPart3').val(weightfrompart);
    $('#MaterialCostFromPart').val(materialcostfrompart);
    $('#BoldMaterialCostFromPart').val(materialcostfrompart);

    

    updateBoardArray(); 
}

