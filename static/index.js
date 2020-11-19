function renderScatterPlot() {
    let radius_normal = 6
    let radius_selected = 8
    let color_default = "#69b3a2"
    let color_selected = "#EC888C"
    let color_target = "red"
    let color_before_mouseover = null
    let radius_before_mouseover = null
        // let color_labeled = ""
    let bb = document.querySelector('#scatterPlot')
        .getBoundingClientRect()
    let innerwidth = 1 * (bb.right - bb.left)
    let aspectRatio = 1
    let innerheight = innerwidth / aspectRatio
    let margin = {
        left: 20,
        top: 10,
        right: 10,
        bottom: 20
    }

    function assignColor(index) {
        if (isClassified) {
            return myColor(category_list[index])
        } else {
            if (index == indexOfSelectedDoc) {
                return color_target
            } else {
                return color_default
            }
        }
    }

    $("#scatterPlot").empty();
    let svg_scatterPlot = d3.select('#scatterPlot')
        .append('svg')
        .attr("viewBox", [0, 0, innerwidth, innerheight])

    // Add X axis
    let projection_mode = 2
    let value_range = []
    if (projection_mode == 1) {
        value_range = [
            // [-5*aspectRatio, 2.1*aspectRatio],
            // [-5, 2.1]
            [-5 * aspectRatio, 4 * aspectRatio],
            [-5, 4]
        ]
    } else {
        value_range = [
            [-50, 50],
            [-50, 50]
        ]
    }

    var x = d3.scaleLinear()
        .domain(value_range[0])
        .range([0, innerwidth]);
    var y = d3.scaleLinear()
        .domain(value_range[1])
        .range([innerheight, 0]);
    xAxis = svg_scatterPlot.append("g")
        .attr("id", "xAxis")
        .attr("transform", "translate(0," + String(innerheight - margin.bottom) + ")")
        .call(d3.axisBottom(x));
    yAxis = svg_scatterPlot.append("g")
        .attr("id", "yAxis")
        .attr("transform", "translate(" + margin.left + ", 0)")
        .call(d3.axisLeft(y));

    var clip = svg_scatterPlot.append("defs")
        .append("SVG:clipPath")
        .attr("id", "clip")
        .append("SVG:rect")
        .attr("width", innerwidth)
        .attr("height", innerheight)
        .attr("x", 0)
        .attr("y", 0);

    var scatter = svg_scatterPlot.append('g')
        .attr("clip-path", "url(#clip)")

    let coordsAndId = []
    ads_id_list = []
    for (let i = 0; i < docs.length; i++) {
        let doc = docs[i]
        for (key in doc) {
            ads_id_list.push(key)
        }
    }

    for (let i = 0; i < coords.length; i++) {
        coordsAndId.push({
            'coord': coords[i],
            'index': ads_id_list[i]
        })
    }
    let all_dots = scatter.selectAll(".dot")
        .data(coordsAndId)
        .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("id", function(d) {
            return "dot_" + d.index;
        })
        .attr("cx", function(d) {
            return x(d.coord[0]);
        })
        .attr("cy", function(d) {
            return y(d.coord[1]);
        })
        .attr("r", radius_normal)
        .style("fill", d => assignColor(d.index))
        .style("fill-opacity", 0.5)
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);

    renderSelectedNodes(scatter, lassoSelectedDocs_id, color_selected)

    // for(let i = 0; i < lassoSelectedDocs_id.length; i++){
    //     let id_t = "#dot_" + lassoSelectedDocs_id[i]
    //     scatter
    //         .select(id_t)
    //         .style("fill", color_selected);
    // }
    scatter.select("#dot_" + indexOfSelectedDoc).style("fill", color_target)

    let zoom = d3.zoom()
        .scaleExtent([.5, 20]) // This control how much you can unzoom (x0.5) and zoom (x20)
        .extent([
            [0, 0],
            [innerwidth, innerheight]
        ])
        .on("zoom", updateChart);

    if (ZoomEnable) {
        var zoom_area = svg_scatterPlot.append("rect")
            .attr("width", innerwidth)
            .attr("height", innerheight)
            .style("fill", "none")
            .style("pointer-events", "all")
            // .call(zoom)
        if (zoomState === null) {
            zoom_area.call(zoom)
        } else {
            zoom_area.call(zoom.transform, d3.zoomIdentity.scale(zoomState.k).translate(zoomState.x / zoomState.k, zoomState.y / zoomState.k))
            zoom_area.call(zoom)
        }
    } else {
        lasso()
        xAxis.call(d3.axisBottom(x_temp))
        yAxis.call(d3.axisLeft(y_temp))
        scatter
            .selectAll(".dot")
            .attr('cx', function(d) {
                return x_temp(d.coord[0])
            })
            .attr('cy', function(d) {
                return y_temp(d.coord[1])
            });
    }

    function handleMouseOver(d, i) {
        let id_temp = '#dot_' + d.index
        color_before_mouseover = d3.select(id_temp).style("fill")
        radius_before_mouseover = d3.select(id_temp).attr("r")
        d3.select('#dot_' + d.index)
            .attr("r", radius_selected)
            .style("fill", "orange");
        svg_scatterPlot.append("text")
            .text(d.index)
            .attr("id", "t_" + d.index)
            .attr("x", function() {
                if (x_temp === null) {
                    return x(d.coord[0]) + 5;
                } else {
                    return x_temp(d.coord[0]) + 5;
                }
            })
            .attr("y", function() {
                if (y_temp === null) {
                    return y(d.coord[1]) - 5;
                } else {
                    return y_temp(d.coord[1]) - 5;
                }

            });
    }

    function handleMouseOut(d, i) {
        d3.select('#dot_' + d.index)
            .attr("r", radius_before_mouseover)
            .style("fill", color_before_mouseover);
        d3.select("#t_" + d.index).remove(); // Remove text location
    }

    function updateChart() {
        // recover the new scale
        var newX = d3.event.transform.rescaleX(x);
        var scale_k = d3.event.transform.k
        var newY = d3.event.transform.rescaleY(y);

        x_temp = newX
        y_temp = newY

        // update axes with these new boundaries
        xAxis.call(d3.axisBottom(newX))
        yAxis.call(d3.axisLeft(newY))

        // update circle position
        scatter
            .selectAll(".dot")
            .attr('cx', function(d) {
                return newX(d.coord[0])
            })
            .attr('cy', function(d) {
                return newY(d.coord[1])
            });
        for (let i = 0; i < lassoSelectedDocs_id.length; i++) {
            let id_t = "#dot_" + lassoSelectedDocs_id[i]
            scatter
                .select(id_t)
                .style("fill", color_selected);
        }
        zoomState = d3.event.transform
    }

    function lasso() {
        // Lasso functions
        let lasso_start = function() {
            lasso.items()
                .attr("r", radius_normal) // reset size
                .classed("not_possible", true)
                .classed("selected", false);
            scatter.select("#dot_" + indexOfSelectedDoc).style("fill", color_target)
        };

        let lasso_draw = function() {

            // Style the possible dots
            lasso.possibleItems()
                .classed("not_possible", false)
                .classed("possible", true);

            // Style the not possible dot
            lasso.notPossibleItems()
                .classed("not_possible", true)
                .classed("possible", false);

            if (!Append_mode) {
                lassoSelectedDocs_id = []
            }
            scatter.select("#dot_" + indexOfSelectedDoc).style("fill", color_target)
        };

        let lasso_end = function() {
            // Reset the color of all dots
            lasso.items()
                .classed("not_possible", false)
                .classed("possible", false);

            // Style the selected dots
            lasso.selectedItems()
                .classed("selected", true)
                .attr("r", radius_selected)
                .style("fill", color_selected);

            scatter.selectAll(".selected")
                .classed("selected", true)

            // Reset the style of the not selected dots
            lasso.notSelectedItems()
                .attr("r", radius_normal)
                .style("fill", d => assignColor(Number(d.index)))

            scatter.select("#dot_" + indexOfSelectedDoc).style("fill", color_target)

            var regexp = /\d+/g
            if (Append_mode) {
                let t = lasso.selectedItems()['_groups'][0].map(x => Number(x.getAttribute('id').match(regexp)[0]))
                for (let i = 0; i < t.length; i++) {
                    if (!lassoSelectedDocs_id.includes(t[i])) {
                        lassoSelectedDocs_id.push(t[i])
                    }
                }
            } else {
                lassoSelectedDocs_id = []
                lassoSelectedDocs_id = lasso.selectedItems()['_groups'][0].map(x => Number(x.getAttribute('id').match(regexp)[0]))
            }

            renderSelectedNodes(scatter, lassoSelectedDocs_id, color_selected)
                // renderBatchesIdeationTable(lassoSelectedDocs_id, null, batches)
            renderDocsTable(docs, vectors)


            if (lassoSelectedDocs_id.length > 0) {
                var data = {
                    "lassoSelectedDocs_id": String(lassoSelectedDocs_id)
                };

                jQuery.getJSON("{% url 'polls:getLassoDocs' %}", data, function(ret) {
                    var lasso_docs = JSON.parse(ret['docs'])
                    var lasso_vectors = JSON.parse(ret['vectors'])
                    renderHeatmap(lasso_vectors)
                    renderDocsTable(lasso_docs, lasso_vectors)
                })
            }
        };

        let lasso = d3.lasso()
            .closePathSelect(true)
            .closePathDistance(100)
            .items(all_dots)
            .targetArea(svg_scatterPlot)
            .on("start", lasso_start)
            .on("draw", lasso_draw)
            .on("end", lasso_end);

        svg_scatterPlot.call(lasso);
    }
}