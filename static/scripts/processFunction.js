function updateProcessLength(index) {
  $("#processLength").val(index);
}

function deleteProcess(rowindex) {
//   console.log(index);
  var table = document
    .getElementById("processTable")
    .getElementsByTagName("tbody")[0];
  table.deleteRow(rowindex - 1);

  // remove item from array and fixing the index
  processList.splice(rowindex - 1, 1);
  index -= 1;
  for (var i = 0; i < index; i++) {
	  
	  
	  var selectedProcessId = $('table#processTable tbody tr').eq(i).children().eq(1).children().val()
	  var selectedProcessName = $('table#processTable tbody tr').eq(i).children().eq(2).text()
	  var selectedProcessCost = $('table#processTable tbody tr').eq(i).children().eq(3).html()
	  var selectedOpeSum = $('table#processTable tbody tr').eq(i).children().eq(4).children().val()
	  var selectedPerOpeBudgetRatio = $('table#processTable tbody tr').eq(i).children().eq(5).children().val()
	  var selectedPerBudgetRatio = $('table#processTable tbody tr').eq(i).children().eq(6).children().val()
	  var selectedSetTime = $('table#processTable tbody tr').eq(i).children().eq(7).children().val()
	  var selectedOpeTime = $('table#processTable tbody tr').eq(i).children().eq(8).children().val()
	  var selectedTotalTime = $('table#processTable tbody tr').eq(i).children().eq(9).children().val()
	  var selectedQtyPerMin = $('table#processTable tbody tr').eq(i).children().eq(10).children().val()
	  // console.log("SELECTED PROCESS = ", selectedProcessCost);
	  // cell4.innerHTML = `<td>${selectedProcess.SettingCost}/${selectedProcess.ProcessCost}</td>`;
	  
	  
	table.rows[i].cells[0].innerHTML = `<th scope="row">${i + 1}</th>`;
    table.rows[i].cells[1].innerHTML = `<td><input type="text" name='ProcessId' value='${selectedProcessId}' style="background: transparent; border: none; width: 100%;"></td>`; 
    table.rows[i].cells[2].innerHTML = `<td>${selectedProcessName}</td>`;
    table.rows[i].cells[3].innerHTML = `<td>${selectedProcessCost}</td>`;
    table.rows[i].cells[4].innerHTML = `<td><input type="text" class="operationInputMd" onfocus="savePrevValue(${i + 1})" onchange="calculateByOpeSum(${i + 1})" name='opeSum-${i + 1}' id='opeSum-${i + 1}' value=${selectedOpeSum}></td>`;
    table.rows[i].cells[5].innerHTML = `<td><input type="text" class="inputS" name='operationPerOperationBudgetRatio-${i + 1}' onchange="calculateByOperationPerOperationBudgetRatio(${i + 1})" id='operationPerOperationBudgetRatio-${i + 1}' value=${selectedPerOpeBudgetRatio}> %</td>`;
    table.rows[i].cells[6].innerHTML = `<td><input type="text" class="inputS" name='operationPerBudgetRatio-${i + 1}' onchange="calculateByOperationPerBudgetRatio(${i + 1})" id='operationPerBudgetRatio-${i + 1}' value=${selectedPerBudgetRatio}> %</td>`;
    table.rows[i].cells[7].innerHTML = `<td><input type="text" onchange="calculateBySetTime(${i + 1})" class="operationInputMd" name='setTime-${i + 1}' id='setTime-${i + 1}' value=${selectedSetTime}></td>`;
    table.rows[i].cells[8].innerHTML = `<td><input type="text" onchange="calculateByOpeTime(${i + 1})" class="operationInputMd" name='opeTime-${i + 1}' id='opeTime-${i + 1}' value=${selectedOpeTime}></td>`;
    table.rows[i].cells[9].innerHTML = `<td><input type="text" class="operationInputMd" onchange="calculateByTotalOpeTime(${i + 1})" name='totalOpeTime-${i + 1}' id='totalOpeTime-${i + 1}' value=${selectedTotalTime}></td>`;
    table.rows[i].cells[10].innerHTML = `<td><input type="text" class="inputS" onchange="calculateByQuantityPerMin(${i + 1})" name='quantityPerMinute-${i + 1}' id='quantityPerMinute-${i + 1}' value=${selectedQtyPerMin}></td>`;
    table.rows[i].cells[11].innerHTML = `<td><button type="button" onclick="deleteProcess(${i + 1})" class="trash"><i id="trash-icon"></i></button></td>`;


    callFeatherIcon();
  }

  updateProcessLength(index);
  totalOperations();
  
}

function callFeatherIcon() {
  const trashicon = $("#trash-icon");
  trashicon.replaceWith(feather.icons["trash-2"].toSvg());
}

function getProcessData(index) {
  var data = {
    opeSum: isNaN(parseInt(document.getElementById(`opeSum-${index}`).value))
      ? 0
      : parseInt(document.getElementById(`opeSum-${index}`).value),
    operationPerOperationBudgetRatio: isNaN(
      parseFloat(
        document.getElementById(`operationPerOperationBudgetRatio-${index}`)
          .value
      )
    )
      ? 0
      : parseFloat(
          document.getElementById(`operationPerOperationBudgetRatio-${index}`)
            .value
        ),
    operationPerBudgetRatio: isNaN(
      parseFloat(
        document.getElementById(`operationPerBudgetRatio-${index}`).value
      )
    )
      ? 0
      : parseFloat(
          document.getElementById(`operationPerBudgetRatio-${index}`).value
        ),
    setTime:
      document.getElementById(`setTime-${index}`).value == ""
        ? "00:00:00"
        : document.getElementById(`setTime-${index}`).value,
    opeTime:
      document.getElementById(`opeTime-${index}`).value == ""
        ? "00:00:00"
        : document.getElementById(`opeTime-${index}`).value,
    totalOpeTime: document.getElementById(`totalOpeTime-${index}`).value == ""
      ? "00:00:00"
      : document.getElementById(`totalOpeTime-${index}`).value,
    quantityPerMinute: isNaN(
      parseFloat(document.getElementById(`quantityPerMinute-${index}`).value)
    )
      ? 0
      : parseFloat(document.getElementById(`quantityPerMinute-${index}`).value),
  };

  return data;
}

function addProcess() {
	// get process name from search input 
	var processName = document.getElementById('processName').value;

	// get process database from py file 
	const obj = getProcessFromDB();
	var selectedProcess = obj.find(element => element.Name == processName);
		
	if(selectedProcess == undefined){
		return false;
	}
	
	// check for duplicate process
	if(Object.entries(processList).length != 0){
		var checkName = processList.find(element => element.Name == processName);
		if (checkName == undefined){
			processList.push(selectedProcess);
		} else {
			if (checkName.ProcessId == selectedProcess.ProcessId){
				return false;
			}
			processList.push(selectedProcess);
		}
		
	} else {
		processList.push(selectedProcess);
	}
  
	// alter table to add process 	
	var table = document.getElementById("processTable").getElementsByTagName('tbody')[0];
	index++;
	console.log(selectedProcess)
 
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
	cell2.innerHTML = `<td><input type="text" name='ProcessId' value='${selectedProcess.ProcessId}' style="background: transparent; border: none; width: 100%;"></td>`; 
	cell3.innerHTML = `<td>${selectedProcess.Name}</td>`;
	cell4.innerHTML = `<td>${selectedProcess.SettingCost}/${selectedProcess.ProcessCost}</td>`;
	cell5.innerHTML = `<td><input type="text" class="operationInputMd" onfocus="savePrevValue(${index})" onchange="calculateByOpeSum(${index})" name='opeSum' id='opeSum-${index}' value='0'></td>`;
	cell6.innerHTML = `<td><input type="text" class="inputS" name='operationPerOperationBudgetRatio' onchange="calculateByOperationPerOperationBudgetRatio(${index})" id='operationPerOperationBudgetRatio-${index}'> %</td>`;
	cell7.innerHTML = `<td><input type="text" class="inputS" name='operationPerBudgetRatio' onchange="calculateByOperationPerBudgetRatio(${index})" id='operationPerBudgetRatio-${index}'> %</td>`;
	cell8.innerHTML = `<td><input type="text" value="00:00:00" onchange="calculateBySetTime(${index})" class="operationInputMd" name='setTime' id='setTime-${index}'></td>`;
	cell9.innerHTML = `<td><input type="text" value="00:00:00" onchange="calculateByOpeTime(${index})" class="operationInputMd" name='opeTime' id='opeTime-${index}'></td>`;
	cell10.innerHTML = `<td><input type="text" value="00:00:00" class="operationInputMd" onchange="calculateByTotalOpeTime(${index})" name='totalOpeTime' id='totalOpeTime-${index}'></td>`;
	cell11.innerHTML = `<td><input type="text" class="inputS" onchange="calculateByQuantityPerMin(${index})" name='quantityPerMinute' id='quantityPerMinute-${index}'></td>`;
	cell12.innerHTML = `<td><button type="button" onclick="deleteProcess(${index})" class="trash"><i id="trash-icon"></i></button></td>`;
	cell13.innerHTML = `<td><input type="hidden" name='processId-${index}' value='${index}'></td>`;

	callFeatherIcon();
	updateProcessLength(index);
	$('#processName').val('');
	return false;
}

function setProcessData( index, opeSum, operationPerOperationBudgetRatio, operationPerBudgetRatio, setTime, opeTime, totalOpeTime, quantityPerMinute) {
	$(`#opeSum-${index}`).val(opeSum);
	$(`#operationPerOperationBudgetRatio-${index}`).val(
		operationPerOperationBudgetRatio
	);
	$(`#operationPerBudgetRatio-${index}`).val(operationPerBudgetRatio);
	$(`#setTime-${index}`).val(setTime);
	$(`#opeTime-${index}`).val(opeTime);
	$(`#totalOpeTime-${index}`).val(totalOpeTime);
	$(`#quantityPerMinute-${index}`).val(quantityPerMinute);
}

function calculateOperationPerOperationBudgetRatio(opeSum, operationBudget) {
	var result = (opeSum / operationBudget) * 100;
	var resultFixed = result.toFixed(2);
	// console.log(opeSum, operationBudget, getFuncName());
	return resultFixed;
}

function calculateOpePerBudgetRatio(opeSum, budgetPerUnit) {
	var result = (opeSum / budgetPerUnit) * 100;
	var resultFixed = result.toFixed(2);
	return resultFixed;
}

function calculateOpeTime(opeSum, procCost) {
	var result = (opeSum / parseFloat(procCost)) * 60;
	var resultFixed = convertSecondsToDateTime(result);
	return resultFixed;
}

function convertDateTimeToSeconds(date){
	var t = date.split(":")
	var sec = t[0] * 60 * 60 + t[1] * 60 + parseInt(t[2])
	//   console.log(date, "||",  sec);
	return sec;
}

function convertSecondsToDateTime(sec){
	var hour = Math.floor( sec / 3600).toString()
	hour < 10 ? hour = "0" + hour : hour = hour;

	var rest = sec - (hour*3600)
	var min = Math.floor(rest/60)
	min < 10 ? min = "0" + min : min = min;
	
	rest = rest - (min * 60)
	var sec = rest
	sec < 10 ? sec = "0" + sec : sec = sec;

  
	var res = `${hour}:${min}:${sec}`;
	return res;
}

function calculateTotalOpeTime(opeTime, quantity) {
	opeTime = convertDateTimeToSeconds(opeTime);
	var result = opeTime * quantity;
	var resultFixed = convertSecondsToDateTime(result)

	return resultFixed;
}

function calculateQuantityPerMinute(opeTime) {
	opeTime = opeTime.split(":");
	opeTime = +opeTime[0] * 60 * 60 + +opeTime[1] * 60 + +opeTime[2]; //convert date time to second
	if(opeTime == 0){
		return 0
	}
	var result = 60 / opeTime;
	return result.toFixed(5);
}

function calculateBySetTime(index) {
	var processData = getProcessData(index);
	var data = getData();
	var process = processList[index - 1];



	if (processData.opeSum == "" && processData.opeSum == 0) {
		// console.log('calculatebysettime first condition');
		var setTimeSec = convertDateTimeToSeconds(processData.setTime)
		var opeSum = (setTimeSec * process.SettingCost) / (60 * data.quantity);
		$(`#opeSum-${index}`).val(opeSum);
		var operationPerOperationBudgetRatio =
			calculateOperationPerOperationBudgetRatio(opeSum, data.operationBudget);
		var operationPerBudgetRatio = calculateOpePerBudgetRatio(opeSum, data.budgetPerUnit);
		var opeTime = "00:00:00";
		var totalOpeTime = calculateTotalOpeTime(opeTime, data.quantity);
		var quantityPerMinute = calculateQuantityPerMinute(opeTime);

		setProcessData(
			index,
			opeSum,
			operationPerOperationBudgetRatio,
			operationPerBudgetRatio,
			processData.setTime,
			opeTime,
			totalOpeTime,
			quantityPerMinute
		);
	} else if (processData.opeSum != 0) {
		var opeSum = 0;

		var setTimeSec = convertDateTimeToSeconds(processData.setTime)
		opeSum += (setTimeSec * process.SettingCost) / (60 * data.quantity);

		var opeTimeSec = convertDateTimeToSeconds(processData.opeTime)
		opeSum += ( opeTimeSec * process.ProcessCost) / 60;
		$(`#opeSum-${index}`).val(opeSum);

		var operationPerOperationBudgetRatio = calculateOperationPerOperationBudgetRatio( opeSum, data.operationBudget );
		var operationPerBudgetRatio = calculateOpePerBudgetRatio(
			opeSum,
			data.budgetPerUnit
		);
		var opeTime = processData.opeTime
		var totalOpeTime = calculateTotalOpeTime(opeTime, data.quantity);
		var quantityPerMinute = calculateQuantityPerMinute(opeTime);

		setProcessData(
			index,
			opeSum,
			operationPerOperationBudgetRatio,
			operationPerBudgetRatio,
			processData.setTime,
			opeTime,
			totalOpeTime,
			quantityPerMinute
		);

	}

	totalOperations();
}

function savePrevValue(i) {
//   console.log("Saving value " + $("#opeSum-1").val());
	$("#opeSum-"+i).data("val", $("#opeSum-"+i).val());
}

function getTotalOpeSumFromSetTimeAndOpeTime(index) {
	var processData = getProcessData(index);
	var data = getData();
	var process = processList[index - 1];

	var opeSum = 0;
	processData.setTime = convertDateTimeToSeconds(processData.setTime)
	opeSum += (processData.setTime * process.SettingCost) / 60;

	processData.opeTime = convertDateTimeToSeconds(processData.opeTime)
	opeSum += (processData.opeTime * process.ProcessCost) / 60;

	return opeSum;
}

function calculateByOpeSum(index) {
	var processData = getProcessData(index);
	var data = getData();
	var process = processList[index - 1];

	var prev = $("#opeSum-" + index).data("val");
	var curr = $("#opeSum-" + index).val();
	//   console.log( 'prev = ', $('#opeSum-1').data('val') );

	if (processData.setTime != "" && processData.setTime != "00:00:00") {
		// console.log("ENTER HERE 1");
		if (curr > prev) {
			// console.log("atas run 1.1");
			var operationPerOperationBudgetRatio = calculateOperationPerOperationBudgetRatio(curr, data.operationBudget);
			var operationPerBudgetRatio = calculateOpePerBudgetRatio( processData.opeSum, data.budgetPerUnit );
			var opeTime = calculateOpeTime( processData.opeSum - prev, process.ProcessCost );
			var totalOpeTime = calculateTotalOpeTime(opeTime, data.quantity);
			var quantityPerMinute = calculateQuantityPerMinute(opeTime);
		//   console.log("run", prev - processData.opeSum);
			// console.log("run 1.1");
		} else if (curr <= prev) {
			// console.log("atas run 1.2");

			var opeSum =
			processData.opeSum - (processData.setTime * process.setCost) / 60;
			var operationPerOperationBudgetRatio = calculateOperationPerOperationBudgetRatio(curr, data.operationBudget);
			var operationPerBudgetRatio = calculateOpePerBudgetRatio(processData.opeSum, data.budgetPerUnit);

			var f = getTotalOpeSumFromSetTimeAndOpeTime(index);
			//   console.log("rest money = ", f);
			if (curr - f > 0) {
				var opeTime = calculateOpeTime(curr - f, process.ProcessCost);
				var totalOpeTime = calculateTotalOpeTime(opeTime, data.quantity);
				var quantityPerMinute = calculateQuantityPerMinute(opeTime);
			} else {
				var secSetTime = (curr * 60) / process.SettingCost;
				
				var setTimeNew = convertSecondsToDateTime(secSetTime);
				// console.log(secSetTime, hours, mins, sec);
				var opeTime = "00:00:00";
				var totalOpeTime = calculateTotalOpeTime("00:00:00", data.quantity);
				var quantityPerMinute = 0;

				setProcessData(
					index,
					processData.opeSum,
					operationPerOperationBudgetRatio,
					operationPerBudgetRatio,
					setTimeNew,
					opeTime,
					totalOpeTime,
					quantityPerMinute
				);
				totalOperations();
				restOperations();
				return;
			}
				
			// console.log("run 1.2");
		} else if (processData.opeTime == "" || processData.opeTime == "00:00:00") {
			// console.log("atas run 1.3");
			var operationPerOperationBudgetRatio =
			calculateOperationPerOperationBudgetRatio( curr, data.operationBudget );
			var operationPerBudgetRatio = calculateOpePerBudgetRatio( processData.opeSum, data.budgetPerUnit );
			var opeTime = "00:00:00";
			var totalOpeTime = "00:00:00";
			var quantityPerMinute = 0;
		  	// console.log("run 1.3");
		} else {
			// console.log("atas run 1.4");
			var opeSum =
			processData.opeSum - (processData.setTime * process.setCost) / 60;
			var operationPerOperationBudgetRatio = calculateOperationPerOperationBudgetRatio( curr, data.operationBudget );
			var operationPerBudgetRatio = calculateOpePerBudgetRatio( processData.opeSum, data.budgetPerUnit );
			var opeTime = calculateOpeTime(opeSum, process.ProcessCost);
			var totalOpeTime = calculateTotalOpeTime(opeTime, data.quantity);
			var quantityPerMinute = calculateQuantityPerMinute(opeTime);
			// console.log("run 1.4");
			
			// ope sum - calculate ope sum by settime
			// lalu hasilnya baru dipake buat ngitung opetime
			// ambil data opesum sekarang yang sudah diubah oleh settime += calculate opesum by ope time
		}
			// console.log('OnChange1 :: oldValue: ' + document.getElementById('opeSum-1').oldValue + ', newValue: ' + index.newValue);
	} else {
		// console.log("ENTER HERE 2");
		var operationPerOperationBudgetRatio = calculateOperationPerOperationBudgetRatio(curr,data.operationBudget);
		var operationPerBudgetRatio = calculateOpePerBudgetRatio(
			processData.opeSum,
			data.budgetPerUnit
		);
		var opeTime = calculateOpeTime(processData.opeSum, process.ProcessCost);
		var totalOpeTime = calculateTotalOpeTime(opeTime, data.quantity);
		var quantityPerMinute = calculateQuantityPerMinute(opeTime);
		// console.log("RUN 2.1");
	}

	setProcessData(
		index,
		processData.opeSum,
		operationPerOperationBudgetRatio,
		operationPerBudgetRatio,
		processData.setTime,
		opeTime,
		totalOpeTime,
		quantityPerMinute
	);
	totalOperations();
	restOperations();
	//  console.log("IN SECOND = ", convertDateTimeToSeconds("12:32:11"));
}

$("#opeSum-1").change(function () {
  var prev = $(this).data("val");
  var current = $(this).val();

});

function calculateByOperationPerOperationBudgetRatio(index) {
  var processData = getProcessData(index);
  var data = getData();

  var opeSum = Math.round(
    (processData.operationPerOperationBudgetRatio * data.operationBudget) / 100
  );
  $(`#opeSum-${index}`).val(opeSum);

  calculateByOpeSum(index);
}

function calculateByOperationPerBudgetRatio(index) {
  var processData = getProcessData(index);
  var data = getData();

  var opeSum = Math.round(
    (processData.operationPerBudgetRatio * data.budgetPerUnit) / 100
  );
  $(`#opeSum-${index}`).val(opeSum);

  calculateByOpeSum(index);
}

function calculateByOpeTime(index) {
  var processData = getProcessData(index);
  var data = getData();

  // var opeSum = data.opeTime
  // var opeSum = Math.round(processData.operationPerBudgetRatio * data.budgetPerUnit / 100);
  // $(`#opeSum-${index}`).val(opeSum);
  var opeSum = getTotalOpeSumFromSetTimeAndOpeTime(index);
//   console.log(opeSum);
  var operationPerOperationBudgetRatio =
    calculateOperationPerOperationBudgetRatio(opeSum, data.operationBudget);
  var operationPerBudgetRatio = calculateOpePerBudgetRatio(
    opeSum,
    data.budgetPerUnit
  );
  var opeTime = processData.opeTime;
  var totalOpeTime = calculateTotalOpeTime(opeTime, data.quantity);
  var quantityPerMinute = calculateQuantityPerMinute(opeTime);

  setProcessData(
    index,
    opeSum,
    operationPerOperationBudgetRatio,
    operationPerBudgetRatio,
    processData.setTime,
    opeTime,
    totalOpeTime,
    quantityPerMinute
  );
  totalOperations();
  // calculateByOpeSum(index);
  
}

function calculateByTotalOpeTime(index){
  var processData = getProcessData(index);
  var data = getData();
  
  var totalopetime = processData.totalOpeTime;

  
  if (totalopetime != '' && totalopetime != 0){
    var totalopetimeseconds = convertDateTimeToSeconds(totalopetime)
  } else {
    var totalopetimeseconds = 0;
  }

  totalopetime = convertSecondsToDateTime(totalopetimeseconds)

  var opetime = totalopetime
  // var quotequantity = document.getElementById('QuoteQuantity').value;
  if (data.quantity != '' && data.quantity != 0){
      var opetimeseconds = totalopetimeseconds/data.quantity;
      opetime = convertSecondsToDateTime(opetimeseconds)
  } else {
      var opetimeseconds = totalopetimeseconds;
  }

  $('#opeTime-' + index).val(opetime)
  calculateByOpeTime(index)

//   console.log("OPETIMESECOND = ", opetimeseconds);
//   console.log("totaloptime = ", totalopetime);


}

function calculateByQuantityPerMin(index){
  var processData = getProcessData(index);
  var data = getData();

  
  var opeTimeSec = 60/processData.quantityPerMinute;
  var opeTime = convertSecondsToDateTime(opeTimeSec);
  var totalOpeTime = convertSecondsToDateTime(opeTimeSec * data.quantity);
  $(`#opeTime-${index}`).val(opeTime);
  var opeSum = getTotalOpeSumFromSetTimeAndOpeTime(index);
  var operationPerOperationBudgetRatio = calculateOperationPerOperationBudgetRatio(opeSum, data.operationBudget);
  var operationPerBudgetRatio = calculateOpePerBudgetRatio(
    opeSum,
    data.budgetPerUnit
    );
    
    setProcessData(
      index,
      opeSum,
      operationPerOperationBudgetRatio,
      operationPerBudgetRatio,
      processData.setTime,
      opeTime,
      totalOpeTime,
      processData.quantityPerMinute
    );
      
    // console.log('CALCULATE BY QUAN/min', 'OPESUM = ', opeSum);
}

function totalOperations(){
	// console.log(getFuncName(), "function entered");
	var totalOpeSum = 0
	var totalOpePerOpeBudgetRatio = 0
	var totalOpePerBudgetRatio = 0
	var totalSetTime = 0
	var totalOpeTime  = 0
	var totalTotalOpeTime = 0
	var processList = $('#processTable tr');
	var processLength = processList.length - 2;


	for (let index = 1; index < processLength; index++) {
		var elel = $(processList[index]).children() 
		// console.log("KEKKETKLFADSHNUF = ", elel[4] );
		// console.log( $(elel[5]).children().val().split('%') );

		totalOpeSum += parseInt( $(elel[4]).children().val() )
		// console.log("TOTALOPESUM EACH = ", totalOpeSum, getFuncName());
		totalOpePerOpeBudgetRatio += parseFloat(  $(elel[5]).children().val().split('%')[0] )
		totalOpePerBudgetRatio += parseFloat(  $(elel[6]).children().val().split('%')[0] )
		totalSetTime += parseInt(convertDateTimeToSeconds($(elel[7]).children().val()))
		
		totalOpeTime += parseInt(convertDateTimeToSeconds($(elel[8]).children().val()))

		// totalSetTime = new Date(totalSetTime * 1000).toISOString().slice(11, 19);

		totalTotalOpeTime += parseInt(convertDateTimeToSeconds($(elel[9]).children().val()))
	}


	$('#operationCost').val(zeroSeparator(totalOpeSum));
	var costExcludeOperation = $('#materialOutsourceOtherCost').val().replaceAll(',', '')
	totalCost = parseFloat(totalOpeSum) + parseFloat(costExcludeOperation);
	$('#totalCost').val(zeroSeparator (totalCost));

	$('#totalOpeSum').text(totalOpeSum);
	$('#totalOpePerOpe').text(totalOpePerOpeBudgetRatio.toFixed(5) + ' %' )
	$('#totalOpePerBudget').text(totalOpePerBudgetRatio.toFixed(5) + ' %')
	$('#totalSetTime').text( convertSecondsToDateTime(totalSetTime) );
	$('#totalOpeTime').text( convertSecondsToDateTime(totalOpeTime) );
	$('#totalTotalOpeTime').text( convertSecondsToDateTime(totalTotalOpeTime) );

	$('#totalOperationCost').val(totalOpeSum)
	restOperations();
  
}

function restOperations(){  
  var totalBudget = $('#totalBudget').val().replaceAll(',', '')
  var costExcludeOperation = $('#materialOutsourceOtherCost').val().replaceAll(',', '')
  var costAvailable = parseFloat(totalBudget) - parseFloat(costExcludeOperation)
  $('#restOpeSum').text(costAvailable);

  var totalOpeSum = $('#totalOpeSum').text()
  costAvailable = costAvailable - totalOpeSum
  $('#restOpeSum').text( zeroSeparator(costAvailable));


  var totalOpePerOpe = $('#totalOpePerOpe').text();
  var restOpePerOpe = 100 - parseFloat(totalOpePerOpe);
  restOpePerOpe = restOpePerOpe.toFixed(2) + '%';
  $('#restOpePerOpe').text(restOpePerOpe )

  var totalOpePerBudget = $('#totalOpePerBudget').text();
  var restOpePerBudget = 100 - parseFloat(totalOpePerBudget);
  restOpePerBudget = restOpePerBudget.toFixed(2) + '%';
  $('#restOpePerBudget').text(restOpePerBudget )
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
