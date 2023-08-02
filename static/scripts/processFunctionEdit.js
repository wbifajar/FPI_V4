function addProcessToTableFromDB(){     
    const obj = getSelectedProcessFromDB();
    console.log(obj);

    obj.forEach((element, index) => {
        // alter table to add others 
        var table = document.getElementById("processTable").getElementsByTagName('tbody')[0];
        index++;
        console.log("QUOTATION PROCESSSSS = ", element)
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);
        var cell6 = row.insertCell(5);
        var cell7 = row.insertCell(6);
        var cell8 = row.insertCell(7);
        var cell9 = row.insertCell(8);
        var cell10 = row.insertCell(9);
        var cell11 = row.insertCell(10);
        var cell12 = row.insertCell(11);
        var cell13 = row.insertCell(12);
        
        cell2.style.width = "5%";
        
        cell1.innerHTML = `<th scope="row">${index}</th>`; 
        cell2.innerHTML = `<td><input type="text" name='ProcessId' value='${element.ProcessId}' style="background: transparent; border: none; width: 100%;"></td>`; 
        cell3.innerHTML = `<td>${element.Name}</td>`;
        cell4.innerHTML = `<td>${element.SettingCost}/${element.ProcessCost}</td>`;
        cell5.innerHTML = `<td><input type="text" class="operationInputMd" onfocus="savePrevValue()" onchange="calculateByOpeSum(${index})" name='opeSum' id='opeSum-${index}' value=${element.OPESUM}></td>`;
        cell6.innerHTML = `<td><input type="text" class="inputS" name='operationPerOperationBudgetRatio' onchange="calculateByOperationPerOperationBudgetRatio(${index})" id='operationPerOperationBudgetRatio-${index}' value=${element.OPE_PER_OPE_BUDGET_RATIO}> %</td>`;
        cell7.innerHTML = `<td><input type="text" class="inputS" name='operationPerBudgetRatio' onchange="calculateByOperationPerBudgetRatio(${index})" id='operationPerBudgetRatio-${index}' value=${element.OPE_PER_BUDGET_RATIO}> %</td>`;
        cell8.innerHTML = `<td><input type="text" onchange="calculateBySetTime(${index})" class="operationInputMd" name='setTime' id='setTime-${index}' value=${element.SETTIME}></td>`;
        cell9.innerHTML = `<td><input type="text" onchange="calculateByOpeTime(${index})" class="operationInputMd" name='opeTime' id='opeTime-${index}' value=${element.OPETIME}></td>`;
        cell10.innerHTML = `<td><input type="text" class="operationInputMd" onchange="calculateByTotalOpeTime(${index})" name='totalOpeTime' id='totalOpeTime-${index}' value=${element.TOTAL_OPETIME}></td>`;
        cell11.innerHTML = `<td><input type="text" class="inputS" onchange="calculateByQuantityPerMin(${index})" name='quantityPerMinute' id='quantityPerMinute-${index}' value=${element.QUANTITY_PER_MIN}></td>`;
        cell12.innerHTML = `<td><button type="button" onclick="deleteProcess(${index})" class="trash"><i id="trash-icon"></i></button></td>`;
        cell13.innerHTML = `<td><input type="hidden" name='processId-${index}' value='${element.ProcessId}'></td>`;
    
        callFeatherIcon();
        updateProcessLength(index);
        $('#processName').val('');
        return false;
    });
}

$(function(){
    addProcessToTableFromDB()
})