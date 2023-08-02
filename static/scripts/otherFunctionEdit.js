function addOtherToTableFromDB(){     
        const obj = getQuotationOtherFromDB();
        console.log(obj);

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