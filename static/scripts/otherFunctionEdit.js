function addOtherToTableFromDB(){     
        const obj = getQuotationOtherFromDB();
        // console.log(obj);

        obj.forEach((element, index) => {
            // alter table to add others 
            var table = document.getElementById("othersTable").getElementsByTagName('tbody')[0];

            var row = table.insertRow(-1);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);
            var cell7 = row.insertCell(6);

            cell1.style.width = "15%";

            cell1.innerHTML = `<th scope="row">${index+1}</th>`;
            cell2.innerHTML = `<td>${element.Name}</td>`;
            cell3.innerHTML = `<td><input type="input" name="otherprice" id="otherPrice-${index+1}" onchange="calculateOtherPercentage(${index+1}, this.value)" class="inputMd" value=${element.OTHER_PRICE}></td>`;
            cell4.innerHTML = `<td><input type="input" name="otherpercentage" class="inputPercentage inputMd" id="otherPercentage-${index+1}" value="${element.OTHER_PERCENTAGE}"></td>`;
            cell5.innerHTML = `<td><input type="checkbox" name="otherisperunit-${index+1}" id="otherCheckBox-${index+1}" name="otherCheckBox-${index+1}" onchange="calculateCostExcludeOperation()" value="${element.OTHER_IS_PER_UNIT}"` + (element.OTHER_IS_PER_UNIT == 1 ? "checked" : "") +`></td>`;
            cell6.innerHTML = `<td><button type="button" onclick="deleteOther(${index+1})" class="trash"><i id="trash-icon"></i></button></td>`;
            cell7.innerHTML = `<td><input type="hidden" name='othersId' value='${element.OtherId}'></td>`;
            
            callFeatherIcon();
            updateOtherLength(index+1);
            $('#otherName').val('');
        });
}

$(function(){
    addOtherToTableFromDB()
})

function addOther() {
    // get others name from search input 
    var otherName = document.getElementById('otherName').value;

    // get others database from py file 
    const obj = getOtherFromDB();
    var selectedOthers = obj.find(element => element.Name == otherName);

    if(selectedOthers == undefined){
        return false;
    }
    
    // check for duplicate others
    if(Object.entries(othersList).length != 0){
        var checkName = othersList.find(element => element.Name == otherName);
        if (checkName == undefined){
            othersList.push(selectedOthers);
        } else {
            if (checkName.OtherId == selectedOthers.OtherId){
                return false;
            }
            othersList.push(selectedOthers);
        }
    } else {
        othersList.push(selectedOthers);
    }
    
    // alter table to add others 
    var table = document.getElementById("othersTable").getElementsByTagName('tbody')[0];
    othersIndex++;

    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);
    var cell7 = row.insertCell(6);

    cell1.style.width = "15%";

    cell1.innerHTML = `<th scope="row">${othersIndex}</th>`;
    cell2.innerHTML = `<td>${selectedOthers.Name}</td>`;
    cell3.innerHTML = `<td><input type="input" name="otherprice" id="otherPrice-${othersIndex}" onchange="calculateOtherPercentage(${othersIndex}, this.value)" class="inputMd"></td>`;
    cell4.innerHTML = `<td><input type="input" name="otherpercentage" class="inputPercentage inputMd" id="otherPercentage-${othersIndex}"></td>`;
    cell5.innerHTML = `<td><input type="checkbox" name="otherisperunit-${othersIndex}" id="otherCheckBox-${othersIndex}" name="otherCheckBox-${othersIndex}" onchange="calculateCostExcludeOperation()"></td>`;
    cell6.innerHTML = `<td><button type="button" onclick="deleteOther(${othersIndex})" class="trash"><i id="trash-icon"></i></button></td>`;
    cell7.innerHTML = `<td><input type="hidden" name='othersId' value='${selectedOthers.OtherId}'></td>`;
    
    callFeatherIcon();
    updateOtherLength(othersIndex);
    $('#otherName').val('');
    
    return false;
}

function deleteOther(rowindex){
    var table = document.getElementById("othersTable").getElementsByTagName('tbody')[0];
    table.deleteRow(rowindex-1);

    // remove item from array and fixing the index 
    othersList.splice(rowindex-1, 1);
    var othersTableLength = $('table#othersTable > tbody tr').length;
    // othersIndex-=1;
    for(var i=0 ; i< othersTableLength ; i++){
        table.rows[i].cells[0].innerHTML = `<th scope="row">${i+1}</th>`;

        var selectedOthersName = $('table#othersTable tbody tr').eq(i).children().eq(1).children().val()
        var selectedOthersValue = $('table#othersTable tbody tr').eq(i).children().eq(2).children().val()
        var selectedOthersPercentage = $('table#othersTable tbody tr').eq(i).children().eq(3).children().val()
        var selectedOthersCheckbox = $('table#othersTable tbody tr').eq(i).children().eq(4).children()[0].checked == true ? 'checked' : ''
        // console.log("SELECTED = ", selectedOthersCheckbox)

        table.rows[i].cells[2].innerHTML = `<td><input type="input" id="otherPrice-${i + 1}" onchange="calculateOtherPercentage(${i + 1}, this.value)" class="inputMd" value=${selectedOthersValue} ></td>`;
        table.rows[i].cells[3].innerHTML = `<td><input type="input" class="inputPercentage" id="otherPercentage-${i + 1}" value="${selectedOthersPercentage}"></td>`;
        table.rows[i].cells[4].innerHTML = `<td><input type="checkbox" id="otherCheckBox-${i+1}" name="otherCheckBox-${i+1}" onchange="calculateCostExcludeOperation()" ${selectedOthersCheckbox}></td>`;
        table.rows[i].cells[5].innerHTML = `<td><button type="button" onclick="deleteOther(${i+1})" class="trash"><i id="trash-icon"></i></button></td>`;
        callFeatherIcon();
    }

    updateOtherLength(othersIndex);
    calculateTotalBudget();
}

function updateOtherLength(index){
    $('#othersLength').val(index);
}

function calculateOtherPercentage(index, val){
    var data = getData();
    var percent = parseFloat(val)/data.budgetPerUnit*100;
    $('#otherPercentage-'+index).val(percent);

    calculateCostExcludeOperation();
    getTotalOtherCost();
    calculateMaterialOutsourceOther();
}
