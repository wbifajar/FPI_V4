
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

var boardarr = [[]]
var bararr = [[]]

// find index of material id in array of board input value (if existed) if not return -1
function findIndexOfMaterialId(arr, num){
    for(var i = 0; i < arr.length; i++){
        console.log("ADSADASD = ", arr[i][0], num)
        if(arr[i][0] === num){
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
    var index = findIndexOfMaterialId(boardarr, recipient)
    if( index != -1 ){
        console.log('ISII INI MODAL FIELD INPUTNYA', index);
        $('#BoardMaterialId').val( boardarr[index][1] )
        $('#BoardMaterialName').val( boardarr[index][2] )

        $("#VerticalScaleMaterial").val( boardarr[index][3] )
        $("#HorizontalScaleMaterial").val( boardarr[index][4] )
        $("#ThicknessMaterial").val( boardarr[index][5] )

        $("#MaterialSpesificGravity").val( boardarr[index][6] )
        $("#MaterialPrice").val( boardarr[index][7] )

        // === FROM NUMBER OF PART =====
        $("#VerticalScaleFromNumber").val( boardarr[index][8] )
        $("#HorizontalScaleFromNumber").val( boardarr[index][9] )

        $("#ExposedFromNumber").val( boardarr[index][10] )
        $("#MarginFromNumber").val( boardarr[index][11] )

        $('#NumVerFromNumber').val( boardarr[index][12] );
        $('#NumHorFromNumber').val( boardarr[index][13] );
        $('#QtyPerSheetFromNumber').val( boardarr[index][14] );

        $('#WeightFromNumber').val( boardarr[index][15] );
        $('#QtyFromNumber').val( boardarr[index][16] );
        $('#WeightPerQtyFromNumber').val( boardarr[index][17] );

        $('#PriceFromNumber').val( boardarr[index][18] )
        $('#WeightFromNumber2').val( boardarr[index][19] );
        $('#MaterialCostFromNumber').val( boardarr[index][20] );
        
        $('#BoldMaterialCostFromNumber').val( boardarr[index][21] );

        // === END FROM NUMBER OF PART =====

        // ==== FROM PART OF PART =====
        $("#ExposedFromPart").val(boardarr[index][22])
        $("#MarginFromPart").val(boardarr[index][23])    

        $('#WeightFromPart').val(boardarr[index][24]);

        $('#PriceFromPart').val(boardarr[index][25]);
        $('#WeightFromPart2').val(boardarr[index][26]);
        $('#MaterialCostFromPart').val(boardarr[index][27])

        $('#BoldMaterialCostFromPart').val(boardarr[index][28])
    }else{
        console.log('ISII INI MODAL FIELD INPUTNYA', index);
        $('#BoardMaterialId').val(  '' )
        $('#BoardMaterialName').val(  '' )

        $("#VerticalScaleMaterial").val(  '' )
        $("#HorizontalScaleMaterial").val(  '' )
        $("#ThicknessMaterial").val(  '' )

        $("#MaterialSpesificGravity").val(  '' )
        $("#MaterialPrice").val(  '' )

        // === FROM NUMBER OF PART =====
        $("#VerticalScaleFromNumber").val(  '' )
        $("#HorizontalScaleFromNumber").val(  '' )

        $("#ExposedFromNumber").val(  ''  )
        $("#MarginFromNumber").val(  ''  )

        $('#NumVerFromNumber').val(  ''  );
        $('#NumHorFromNumber').val(  ''  );
        $('#QtyPerSheetFromNumber').val(  ''  );

        $('#WeightFromNumber').val(  ''  );
        $('#QtyFromNumber').val(  ''  );
        $('#WeightPerQtyFromNumber').val(  ''  );

        $('#PriceFromNumber').val(  ''  )
        $('#WeightFromNumber2').val(  ''  );
        $('#MaterialCostFromNumber').val(  ''  );
        
        $('#BoldMaterialCostFromNumber').val(  ''  );

        // === END FROM NUMBER OF PART =====

        // ==== FROM PART OF PART =====
        $("#ExposedFromPart").val( '' )
        $("#MarginFromPart").val( '' )    

        $('#WeightFromPart').val( '' );

        $('#PriceFromPart').val( '' );
        $('#WeightFromPart2').val( '' );
        $('#MaterialCostFromPart').val( '' )

        $('#BoldMaterialCostFromPart').val( '' )
    }

    console.log(boardarr);

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
        index,
        materialid,
        materialname,
        verscale,
        horscale,
        thickness,
        specificgravity,
        price,
        fromnum_verscale,
        fromnum_horscale,
        fromnum_exposed,
        fromnum_margin, //10
        numver,
        numhor,
        qtypersheet,
        weightfromnum,
        qtyfromnumber, //15
        weightperqty,
        pricefromnum,
        weightfromnum2,
        fromnum_materialcost,
        boldmaterialcost,
        exposedfrompart,
        marginfrompart,
        weightfrompart,
        pricefrompart,
        weightfrompart2,
        materialcostfrompart,
        boldmaterialcostfrompart
    ]

    // kalo belom ada create baru, kalo belom ada update
    target = findIndexOfMaterialId(boardarr, index)
    if( target == -1 ){
        boardarr.push(arrBoardInputFieldValue);
    }else{
        boardarr[target] = arrBoardInputFieldValue
    }

    console.log(boardarr);
}


// modal3.addEventListener('show.bs.modal', event => {
//     // Button that triggered the modal
//     const button = event.relatedTarget

//     // id modal board yang akan dibuka oleh button ini
//     const recipient = button.getAttribute('data-bs-index')
//     const modalTitle = modal2.querySelector('.modal-title')

//     modalTitle.textContent = `This is modal with id : ${recipient}`
//     // set attribute data-bs-index ke modal board yang akan dibuka
//     $('#bar-modal-content').attr('data-bs-index', recipient);

//     // when board modal triggered,
//     // fill value in board modal if already existed before
//     var index = findIndexOfMaterialId(bararr, recipient)
//     if( index != -1 ){
//         console.log('ISII INI MODAL FIELD INPUTNYA', index);
//         $('#BarMaterialId').val( boardarr[index][1] )
//         $('#BarMaterialName').val( boardarr[index][2] )

//         $("#VerticalScaleMaterial").val( boardarr[index][3] )
//         $("#HorizontalScaleMaterial").val( boardarr[index][4] )
//         $("#ThicknessMaterial").val( boardarr[index][5] )

//         $("#MaterialSpesificGravity").val( boardarr[index][6] )
//         $("#MaterialPrice").val( boardarr[index][7] )

//         // === FROM NUMBER OF PART =====
//         $("#VerticalScaleFromNumber").val( boardarr[index][8] )
//         $("#HorizontalScaleFromNumber").val( boardarr[index][9] )

//         $("#ExposedFromNumber").val( boardarr[index][10] )
//         $("#MarginFromNumber").val( boardarr[index][11] )

//         $('#NumVerFromNumber').val( boardarr[index][12] );
//         $('#NumHorFromNumber').val( boardarr[index][13] );
//         $('#QtyPerSheetFromNumber').val( boardarr[index][14] );

//         $('#WeightFromNumber').val( boardarr[index][15] );
//         $('#QtyFromNumber').val( boardarr[index][16] );
//         $('#WeightPerQtyFromNumber').val( boardarr[index][17] );

//         $('#PriceFromNumber').val( boardarr[index][18] )
//         $('#WeightFromNumber2').val( boardarr[index][19] );
//         $('#MaterialCostFromNumber').val( boardarr[index][20] );
        
//         $('#BoldMaterialCostFromNumber').val( boardarr[index][21] );

//         // === END FROM NUMBER OF PART =====

//         // ==== FROM PART OF PART =====
//         $("#ExposedFromPart").val(boardarr[index][22])
//         $("#MarginFromPart").val(boardarr[index][23])    

//         $('#WeightFromPart').val(boardarr[index][24]);

//         $('#PriceFromPart').val(boardarr[index][25]);
//         $('#WeightFromPart2').val(boardarr[index][26]);
//         $('#MaterialCostFromPart').val(boardarr[index][27])

//         $('#BoldMaterialCostFromPart').val(boardarr[index][28])
//     }else{
//         console.log('ISII INI MODAL FIELD INPUTNYA', index);
//         $('#BoardMaterialId').val(  '' )
//         $('#BoardMaterialName').val(  '' )

//         $("#VerticalScaleMaterial").val(  '' )
//         $("#HorizontalScaleMaterial").val(  '' )
//         $("#ThicknessMaterial").val(  '' )

//         $("#MaterialSpesificGravity").val(  '' )
//         $("#MaterialPrice").val(  '' )

//         // === FROM NUMBER OF PART =====
//         $("#VerticalScaleFromNumber").val(  '' )
//         $("#HorizontalScaleFromNumber").val(  '' )

//         $("#ExposedFromNumber").val(  ''  )
//         $("#MarginFromNumber").val(  ''  )

//         $('#NumVerFromNumber').val(  ''  );
//         $('#NumHorFromNumber').val(  ''  );
//         $('#QtyPerSheetFromNumber').val(  ''  );

//         $('#WeightFromNumber').val(  ''  );
//         $('#QtyFromNumber').val(  ''  );
//         $('#WeightPerQtyFromNumber').val(  ''  );

//         $('#PriceFromNumber').val(  ''  )
//         $('#WeightFromNumber2').val(  ''  );
//         $('#MaterialCostFromNumber').val(  ''  );
        
//         $('#BoldMaterialCostFromNumber').val(  ''  );

//         // === END FROM NUMBER OF PART =====

//         // ==== FROM PART OF PART =====
//         $("#ExposedFromPart").val( '' )
//         $("#MarginFromPart").val( '' )    

//         $('#WeightFromPart').val( '' );

//         $('#PriceFromPart').val( '' );
//         $('#WeightFromPart2').val( '' );
//         $('#MaterialCostFromPart').val( '' )

//         $('#BoldMaterialCostFromPart').val( '' )
//     }

//     console.log(boardarr);

// })