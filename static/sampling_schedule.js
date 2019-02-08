function setup_chart_area() {
    const margin = {top: 30, right: 20, bottom: 30, left: 50},
          width = window.innerWidth - margin.left - margin.right,
          height = window.innerHeight - margin.top - margin.bottom;

    var svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    return [margin, width, height, svg];
}

function draw_lineplot() {

    var [margin, width, height, svg] = setup_chart_area();

    var x = d3.scaleLinear()
        .domain([0, d3.max(df, function(d) {return (d.cum_mins_running); })])
        .range([0, width]);
    var y = d3.scaleLinear()
        .domain([0, d3.max(df, function(d) {return (d.vol_passed); })])
        .range([height, 0]);

    var xAxis = d3.axisBottom(x);
    var yAxis = d3.axisLeft(y);

    var valueline = d3.line()
        .x(function(d) { return x(d.cum_mins_running); })
        .y(function(d) { return y(d.vol_passed); });

    // draw axes
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(0, ${height})`)
        .call(xAxis);
    svg.append("g")
        .attr("class", "axis")
        .call(yAxis);

    // draw data
    svg.append("path")
        .data([df])
        .attr("class", "line")
        .attr("d", valueline);
}

function radial_clockplot() {
    var [margin, width, height, svg] = setup_chart_area();

    // TODO: split this by calendar day of df.dt
    var testDay1 = df.slice(0, 960); // TODO: extract time and date separately

    var r = d3.scaleLinear()
        .domain(d3.extent(testDay1, function(d) { return (d.vol_passed); }))
        .range([0, height / 2]);

    var theta = d3.scaleLinear()
        // .domain(d3.extent(testDay1, function(d) { return (d.dt); }))
        .domain([0, 60 * 23 + 59])
        .range([0, Math.PI * 2]);

    function calcMins(d) {
        d = new Date(d.dt);
        return (d.getHours() * 60 + d.getMinutes());
    }

    console.log(calcMins(testDay1[0]));

    console.log(theta(calcMins(testDay1[0])));

    var l = d3.radialLine()
        .angle(function(d) { return (theta(calcMins(d.dt))); })
        .radius(function(d) { return (r(d.vol_passed)); });

    // TODO: get outer clock working
    var arc = d3.arc()
        .innerRadius(0)
        .outerRadius(width) // scale with number of days, n x 7 arrangement after getting one working
        .startAngle(0)
        .endAngle(Math.PI / 2);

    svg.append("g")
        .attr("d", arc);

    // TODO: loop this over all calendar days the testing is performed, drawing a new clock every day
    svg.append("path")
        .data([testDay1])
        .attr("transform", `translate(${ width / 2 }, ${ height / 2 })`)
        .attr("d", l);
}
