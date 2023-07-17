// buat others 
var othersIndex = 0;
const othersList = [];

// buat process 
var index = 0;
const processList = [];

// buat material 
var materialIndex = 0;
const materialList = [];

function removeNonDigit(val){
    return val.replace(/[^0-9.-]+/g,"")
}

function handleNanValue(val) {
    return isNaN(parseFloat(val)) ? 0 : parseFloat(val)
}

function getData() {
    var data = {
        'quantity': handleNanValue($('#quantity').val()),
        'budgetPerUnit': handleNanValue($('#budgetPerUnit').val()),
        'totalBudget': handleNanValue($('#totalBudget').val()),
        'managementCostPercentage': handleNanValue($('#managementCostPercentage').val()),
        'managementCost': handleNanValue( removeNonDigit($('#managementCost').val()) ),

        'materialCost': handleNanValue($('#materialCost').val()),
        'materialCostPercentage': handleNanValue($('#materialCostPercentage').val()),
        'totalMaterialCost': handleNanValue( removeNonDigit($('#totalMaterialCost').val()) ),

        'outsourceCost': handleNanValue($('#outsourceCost').val()),
        'outsourceCostPercentage': handleNanValue($('#outsourceCostPercentage').val()),
        'totalOutsourceCost': handleNanValue( removeNonDigit($('#totalOutsourceCost').val()) ),

        'operationBudget': handleNanValue( removeNonDigit($('#operationBudget').val()) ),
    }
    console.log(data);
    return data;
}

function zeroSeparator(val) {
    val = parseFloat(val).toLocaleString('en');
    return val;
}

function calculateBudgetAvailable() {
    var totalBudget = $('#totalBudget').val().replaceAll(',', '')
    var costExcludeOperation = $('#materialOutsourceOtherCost').val().replaceAll(',', '')
    // console.log( "costExcludeOperation = ", costExcludeOperation);
    var costAvailable = parseFloat(totalBudget) - parseFloat(costExcludeOperation)
    // console.log('total cost available before other cost = ', totalBudget );
    return costAvailable
}

function calculateTotalBudget() {
    var data = getData();
    var result = data.quantity * data.budgetPerUnit;
    $('#totalBudget').val(zeroSeparator(result));
    $('#budgetPerUnit2').val(zeroSeparator(data.budgetPerUnit));

    calculateManagementCost();

    for (var i = 0; i < othersIndex; i++) {
        otherPrice = document.getElementById('otherPrice-' + (i + 1)).value;
        calculateOtherPercentage(i + 1, otherPrice);
    }
    var costAvailable = calculateBudgetAvailable();

    $('#restOpeSum').text(zeroSeparator(costAvailable))
    recalculateBySetTime();
    calculateCalculationResult();
}

function calculateManagementCost() {
    var data = getData();
    var result = data.budgetPerUnit * data.managementCostPercentage / 100;
    $('#managementCost').val(zeroSeparator(result));
    $('#managamentCostPercentageNew').val(data.managementCostPercentage);

    calculateCostExcludeOperation();
}

function calculateCostExcludeOperation() {
    var data = getData();
    var result = data.managementCost + data.totalMaterialCost + data.totalOutsourceCost;

    for (var i = 0; i < othersIndex; i++) {
        var otherPrice = parseFloat(document.getElementById(`otherPrice-${i + 1}`).value);
        var otherCheckBox = document.getElementById(`otherCheckBox-${i + 1}`).checked;

        if (!isNaN(otherPrice)) {
            if (otherCheckBox == false) {
                result += otherPrice * data.quantity;
            } else {
                if (data.quantity != '' && data.quantity != 0) {
                    result += otherPrice / data.quantity;
                } else {
                    result += otherPrice * data.quantity;
                }
            }
            // result += otherPrice;
        }
    }

    $('#materialOutsourceOtherCost').val(zeroSeparator(result));

    var operationBudget = data.budgetPerUnit - result;
    $('#operationBudget').val(zeroSeparator(operationBudget));
    if (operationBudget < 0) {
        document.getElementById("operationBudget").style.color = "white";
        document.getElementById("operationBudget").style.backgroundColor = "red";
    } else {
        document.getElementById("operationBudget").style.color = "black";
        document.getElementById("operationBudget").style.backgroundColor = "transparent";
    }
}

function getTotalOtherCost() {
    var data = getData();
    var result = 0;
    var othersIndexLen = $('table#othersTable > tbody tr').length
    console.log("othersIndexLen = ", othersIndexLen);
    for (var i = 0; i < othersIndexLen; i++) {
        var otherPrice = parseFloat(document.getElementById(`otherPrice-${i + 1}`).value);
        var otherCheckBox = document.getElementById(`otherCheckBox-${i + 1}`).checked;

        if (!isNaN(otherPrice)) {
            if (otherCheckBox == false) {
                result += otherPrice * data.quantity;
            } else {
                if (data.quantity != '' && data.quantity != 0) {
                    result += otherPrice / data.quantity;
                } else {
                    result += otherPrice * data.quantity;
                }
            }
            // result += otherPrice;
        }

        console.log(result);
    }

    return result
}

function calculateTotalMaterialCost() {
    var data = getData();
    var result = data.materialCost * data.materialCostPercentage / 100;
    $('#totalMaterialCost').val(zeroSeparator(result));
    

    calculateCostExcludeOperation();
    calculateMaterialOutsourceOther();
}

function calculateTotalOursourceCost() {
    var data = getData();
    var result = data.outsourceCost * data.outsourceCostPercentage / 100;
    $('#totalOutsourceCost').val(zeroSeparator(result));

    calculateCostExcludeOperation();
    calculateMaterialOutsourceOther();
}

function calculateMaterialOutsourceOther(){
    var totalMaterialCost =  removeNonDigit($('#totalMaterialCost').val())
    var totalOutsourceCost = removeNonDigit($('#totalOutsourceCost').val())
    var totalOtherCost = getTotalOtherCost()

    var total = parseFloat(totalMaterialCost) + parseFloat(totalOutsourceCost) + parseFloat(totalOtherCost)
    $('#materialOutsourceOtherCost').val(total)
    calculateCalculationResult();
}

function calculateCalculationResult(){
    var totalOperationCost = $('#totalOperationCost').val();
    var totalMaterialOutsourceOther = $('#materialOutsourceOtherCost').val();
    var managementCostPercentage = $('#managementCostPercentage').val();
    var managementCostVal = parseFloat(managementCostPercentage)/100


    var calculationResult = (parseFloat(totalOperationCost) + parseFloat(totalMaterialOutsourceOther)) / (1 - managementCostVal)
    calculationResult = calculationResult.toFixed(0)
    $('#calculationResult').val(calculationResult)

    var managementCostAfter = parseFloat($('#calculationResult').val()) - parseFloat(totalOperationCost) - parseFloat(totalMaterialOutsourceOther)
    $('#managementCostNew').val(managementCostAfter)
    
}


function recalculateBySetTime(){
    var processTableLen = $('table#processTable > tbody tr').length
   
    for (var i = 0; i < processTableLen; i++) {
        calculateBySetTime(i+1);
    }
}