function draw_lineplot() {
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 600 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

    var x = d3.scaleLinear()
        .domain([0, d3.max(d3.values(df))])
        .range([0, width]);
    var y = d3.scaleLinear()
        .domain([0, d3.max(d3.values(df))])
        .range([0, height]);

    var xAxis = d3.axisBottom([0, width]).scale(x);
    var yAxis = d3.axisLeft([0, height]).scale(y);

    var valueline = d3.line()
        .x(function(df) { return x(df.cum_mins_running); })
        .y(function(df) { return y(df.vol_passed); });

    var svg = d3.select("#chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g");

    // x.domain(d3.extent(df, function(df) {return df.cum_mins_running; }));
    // y.domain([0, d3.max(df, function(df) {return df.vol_passed; })]);

    svg.append("path")
        .data([df])
        .attr("class", "line")
        .attr("d", valueline);

    svg.append("g")
        .attr("class", "x axis")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

}
