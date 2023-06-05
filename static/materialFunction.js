function getMaterialData(materialIndex){
     
    var data = {
        'usedQuantity' : isNaN(parseInt(document.getElementById(`usedQuantity-${materialIndex}`).value)) ? 0 : parseInt(document.getElementById(`usedQuantity-${materialIndex}`).value),
        // 'materialNumber' : isNaN(parseInt(document.getElementById(`materialNumber-${materialIndex}`).value)) ? 0 : parseInt(document.getElementById(`materialNumber-${materialIndex}`).value),
        'materialCost' : isNaN(parseInt(document.getElementById(`materialCost-${materialIndex}`).value)) ? 0 : parseInt(document.getElementById(`materialCost-${materialIndex}`).value),
    }

    return data;
}

function setMaterialData(materialIndex, usedQuantity, materialNumber, materialCost){
    $(`#usedQuantity-${materialIndex}`).val(usedQuantity);
    // $(`#materialNumber-${materialIndex}`).val(materialNumber);
    $(`#materialCost-${materialIndex}`).val(materialCost);
}

var boardArr = []
var barArr = []

function addMaterial() {
    // get material name from search input 
    var materialName = document.getElementById('searchName').value;

    // get material database from py file 
    const obj = getMaterialFromDB();
    var selectedMaterial = obj.find(element => element.name == materialName);

    if(selectedMaterial == undefined){
        return false;
    }
    
    // check for duplicate material
    if( Object.entries(materialList).length != 0){
        var checkName = materialList.find(element => element.name == materialName);
        if (checkName != undefined && checkName.idPart == selectedMaterial.idPart){
            return false
        }
    } 
    materialList.push(selectedMaterial);

    
    
    // alter table to add process 
    var table = document.getElementById("materialTable").getElementsByTagName('tbody')[0];
    materialIndex++;

    var row = table.insertRow(materialIndex-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);
    var cell7 = row.insertCell(6);
    var cell8 = row.insertCell(7);
    var cell9 = row.insertCell(8);

    cell1.innerHTML = `<th scope="row">${materialIndex}</th>`;
    cell2.innerHTML = `<td><input type="input" class="inputt material-id" value="${selectedMaterial.idPart}"></td>`;
    cell3.innerHTML = `<td><input type="input" value="${selectedMaterial.name}"></td>`;
    cell4.innerHTML = `<td><input type="input" list="process" class="inputt1"></td>`;
    cell5.innerHTML = `<td>
                        <input type="input" class="inputt1 material-used-process" 
                        onchange="calculateByUsedQuantity(${materialIndex})" 
                        name="usedQuantity-${materialIndex}" 
                        id="usedQuantity-${materialIndex}">
                            <a data-bs-toggle="modal" data-bs-target="#exampleModal1" id="modal-${materialIndex}" data-bs-index="${selectedMaterial.idPart}" >
                                <img class="imgcalcu" src="/static/images/calculator.png">
                            </a>
                        </td>`;
    cell6.innerHTML = `<td> <p class="material-price"> ${selectedMaterial.price} </p> </td>`;
    cell7.innerHTML = `<td><input type="input" class="inputt1 material-cost-price" value=0 name="materialCost-${materialIndex}" id=materialCost-${materialIndex}></td>`;
    cell8.innerHTML = `<td><button type="button" onclick="deleteMaterial(${materialIndex});" class="trash"><i id="trash-icon"></i></button></td>`;
    cell9.innerHTML = `<td><input type="hidden" name='idMaterial-${materialIndex}' value='${selectedMaterial.idPart}'></td>`;
  
    callFeatherIcon();
    updateMaterialLength(index);
    $('#searchName').val('');

    // add empty array to boardArr array dan barArr array
    // with some default value from DB : material id, name, gravity, price 
    boardArr.push([
        selectedMaterial.idPart, selectedMaterial.idPart , selectedMaterial.name, '', '', '', selectedMaterial.spesificGravity , selectedMaterial.price, '', '', '', 
        '', '', '', '', '', '', '', selectedMaterial.price, '', '',
        '', '', '', '', selectedMaterial.price, '', '', ''  
    ])

    barArr.push([
        selectedMaterial.idPart, selectedMaterial.idPart, selectedMaterial.name, '', '', selectedMaterial.spesificGravity, selectedMaterial.price, '', '', '',
        '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '',
    ])

    console.log(boardArr);
    return false;
}

function updateMaterialLength(index){
    $('#materialLength').val(index);
}

function deleteMaterial(rowindex){
    // console.log(index);
    var table = document.getElementById("materialTable").getElementsByTagName('tbody')[0];
    table.deleteRow(rowindex-1);

    // remove item from array and fixing the index 
    materialList.splice(rowindex-1, 1);
    materialIndex-=1;
    for(var i=0 ; i<materialIndex ; i++){
        table.rows[i].cells[0].innerHTML = `<th scope="row">${i+1}</th>`;
        // untuk ambil material id nya 
   
        // var material_id = $(el).attr('onchange').split('(')[1].split(')')[0] 
        var selected_material_id = $('table#materialTable tbody tr').eq(i).children().eq(1).children().val()
        var used_qty = $('table#materialTable tbody tr').eq(i).children().eq(4).children().eq(0).val()  
        var selected_material_price = $('table#materialTable tbody tr').eq(i).children().eq(5).children().text()
        var selected_material_cost_price = $('table#materialTable tbody tr').eq(i).children().eq(6).children().val()
        console.log("DELETD SELECTED MATERIAL COST PRICE = ", used_qty );
        console.log("DELETD SELECTED MATERIAL PRICE = ", selected_material_price );
        
        table.rows[i].cells[4].innerHTML = `<td><input type="input" class="inputt1 material-used-process" onchange="calculateByUsedQuantity(${i+1})" name="usedQuantity-${i+1}" id="usedQuantity-${i+1}" value=${used_qty}><a data-bs-toggle="modal" data-bs-target="#exampleModal1" id="modal-${i+1}" data-bs-index="${ selected_material_id }" ><img class="imgcalcu" src="/static/images/calculator.png"></a></td>;`
        // table.rows[i].cells[5].innerHTML = `<td><input type="input" class="inputt1" onchange="calculateByNumber(${i+1})" name="materialNumber-${i+1}" id="materialNumber-${i+1}" value="0"></td>`;
        table.rows[i].cells[5].innerHTML = `<td> <p class="material-price"> ${ selected_material_price } </p> </td>`;
        table.rows[i].cells[6].innerHTML = `<td><input type="input" class="inputt1 material-cost-price" value=${selected_material_cost_price} name="materialCost-${i+1}" id=materialCost-${i+1} ></td>`;
        table.rows[i].cells[7].innerHTML = `<td><button type="button" onclick="deleteMaterial(${i+1})" class="trash"><i id="trash-icon"></i></button></td>`;
        callFeatherIcon();
    }

    updateMaterialLength(index);
    updateBoardArrayDelete(rowindex - 1);
    updateTotalMaterialCostOnModal();
}

function calculateMaterialCost(usedQuantity, price){
    var result = usedQuantity * price;
    return result;
}

// function calculateUsedQuantity(number){
//     var result = 1/number;
//     return result;
// }

function calculateByUsedQuantity(materialIndex){
    var data = getMaterialData(materialIndex);
    var material = materialList[materialIndex-1];
    
    
    var materialCost = calculateMaterialCost(data.usedQuantity, material.price);
    $(`#materialCost-${materialIndex}`).val(materialCost);
    console.log('MATERIAL COST = ', materialCost);
    updateTotalMaterialCostOnModal();
}

// function calculateByNumber(number){
//     var data = getMaterialData(number);
//     var material = materialList[materialIndex-1];

//     var usedQuantity = calculateUsedQuantity(data.materialNumber);
//     var materialCost = calculateMaterialCost(usedQuantity, material.Price);
    
//     setMaterialData(materialIndex, usedQuantity, data.materialNumber, materialCost);
// }

$('#reflect-cost-button').on('click', function(){
    var total = $('#total-material-cost').text()
    $('#materialCost').val(total)

    var materialCostPercentage = $('#materialCostPercentage').val()

    // console.log('OTAL MTAERIAL VSOT = ', total * materialCostPercentage / 100 );
    $('#totalMaterialCost').val(total * materialCostPercentage / 100)
})

