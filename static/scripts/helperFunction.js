function removeNonDigit(val){
    return val.replace(/[^0-9.-]+/g,"")
}

function replaceNanValue(val, new_val) {
    const test_val = parseFloat(val)
    return isNaN(test_val) ? new_val : test_val
}

function replaceInfinityValue(val, new_val){
    if(val == Infinity) return new_val
    return val
}

function getFuncName() {
    return getFuncName.caller.name
}