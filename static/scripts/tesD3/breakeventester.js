// import unemployment from './unemployment.js' ;
$('#graphnumber').on('change', function (){
  var data = []
  var proc_data = getData()
  for (var index = 0; index < $('#graphnumber').val(); index++) {
    data.push({
      "division": "Unit Price",
      "date": index+1,
      "unemployment": proc_data.budgetPerUnit
    })
    
  }

  var totalMaterialCost = parseInt(removeNonDigit($('#totalMaterialCost').val()))
  var totalOutsourceCost = parseInt(removeNonDigit($('#totalOutsourceCost').val()))
  for (var i = 0; i < $('#graphnumber').val(); i++) {
    
    var othercost = parseFloat(getTotalOtherCost()) / proc_data.quantity
    var procccost = parseFloat( $('#totalOperationCost').val() ) / (i+1)
    var tot = totalMaterialCost 
    + totalOutsourceCost 
    + othercost
    + procccost

    // console.log(othercost, procccost);
    data.push({
      "division": "Sell Unit Price",
      "date": i+1,
      "unemployment": tot
    })
    
  }

  // console.log(totalMaterialCost, totalOutsourceCost);
  // console.log(data);
  updateGraph(data);
})

var unemployment = [  
    {
      "division": "Sell Unit Price",
      "date": 1,
      "unemployment": 4.9
    },
    {
      "division": "Sell Unit Price",
      "date": 2,
      "unemployment": 4.5
    },
    {
      "division": "Sell Unit Price",
      "date": 3,
      "unemployment": 4.3
    },
    {
      "division": "Sell Unit Price",
      "date": 4,
      "unemployment": 4.0
    },
    {
      "division": "Sell Unit Price",
      "date": 5,
      "unemployment": 3.9
    },
    {
      "division": "Sell Unit Price",
      "date": 6,
      "unemployment": 3.8
    },
    {
      "division": "Sell Unit Price",
      "date": 7,
      "unemployment": 3.7
    },  
    {
      "division": "Unit Price",
      "date": 1,
      "unemployment": 4
    },
    {
      "division": "Unit Price",
      "date": 2,
      "unemployment": 4
    },
    {
      "division": "Unit Price",
      "date": 3,
      "unemployment": 4
    },
    {
      "division": "Unit Price",
      "date": 4,
      "unemployment": 4
    },
    {
      "division": "Unit Price",
      "date": 5,
      "unemployment": 4
    },
    {
      "division": "Unit Price",
      "date": 6,
      "unemployment": 4
    },
    {
      "division": "Unit Price",
      "date": 7,
      "unemployment": 4
    } ]
  


function updateGraph(unemployment){
  // Specify the chart’s dimensions.
  const width = 1500;
  const height = 800;
  const marginTop = 20;
  const marginRight = 20;
  const marginBottom = 30;
  const marginLeft = 30;

  // Create the positional scales.
  const x = d3.scaleUtc()
    .domain(d3.extent(unemployment, d => d.date))
    .range([marginLeft, width - marginRight]);

  const y = d3.scaleLinear()
    .domain([0, d3.max(unemployment, d => d.unemployment)]).nice()
    .range([height - marginBottom, marginTop]);

    d3.select("#myPlot svg").remove();
  // Create the SVG container.
  const svg = d3.select("#myPlot")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; overflow: visible; font: 10px sans-serif;")
      .append("g")
      .attr("transform", "translate(" + marginLeft + "," + marginTop + ")");

  // Add the horizontal axis.
  svg.append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .style('font-size', "14px")
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));

  // Add the vertical axis.
  svg.append("g")
      .attr("transform", `translate(${marginLeft},0)`)
      .style('font-size', "14px")
      .call(d3.axisLeft(y))
      .call(g => g.select(".domain").remove())
          // .call(voronoi ? () => {} : g => g.selectAll(".tick line").clone()
          //     .attr("x2", width - marginLeft - marginRight)
          //     .attr("stroke-opacity", 0.1))
      .call(g => g.append("text")
          .attr("x", -marginLeft)
          .attr("y", 10)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text("Price"));


  // Compute the points in pixel space as [x, y, z], where z is the name of the series.
  const points = unemployment.map((d) => [x(d.date), y(d.unemployment), d.division]);

  // // An optional Voronoi display (for fun).
  // if (voronoi) svg.append("path")
  //     .attr("fill", "none")
  //     .attr("stroke", "#ccc")
  //     .attr("d", d3.Delaunay
  //       .from(points)
  //       .voronoi([0, 0, width, height])
  //       .render());

  // Group the points by series.
  const groups = d3.rollup(points, v => Object.assign(v, {z: v[0][2]}), d => d[2]);


 // Add Grid Line
svg.append("g")
	.attr("stroke", "currentColor")
	.attr("stroke-opacity", 0.1)
	.call(g => g.append("g")
		.selectAll("line")
		.data(x.ticks())
		.join("line")
		.attr("x1", d => 0.5 + x(d))
		.attr("x2", d => 0.5 + x(d))
		.attr("y1", marginTop)
		.attr("y2", height - marginBottom))
	.call(g => g.append("g")
		.selectAll("line")
		.data(y.ticks())
		.join("line")
		.attr("y1", d => 0.5 + y(d))
		.attr("y2", d => 0.5 + y(d))
		.attr("x1", marginLeft)
		.attr("x2", width - marginRight));

  // Draw the lines.
  const line = d3.line();
  const path = svg.append("g")
      .attr("fill", "none")
    .selectAll("path")
    .data(groups.values())
    .join("path")
      .attr("stroke",  (d, i) => ["green", "blue"][i])
      .attr("stroke-width", 2)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .style("mix-blend-mode", "multiply")
      .attr("d", line);
  // console.log(groups);

  //draw the dots
 
  // Add an invisible layer for the interactive tip.
  // console.log(d => d,quantity);
  const dot = svg.append("g")
      .attr("display", "none");

  dot.append("circle")
      .attr("r", 4);

  dot.append("text")
      .attr("text-anchor", "middle")
      .attr("y", -8);
  
  svg
      .on("pointerenter", pointerentered)
      .on("pointermove", pointermoved)
      .on("pointerleave", pointerleft)
      .on("touchstart", event => event.preventDefault());



  // When the pointer moves, find the closest point, update the interactive tip, and highlight
  // the corresponding line. Note: we don't actually use Voronoi here, since an exhaustive search
  // is fast enough.
  function pointermoved(event) {
    const [xm, ym] = d3.pointer(event);
    const i = d3.leastIndex(points, ([x, y]) => Math.hypot(x - xm, y - ym));
    const [x, y, k] = points[i];
    path.style("stroke", ({z}) => z === k ? null : "#ddd").filter(({z}) => z === k).raise();
    dot.attr("transform", `translate(${x},${y})`);
    dot.select("text").text(k);
    svg.property("value", unemployment[i]).dispatch("input", {bubbles: true});
  }

  function pointerentered() {
    path.style("mix-blend-mode", null).style("stroke", "#ddd");
    dot.attr("display", null);
  }

  function pointerleft() {
    path.style("mix-blend-mode", "multiply").style("stroke", null);
    dot.attr("display", "none");
    svg.node().value = null;
    svg.dispatch("input", {bubbles: true});
  }
}