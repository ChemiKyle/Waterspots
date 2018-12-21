function c1v1() {
    var c1 = document.getElementsByName("c1")[0].value;
    var v1 = document.getElementsByName("v1")[0].value;
    var c2 = document.getElementsByName("c2")[0].value;
    var v2 = document.getElementsByName("v2")[0].value;

    if (c2 == "" && v2 == "") {printResult("Please enter three parameters.");}
    else if (c2 == "") {
        c2 = c1 * v1 / v2;
        printResult(`(${c1} ppb * ${v1} L) / ${v2} L = ${c2} ppb` +
                    "<br/>Concentration needed (C2): " + c2.toFixed(3) + " ppb");
    }
    else if (v2 == "") {
        v2 = c1 * v1 / c2;
        printResult(`(${c1} ppb * ${v1} L) / ${c2} ppb` +
                    "<br/>Volume needed (V2): " + v2.toFixed(6) + " L");
    }
    else {printResult("Please enter three parameters.");}

}

function gallonsLiters() {
    var gals = document.getElementsByName("gals")[0].value;
    var liters = document.getElementsByName("liters")[0].value;

    if (gals == "" && liters == "") {printResult("Please fill in a value for conversion");}
    else if (liters == "") {
        liters = gals * 3.785;
        printResult(`${gals} / 3.785 gal/L = ${liters} L`);
    } else if (gals == "") {
        gals = liters / 3.785;
        printResult(`${liters} L * 3.785 gal/L = ${gals} gal`);
    }
    else {printResult("Please fill in a value for conversion");}

}

function turbidityCalc() {
    var volume = document.getElementsByName("turb_volume")[0].value;
    var volume_units = document.getElementsByName("volume_units")[0].value;
    var dust_type = document.getElementsByName("dust_type")[0].value;
    var end_turbidity = document.getElementsByName("end_turbidity")[0].value;
    var turb_constant;

    if (volume_units == "Liters") {
        volume /= 3.785;
    }
    // TODO: change to dictionary
    if (dust_type == "fine") {
        turb_constant = 0.06 / 11;
    } else if (dust_type == "coarse") {
        turb_constant = 130 / 8500;
    }

    var grams_needed = volume * turb_constant * end_turbidity;
    printResult(`Grams needed: ${grams_needed}`);
}

function printResult(result) {
    document.getElementById("result").innerHTML = result;
}

function adjustMetricPrefix(num, unit) {
    // incomplete function to adjust metric prefix for nicer numbers
    var powAdjust = 0;
    function powerAdjust(num, powAdjust) {
        if (num == 0) {return 0;}

        if (num / 1000 > 1) {
            num /= 1000;
            powAdjust++;
            powerAdjust(num, powAdjust);
        }
        else if (num * 1000 < 1) {
            num *= 1000;
            powAdjust--;
            powerAdjust(num, powAdjust);
        }
        return powAdjust;
    }
    num *= 10**powAdjust;
    if (unit == "L") {
        // TODO: dictionary with key: power of 10; val: modifier
    }

}
