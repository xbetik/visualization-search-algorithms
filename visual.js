const padding_x = 250;
const padding_y = 90;
const most_right_label_padding = 150;
const most_down_label_padding = 50;
const between_node_label_gap = 10;
let tree_width = 960;
let tree_height = 180;
let treeRevealed = false;
let animationOn = false;
let nodes;
let links;
let nodeGap = 0;
let counter = 0;
let cfg_shown = false;

init();

function init() {
    let svg = d3.select("body").append("svg");
    let canvas = svg.attr({
        "width" : tree_width+padding_x+most_right_label_padding,
        "height" : padding_y + (tree_height*(labels.length+1)) + most_down_label_padding
    })
        .append("g")
        .attr("transform", "translate(" + padding_x + "," + padding_y + ")");

    let tree = d3.layout.tree()
        .size([tree_width]);

    nodes = tree.nodes(treeData);
    links = getLinks();
    // Normalize the depth
    nodes.forEach(function(d) { d.y = d.depth * tree_height; });

    addTreeLabel(canvas);
    addMarkers(svg);
    addLinks(canvas);
    addRightEdgeLabels(canvas);
    addLeftEdgeLabels(canvas);
    let node = addNodes(canvas);
    addNodeShape(node);
    addNodeName(node);
    addBottomLabel(node);
    addSideLabels();
    addJumps(svg);
    showFrame();
}

function jumpDirection(source_index, target_index) {
    if (getNode(source_index).x < getNode(target_index).x) {
        return -100;
    }
    return 100;
}

function addJumps(svg) {
    var lineFunction = d3.svg.line()
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; })
        .interpolate("basis");

    for (let i = 0; i < nodes.length; i++) {
        var y = getNode(nodes[i].nodeOrder).y - ((getNode(nodes[i].nodeOrder).y-getNode(nodes[i].jump).y)/2);
        if (typeof nodes[i].jump !== "undefined") {
            svg.append("path")
                .attr("id", "jump-" + (nodes[i].nodeOrder-1))
                .attr("stroke-width", "3px")
                .attr("fill", "none")
                .attr("stroke", "black")
                .attr("d", lineFunction([
                    { "x" : getNode(nodes[i].nodeOrder).x, "y" : getNode(nodes[i].nodeOrder).y-10 },
                    { "x" : getNode(nodes[i].jump).x+jumpDirection(nodes[i].nodeOrder, nodes[i].jump), "y" : y},
                    { "x" : getNode(nodes[i].jump).x, "y" : getNode(nodes[i].jump).y }
                ]))
                .attr("transform", "translate(" + padding_x + "," + padding_y + ")")
                .attr("visibility", "hidden")
                .attr("stroke-dasharray", ("3, 3"))
                .attr("marker-end", "url(#arrowToNode)");
        }
    }
}

function getNode(index) {
    for (let i=0;i<nodes.length;i++) {
        if (nodes[i].nodeOrder === index) {
            return nodes[i];
        }
    }
    return -1;
}


function getLinks() {
    let links = [];
    for(let i=1; i < nodes.length; i++) {
        let target = getNode(i+1);
        if (target !== -1) {
            links.push( { source : target.parent, target : target } );
        }
    }
    return links;
}

function addMarkers(svg) {
    svg.append("marker")
        .attr("id", "arrowToNode")
        .attr("viewBox", "-0 -5 10 10")
        .attr("refX", 14)
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 20)
        .attr("markerHeight", 20)
        .attr("markerUnits", "userSpaceOnUse")
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', "none")
        .style('stroke','black');

    svg.append("marker")
        .attr("id", "arrowFromNode")
        .attr("viewBox", "-0 -5 10 10")
        .attr("refX", 16)
        .attr("refY", 0)
        .attr("orient", "auto-start-reverse")
        .attr("markerWidth", 20)
        .attr("markerHeight", 20)
        .attr("markerUnits", "userSpaceOnUse")
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', "none")
        .style('stroke','black');
}

function addLinks(canvas) {
    let id_counter = 0;
    canvas.selectAll(".link")
        .data(links, function(d) { return d.id = ++id_counter; })
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("id", function (d) { return "link-"+d.id})
        .attr('x1', function (d) {return d.source.x;})
        .attr('x2', function (d) {return d.target.x;})
        .attr('y1', function (d) {return d.source.y;})
        .attr('y2', function (d) {return d.target.y;})
        .attr("stroke", "black")
        .attr("stroke-width", stroke_width)
        .attr("stroke-dasharray", function(d) { return d.target.dashLine === "yes" ? ("3, 3") : ("0, 0")})
        .attr("visibility", "hidden")
        .attr("marker-end", function(d) { return d.target.arrowToNode === "yes" ? "url(#arrowToNode)" : "url()"})
        .attr("marker-start", function(d) { return d.target.arrowFromNode === "yes" ? "url(#arrowFromNode)" : "url()"});
}

function countLeftLabelShift(line) {
    let multiply_constant = 2;
    let opposite = line.target.y-line.source.y;
    let the_leg = Math.abs(line.target.x-line.source.x);
    let hypotenuse = Math.sqrt(opposite*opposite+the_leg*the_leg);
    let angle = Math.asin(opposite/hypotenuse);
    let shift = (10/angle)*multiply_constant;
    if(line.source.x > line.target.x) {
        return line.source.x - (the_leg/2) - shift;
    }
    else if(line.source.x < line.target.x) {
        let angle = Math.asin(opposite/hypotenuse);
        let shift = (10/angle)*multiply_constant;
        return line.target.x - ((the_leg)/2) - shift;
    }
    else {
        return line.target.x -15;
    }
}

function countRightLabelShift(line) {
    let multiply_constant = 2;
    let opposite = line.target.y-line.source.y;
    let the_leg = Math.abs(line.target.x-line.source.x);
    let hypotenuse = Math.sqrt(opposite*opposite+the_leg*the_leg);
    let angle = Math.asin(opposite/hypotenuse);
    let shift = (10/angle)*multiply_constant;
    if(line.source.x > line.target.x) {
        return line.source.x - (the_leg/2) + shift;
    }
    else if(line.source.x < line.target.x) {
        let angle = Math.asin(opposite/hypotenuse);
        let shift = (10/angle)*multiply_constant;
        return line.target.x - ((the_leg)/2);
    }
    else {
        return line.target.x + 15;
    }
}


function addRightEdgeLabels(canvas) {
    let id_counter = 0;
    canvas.selectAll(".edgeLabelsRight")
        .data(links, function(d) { return d.id = ++id_counter; })
        .enter()
        .append("text")
        .attr("class", "edgeLabelsRight")
        .attr("id", function(d) { return "edgeLabelRight-"+d.id })
        .attr("y", function(d) { return d.target.y - ((d.target.y - d.source.y) / 2)})
        .attr("x", function(d) { return countRightLabelShift(d)})
        .text(function(d) { return d.target.edgeLabelRight; })
        .attr("visibility", "hidden")
        .attr("font-weight", "bold");
}

function addLeftEdgeLabels(canvas) {
    let id_counter = 0;
    canvas.selectAll(".edgeLabelsLeft")
        .data(links, function(d) { return d.id = ++id_counter; })
        .enter()
        .append("text")
        .attr("class", "edgeLabelsLeft")
        .attr("id", function(d) { return "edgeLabelLeft-"+d.id })
        .attr("y", function(d) { return d.target.y - ((d.target.y - d.source.y) / 2)})
        .attr("x", function(d) { return countLeftLabelShift(d)})
        .attr("width", "100px")
        .text(function(d) { return d.target.edgeLabelLeft; })
        .style("overflow", "hidden")
        .attr("visibility", "hidden")
        .attr("font-weight", "bold");
}

function addNodes(canvas) {
    let id_counter = 0;
    let node = canvas.selectAll(".node")
        .data(nodes, function (d) { return d.id = nodes[id_counter++].nodeOrder-1; })
        .enter()
        .append("g")
        .attr("id", function(d) { return "g-node-" +d.id})
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    return node;
}

function addNodeShape(node) {
    node.append("path")
        .style("stroke", "black")
        .attr("visibility", "hidden")
        .attr("id",function(d){return "node-"+d.id})
        .style("fill", function(d) { return d.nodeColor === 'blank' ? "white" : d.nodeColor })
        .attr("d", d3.svg.symbol()
            .size(function() { return typeof node_size === "undefined" ? 400 : node_size})
            .type(function(d) { return d.shape === "rectangle" ? "square" : "circle"}));
}

function addNodeName(node) {
    node.append("text")
        .attr("class", "nodeName")
        .text(function (d) {return d.name; })
        .attr("id",function(d){return "text-"+d.id})
        .attr("visibility", "hidden")
        .style("fill", function(d) { return typeof d.nodeColor === "undefined" ? "white" : "black" })
        .attr({
            "text-anchor" : "middle",
            "y" : 6,
            "font-weight" : "bold"
        });
}

function addBottomLabel(node) {
    node.append("text")
        .attr("class", "nodeLabel")
        .text(function(d) { return d.nodeLabel; })
        .attr({
            "id" : function(d) { return "nodeLabel1-"+d.id; },
            "visibility" : "hidden",
            "text-anchor" : "middle",
            "y" : function() { return typeof node_size === "undefined" ? 400/between_node_label_gap : node_size/between_node_label_gap},
            "font-weight" : "bold",
        });
}

function addSideLabels() {
    for(let i=0;i<nodes.length;i++) {
        if (typeof nodes[i].sideLabels !== "undefined") {
            for(let j=0; j<nodes[i].sideLabels.length; j++) {
                d3.select("#g-node-" + (nodes[i].nodeOrder-1))
                    .append("text")
                    .attr("id","sideLabel-"+ (nodes[i].nodeOrder-1))
                    .attr("class", "sideLabels")
                    .attr("visibility", "hidden")
                    .text(nodes[i].sideLabels[j])
                    .attr({
                        "x" : 20,
                        "y" : (j*18)+5,
                        "font-weight" : "bold"
                    })
            }
        }
    }
}

function addTreeLabel(canvas) {
    let level = 1;
    let domain_labels = canvas.append("g")
        .attr("class", "domain_labels")
        .selectAll("domain_labels")
        .data(labels)
        .enter()
        .append("g")
        .attr("class", "domain_label")
        .attr("transform", function(d) {
            return "translate(" + -20 + "," + level++*tree_height + ")";
        });
    level = 1;
    domain_labels.append("text")
        .text(function(d) { return d})
        .attr({
            "id" : function(d) { return "treeLabel-" + level++; },
            "visibility" : "hidden",
            "font-weight" : "bold",
            "font-family" : "monospace"
        });
}

function reveal(element) {
    d3.select(element).attr("visibility", "visible");
}

function revealAll(element) {
    d3.selectAll(element).attr("visibility", "visible");
}

function hide(element) {
    d3.select(element).attr("visibility", "hidden");
}

function hideAll(element) {
    d3.selectAll(element).attr("visibility", "hidden");
}

function revealBackJump(i) {
    if (typeof nodes[i].jump !== "undefined") {
        if (treeRevealed) {
            d3.select("#jump-"+i).attr("stroke", "red");
        }
        else {
            reveal("#jump-"+i);
        }
    }
}

function hideBackJump(i) {
    if (typeof nodes[i].jump !== "undefined") {
        if (treeRevealed) {
            d3.select("#jump-"+i).attr("stroke", "black")
        }
        else {
            hide("#jump-"+i);
        }
    }
}

function showFrame() {
    if (show_frame) {
        for (let i = 0; i < nodes.length; i++) {
            reveal("#node-" + i);
            reveal("#link-" + i);
            reveal("#treeLabel-" + nodes[i].depth);
            revealBackJump(i);
        }
        counter = 1;
        treeRevealed = true;
    }
}

function showNode(i) {
    if(treeRevealed) {
        if (typeof coloredLimit === "undefined" || i < coloredLimit+1) {
            if (show_frame) {
                reveal("#text-"+ (i));
                reveal("#nodeLabel1-"+ (i));
                reveal("#edgeLabelLeft-" + i);
                reveal("#edgeLabelRight-"+ i);
                revealAll("#sideLabel-"+ (i));
            }
            d3.select("#link-" + i)
                .attr("stroke", "red")
                .attr("stroke-width", stroke_width*2);
        }
    }
    else {
        reveal("#link-" + i);
        reveal("#edgeLabelLeft-" + i);
        reveal("#edgeLabelRight-"+ i);
        reveal("#node-"+ i);
        reveal("#text-"+ i);
        reveal("#nodeLabel1-"+ i);
        reveal("#nodeLabel2-"+ i);
        revealAll("#sideLabel-"+ i);
        reveal("#treeLabel-" + nodes[i].depth);
    }
    revealBackJump(i);
}

function hideNode(i) {
    if(treeRevealed) {
        d3.select("#link-" + i)
            .attr("stroke", "black")
            .attr("stroke-width", stroke_width);
    }
    else {
        hide("#link-" + i);
        hide("#edgeLabelLeft-" + i);
        hide("#edgeLabelRight-"+ i);
        hide("#node-"+ i);
        hide("#text-"+ i);
        hide("#nodeLabel1-"+ i);
        hide("#nodeLabel2-"+ i);
        hideAll("#sideLabel-"+ i);
        hide("#jump-"+i)
    }
    hideBackJump(i);
}

function checkColorLimit() {
    if (show_frame) {
        return counter < coloredLimit+1;
    }
    return true;
}

function showTree() {
    if (animationOn) {
        pause();
    }
    for (counter; counter<nodes.length && checkColorLimit(); counter++) {
        showNode(counter);
    }
    if (!treeRevealed) {
        counter = 1;
    }
    treeRevealed = true;
}

function step() {
    if (animationOn) {
        pause();
    }
    if(counter < nodes.length && checkColorLimit()) {
        showNode(counter);
        counter++;
    }
}

function timeNodes() {
    if (show_frame && counter > coloredLimit) {
        pause();
    }
    else {
        if(counter < nodes.length && checkColorLimit()) {
            showNode(counter);
            counter++;
        }
        else {
            pause();
        }
    }
}

function animation() {
    if (animationOn) {
        pause();
    }
    else {
        if(counter < nodes.length) {
            document.getElementById("animation").innerHTML = "Pause";
            document.getElementById("animation").style.backgroundColor = "red";
            window.interval = setInterval(timeNodes, 500)
            animationOn = true;
        }
    }
}

function stepBack() {
    if (animationOn) {
        pause();
    }
    if(counter > 1) {
        counter--;
        hideNode(counter);
    }
}

function pause() {
    document.getElementById("animation").innerHTML = "Animation";
    document.getElementById("animation").style.backgroundColor = "";
    clearInterval(interval);
    animationOn = false;
}

function reset() {
    if (animationOn) {
        pause();
    }
    counter = 0;
    treeRevealed = false;
    d3.selectAll("svg").remove();
    init();
    nodeGap = 0;
    console.log(counter);
    animationOn = false;
}

function restoreUntil(startFrom, restoreLimit) {
    for(let i = startFrom; i < restoreLimit; i++) {
        step();
    }
}

function restore() {
    let restoreLimit = counter;
    let wasRevealed = treeRevealed;
    reset();
    if(wasRevealed) {
        showTree();
        restoreUntil(1, restoreLimit);
    }
    else {
        restoreUntil(0, restoreLimit);
    }
}

heightSlider.oninput = function() {
    tree_height = this.value*36;
    restore();
};

widthSlider.oninput = function() {
    tree_width = this.value*320;
    restore();
};

function saveTreeToPng() {
    html2canvas(document.body).then(function(canvas) {
        let image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        window.location.href=image;
    });
}

function showConfig() {
    if (cfg_shown) {
        document.getElementById("configFile").style.visibility = "hidden";
        document.getElementById("submit_button").style.visibility = "hidden";
        document.getElementById("help").style.visibility = "hidden";
        cfg_shown = false;
    }
    else {
        document.getElementById("configFile").style.visibility = "visible";
        document.getElementById("submit_button").style.visibility = "visible";
        document.getElementById("help").style.visibility = "visible";
        cfg_shown = true;
    }
}