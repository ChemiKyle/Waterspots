function draw_lineplot() {
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = window.innerWidth - margin.left - margin.right,
        height = window.innerHeight - margin.top - margin.bottom;

    var x = d3.scaleLinear()
        .domain([0, d3.max(df, function(d) {return (d.cum_mins_running); })])
        .range([0, width]);
    var y = d3.scaleLinear()
        .domain([0, d3.max(df, function(d) {return (d.vol_passed); })])
        .range([height, 0]);

    var xAxis = d3.axisBottom(x);
    var yAxis = d3.axisLeft(y);

    var plot_df = [df.cum_mins_running, df.vol_passed];
    // var plot_df = [[0, 10, 20, 30, 500, 1000], [1500, 1400, 1200, 1000, 800, 500]];

    // var valueline = d3.line()
        // .x(function(d) { return x(d3.values(d[0])); })
        // .y(function(d) { return y(d3.values(d[1])); });
    var valueline = d3.line()
        .x(function(d) { return x(d.cum_mins_running); })
        .y(function(d) { return y(d.vol_passed); });

    var svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // x.domain(d3.extent(df, function(df) {return df.cum_mins_running; }));
    // y.domain([0, d3.max(df, function(df) {return df.vol_passed; })]);

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(0, ${height})`)
        .call(xAxis);

    svg.append("g")
        .attr("class", "axis")
        .call(yAxis);

    svg.append("path")
        .data([df])
        .attr("class", "line")
        .attr("d", valueline);
}
