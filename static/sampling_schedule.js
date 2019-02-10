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

function radial_clockplot(dayDf) {
    var [margin, width, height, svg] = setup_chart_area();

    svg = svg
        .attr("transform", `translate(${ width / 2 }, ${ height / 2 })`);

    var radius = Math.min(width, height) / 2 - Math.max.apply(null, Object.values(margin));

    var r = d3.scaleLinear()
        .domain(d3.extent(dayDf, function(d) { return (d.vol_passed); }))
        .range([0, radius]);

    var theta = d3.scaleLinear()
        .domain([0, 60 * 24])
        .range([0, Math.PI * 2]);

    function calcMins(d) {
        d = new Date(d.dt);
        d = new Date(d.getTime() - d.getTimezoneOffset()); // Hacky locale adjustment TODO: fix either backend or frontend localization
        return (d.getHours() * 60 + d.getMinutes());
    }

    var l = d3.radialLine()
        .angle(function(d) { return theta(calcMins(d)); })
        .radius(function(d) { return r(d.vol_passed); });

    // TODO: get outer clock working
    var rAxis =  svg.append("g")
        .attr("class", "r axis");
        // .selectAll("g")
        // .data(r.ticks(2).slice(1))
        // .enter()
        // .append("g");

    rAxis.append("g")
        .append("circle")
        .attr("r", radius);

    // rAxis.append("text")
    //     .attr("y", function(d) { return -r(d); })
    //     .style("text-anchor", "middle")
    //     .text(function(d) { return d; });


    var thetaAxis = svg.append("g")
        .attr("class", "theta axis")
        .selectAll("g")
        .data(d3.range(0, 24, 1))
        .enter()
        .append("g")
        .attr("transform", function(d) { return `rotate(${(d - 6) * 360 / 24})`; }); // d3 likes to start radial ticks at 3 o'clock

    thetaAxis.append("line")
        .attr("x2", radius)
        .attr("x1", radius*0.8);

    thetaAxis.append("text")
        .attr("x", radius)
        .attr("dy", ".35em")
        .style("text-anchor", function(d) { return d < 24 && d > 12 ? "end" : null; })
        .attr("transform", function(d) { return d < 24 && d > 12 ? `rotate(180 ${radius}, 0)` : null; })
        .text(function(d) {return d; });

    // var arc = d3.arc()
    //     .innerRadius(0)
    //     .outerRadius(width) // scale with number of days, n x 7 arrangement after getting one working
    //     .startAngle(0)
    //     .endAngle(Math.PI / 2);

    // svg.append("g")
    //     .attr("d", arc);

    var samplingHighlight = d3.areaRadial()
        .startAngle(function(d) { return theta(calcMins(d) - 5); })
        .endAngle(function(d) { return theta(calcMins(d) + 5); })
        .innerRadius(radius / 2)
        .outerRadius(radius);

    // TODO: a separate path for each object in the data
    svg.append("g")
        .attr("class", "samplings")
        .selectAll("g")
        .data([dayDf.filter((d) => { return d.sampling_point; })])
        .enter()
        .selectAll("path")
        // .data(function(d) { return d; })
        // .enter()
        .append("path")
        .attr("d", samplingHighlight);

    // TODO: loop this over all calendar days the testing is performed, drawing a new clock every day
    // svg.append("path")
    //     .attr("class", "line")
    //     .data([dayDf])
    //     .attr("d", l);

    // TODO: add area highlight over current time +/- 5 min
}

function multi_clockplots() {
    const calDays = Math.ceil((df.slice(-1)[0].dt - df[0].dt)
                              / (24*3600*1000));
    console.log(calDays);

    // TODO: split this by calendar day of df.dt
    var testDay1 = df.slice(0, 960); // TODO: extract time and date separately
    var calDay1 = df.slice(0, 783); // First calendar day if starting at 11am

    radial_clockplot(calDay1);
}
