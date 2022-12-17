function chart(data, id){
  var time = data["timestamp"]

  const months = {0 : 'Jan', 1 : 'Feb', 2 : 'Mar', 3 : 'Apr', 4 : 'May', 5 : 'Jun', 6 : 'Jul', 7 : 'Aug', 8 : 'Sep', 9 : 'Oct', 10 : 'Nov', 11 : 'Dec'}
  var dateFormat = d3.timeParse("%Y-%m-%d");
  
  data['Date'] = time.map(d => new Date(d*1000).getFullYear()+"-"+(new Date(d*1000).getMonth())+"-"+new Date(d*1000).getDate())
  for (let i = 0; i < data.length; i++) {

      data[i]['Date'] = dateFormat(data[i]['Date'])
  }

  var modify_data = []
  for(let i=0; i< time.length; i++){
      modify_data.push({"Date": time[i], "High": data['high'][i], "Low": data['low'][i], "Open": data['open'][i], "Close": data['close'][i], 'Volume': data['volume'][i]})
  }
  const margin = {top: 15, right: 50, bottom: 205, left: 50},
  w = 1200 - margin.left - margin.right,
  h = 900 - margin.top - margin.bottom;

  var svg = d3.select("#container"+id)
  .attr("width", w + margin.left + margin.right)
  .attr("height", h + margin.top + margin.bottom)
  .append("g")
  .attr("id", "hello")
  .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");

  let dates = modify_data.map(d => d["Date"])

  var xmin = d3.min(dates.map(r => new Date(r*1000).getTime()));
  var xmax = d3.max(dates.map(r => new Date(r*1000).getTime()));
  
  
  var xScale = d3.scaleLinear().domain([-1, dates.length])
  .range([0, w])
  
  var xDateScale = d3.scaleQuantize().domain([0, dates.length]).range(dates)
  let xBand = d3.scaleBand().domain(d3.range(-1, dates.length)).range([0, w]).padding(0.3)
  
  var xAxis = d3.axisBottom()
  .scale(xScale)
  .tickFormat(function(d) {
      d = new Date(dates[d]*1000)
      hours = d.getHours()
      minutes = (d.getMinutes()<10?'0':'') + d.getMinutes() 
      amPM = hours < 13 ? 'am' : 'pm'
      return hours + ':' + minutes + amPM + ' ' + d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear()
      });
      
      svg.append("rect")
      .attr("id","rect")
      .attr("width", w)
      .attr("height", h)
      .style("fill", "none")
      .style("pointer-events", "all")
      .attr("clip-path", "url(#clip)")
      
      var gX = svg.append("g")
      .attr("class", "axis x-axis") //Assign "axis" class
      .attr("transform", "translate(0," + h + ")")
      .call(xAxis)
      
      gX.selectAll(".tick text")
      .call(wrap, xBand.bandwidth())
      
      
      var ymin = d3.min(modify_data.map(l => l.Low));
      var ymax = d3.max(modify_data.map(h => h.High));

      var vmin = d3.min(modify_data.map(v => v.Volume));
      var vmax = d3.max(modify_data.map(v => v.Volume));
      
      var yScale = d3.scaleLinear().domain([ymin, ymax]).range([h, 0]).nice();
      var yAxis = d3.axisLeft()
      .scale(yScale)
      
      var vScale = d3.scaleLinear().domain([0, vmax]).range([h, 600]).nice();
      var vAxis = d3.axisRight()
      .scale(vScale)

      var gV = svg.append("g")
      .attr("class", "axis y-axis")
      .call(vAxis);
      
      
      var gY = svg.append("g")
      .attr("class", "axis y-axis")
      .call(yAxis);

      var chartBody = svg.append("g")
      .attr("class", "chartBody")
      .attr("clip-path", "url(#clip)");
      
      
      // draw rectangles
      let candles = chartBody.selectAll(".candle")
      .data(modify_data)
      .enter()
      .append("rect")
      .attr('x', (d, i) => xScale(i) - xBand.bandwidth())
      .attr("class", "candle")
      .attr('y', d => yScale(Math.max(d.Open, d.Close)))
      .attr('width', xBand.bandwidth())
      .attr('height', d => (d.Open === d.Close) ? 1 : yScale(Math.min(d.Open, d.Close))-yScale(Math.max(d.Open, d.Close)))
      .attr("fill", d => (d.Open === d.Close) ? "silver" : (d.Open > d.Close) ? "red" : "green")
      
      // draw high and low
      let stems = chartBody.selectAll("g.line")
      .data(modify_data)
      .enter()
      .append("line")
      .attr("class", "stem")
      .attr("x1", (d, i) => xScale(i) - xBand.bandwidth()/2)
      .attr("x2", (d, i) => xScale(i) - xBand.bandwidth()/2)
      .attr("y1", d => yScale(d.High))
      .attr("y2", d => yScale(d.Low))
      .attr("stroke", d => (d.Open === d.Close) ? "white" : (d.Open > d.Close) ? "red" : "green");

      let volume = chartBody.selectAll(".volume")
      .data(modify_data)
      .enter()
      .append("rect")
      .attr('x', (d, i) => xScale(i) - xBand.bandwidth())
      .attr("class", "bar_volume")
      .attr('y', d => vScale(Math.max(d.Volume)))
      .attr("width", xBand.bandwidth())
      .attr("height", d => h - vScale(d.Volume))
      .attr("fill", d =>(d.Open === d.Close) ? "silver" : (d.Open > d.Close) ? "red" : "green")

      svg.append("defs")
      .append("clipPath")
      .attr("id", "clip")
      .append("rect")
      .attr("width", w)
      .attr("height", h)

  const extent = [[0, 0], [w, h]];

  var resizeTimer;
  var zoom = d3.zoom()
  .scaleExtent([1, 1000])
  .translateExtent(extent)
  .extent(extent)
  .on("zoom", zoomed)
  .on('zoom.end', zoomend);
  
  svg.call(zoom)  

  function zoomed() {

      var t = d3.event.transform;
      let xScaleZ = t.rescaleX(xScale);
      
      let hideTicksWithoutLabel = function() {
          d3.selectAll('.xAxis .tick text').each(function(d){
              if(this.innerHTML === '') {
              this.parentNode.style.display = 'none'
              }
          })
      }

      gX.call(
          d3.axisBottom(xScaleZ).tickFormat((d, e, target) => {
              if (d >= 0 && d <= dates.length-1) {
                  d = new Date(dates[d]*1000)
                  hours = d.getHours()
                  minutes = (d.getMinutes()<10?'0':'') + d.getMinutes() 
                  amPM = hours < 13 ? 'am' : 'pm'
              return d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear()
              }
          })
      )

      candles.attr("x", (d, i) => xScaleZ(i) - (xBand.bandwidth()*t.k)/2)
              .attr("width", xBand.bandwidth()*t.k);
      stems.attr("x1", (d, i) => xScaleZ(i) - xBand.bandwidth()/2 + xBand.bandwidth()*0.5);
      stems.attr("x2", (d, i) => xScaleZ(i) - xBand.bandwidth()/2 + xBand.bandwidth()*0.5);

      volume.attr("x", (d, i) => xScaleZ(i) - (xBand.bandwidth()*t.k)/2)
          .attr("width", xBand.bandwidth()*t.k);

      hideTicksWithoutLabel();

      gX.selectAll(".tick text")
      .call(wrap, xBand.bandwidth())

  }


  function zoomend() {
      var t = d3.event.transform;
      let xScaleZ = t.rescaleX(xScale);
      clearTimeout(resizeTimer)
      resizeTimer = setTimeout(function() {

      var xmin = new Date(xDateScale(Math.floor(xScaleZ.domain()[0]))*1000)
      var xmax = new Date(xDateScale(Math.floor(xScaleZ.domain()[1]))*1000)


      var filtered = dates.map(d => ((new Date(d*1000) >= xmin) && (new Date(d*1000) <= xmax)))
      var filtered_low = []
      var filtered_high = []
      var filtered_volume = []
      for(let i=0; i < filtered.length; i++){
          if (filtered[i] ==true) {
              filtered_low.push(data['low'][i])
              filtered_high.push(data['high'][i])
              filtered_volume.push(data['volume'][i])
          }
      }
      minP = +d3.min(filtered_low)
      maxP = +d3.max(filtered_high)
      minV = 0
      maxV = +d3.max(filtered_volume)

      buffer = Math.floor((maxP - minP) * 0.1)
      buffer_v  = Math.floor((maxV - minV) * 0.1)


      yScale.domain([minP - buffer, maxP + buffer])
      vScale.domain([minV - buffer_v, maxV+ buffer_v])

      candles.transition()
          .duration(800)
          .attr("y", (d) => yScale(Math.max(d.Open, d.Close)))
          .attr("height",  (d) => (d.Open === d.Close) ? 1 : yScale(Math.min(d.Open, d.Close))-yScale(Math.max(d.Open, d.Close)));
          
      stems.transition().duration(800)
          .attr("y1", (d) => yScale(d.High))
          .attr("y2", (d) => yScale(d.Low))
      
      volume.transition()
      .duration(800)
      .attr("y", d => vScale(Math.max(d.Volume)))
      .attr("height", d => h - vScale(d.Volume))
      
      gY.transition().duration(800).call(d3.axisLeft().scale(yScale));
      gV.transition().duration(800).call(d3.axisRight().scale(vScale));

      }, 500)
      
  }



  function wrap(text, width) {
      text.each(function() {
      var text = d3.select(this),
          words = text.text().split(/\s+/).reverse(),
          word,
          line = [],
          lineNumber = 0,
          lineHeight = 1.1, // ems
          y = text.attr("y"),
          dy = parseFloat(text.attr("dy")),
          tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
          while (word = words.pop()) {
              line.push(word);
              tspan.text(line.join(" "));
              if (tspan.node().getComputedTextLength() > width) {
              line.pop();
              tspan.text(line.join(" "));
              line = [word];
              tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
          }
      }
      });
  }
}
