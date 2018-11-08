function c1v1() {
    var c1 = document.getElementsByName("c1")[0].value;
    var v1 = document.getElementsByName("v1")[0].value;
    var c2 = document.getElementsByName("c2")[0].value;
    var v2 = document.getElementsByName("v2")[0].value;

    if (c2 == "" && v2 == "") {
        printResult("Please enter three parameters.");
    }
    else if (c2 == "") {
        var c2 = c1 * v1 / v2;
        printResult(c1 + "*" + v1 + "/" + v2 +
                    "<br/>Concentration needed (C2): " + c2.toFixed(3) + " ppb");
    }
    else if (v2 == "") {
        var v2 = c1 * v1 / c2;
        printResult("<br/>Volume needed (V2): " + v2.toFixed(6) + " L");
    }
    else {printResult("Please enter three parameters");}

}


function printResult(result) {
    document.getElementById("result").innerHTML = result;
}

