const padding_x = 250;
const padding_y = 90;
const most_right_label_padding = 150;
const most_down_label_padding = 50;
const between_node_label_gap = 13;
let tree_width = 960;
let tree_height = 180;
let treeRevealed = false;
let animationOn = false;
let nodes;
let links;
let nodeGap = 0;
let cfg_shown = false;
let firstItem, lastItem;
let counter;
let node_size = 400,stroke_width=1.5,coloredLimit=null,show_frame=false,animation_speed=500;

/* #AdditionalVariableTag. This tag marks the place where additional constants will be placed. DO NOT REMOVE IT */
init();

/**
 * Initialize the visualization including the svg and its elements (nodes, links etc.)
 */
function init() {
    let svg = d3.select("body").append("svg");
    let canvas = svg.attr({
        "width" : tree_width+padding_x+most_right_label_padding,
        "height" : padding_y + (tree_height*(labels.length+1)) + most_down_label_padding
    })
        .append("g")
        .attr("class", "allObjects")
        .attr("transform", "translate(" + padding_x + "," + padding_y + ")");

    let tree = d3.layout.tree()
        .size([tree_width]);

    nodes = tree.nodes(treeData);
    links = createLinks();
    // Normalize the depth
    nodes.forEach(function(d) { d.y = d.depth * tree_height; });

    firstItem = getFirstItem();
    lastItem = getLastItem();
    counter = firstItem;

    addTreeLabel(canvas);
    addMarkers(svg);
    addLinks(canvas);
    addEdgeLabels(canvas);
    let node = addNodes(canvas);
    addNodeShape(node);
    addNodeName(node);
    addBottomLabel(node);
    addSideLabels();
    addJumps(svg);
    showFrame();
}

/**
 * Get the index of the first node (or action)
 * @returns {number} min Index of first item
 */
function getFirstItem() {
    let min = 100;
    nodes.forEach(function(d) {
        if (typeof d.actionOrder !== "undefined") {
            if (Math.min(d.nodeOrder, d.actionOrder) < min) {
                min = Math.min(d.nodeOrder, d.actionOrder);
            }
        }
        else {
            if (d.nodeOrder < min) {
                min = d.nodeOrder;
            }
        }
    });
    return min;
}

/**
 * Get the index of the last node (or action)
 * @returns {number} max Index of last item
 */
function getLastItem() {
    let max = -1;
    nodes.forEach(function(d) {
        if (typeof d.actionOrder !== "undefined") {
            if (Math.max(d.nodeOrder, d.actionOrder) > max) {
                max = Math.max(d.nodeOrder, d.actionOrder);
            }
        }
        else {
            if (d.nodeOrder > max) {
                max = d.nodeOrder;
            }
        }
    });
    return max;
}

/**
 * Adds jumps to canvas. The source of the jump is the current node. The target is the node with the given nodeOrder.
 * @param {svg} svg Canvas of elements
 */
function addJumps(svg) {
    var lineFunction = d3.svg.line()
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; })
        .interpolate("basis");

    for (let i = 0; i < nodes.length; i++) {
        if (typeof nodes[i].jump !== "undefined") {
            let source_x = nodes[i].x;
            let source_y = nodes[i].y;
            let target_x = getNode(nodes[i].jump).x;
            let target_y = getNode(nodes[i].jump).y;
            svg.append("path")
                .attr("id", function() {
                    return typeof nodes[i].actionOrder !== "undefined" ? "jump-" + nodes[i].actionOrder : "jump-" + (nodes[i].nodeOrder+1);
                })
                .attr("stroke-width", "3px")
                .attr("fill", "none")
                .attr("stroke", "black")
                .attr("d", lineFunction([
                    { "x" : source_x, "y" : source_y-10 },
                    { "x" : source_x+20, "y" : source_y - (source_y-target_y/2) + 100 },
                    { "x" : target_x+(source_x<target_x ? -4 : 4), "y" : target_y }
                ]))
                .attr("transform", "translate(" + padding_x + "," + padding_y + ")")
                .attr("visibility", "hidden")
                .attr("stroke-dasharray", ("3, 3"))
                .attr("marker-end", "url(#arrowToNode)");
        }
    }
}

/**
 * Gets a node with given order.
 * @param {number} order Timestamp of the node represented by nodeOrder attribute
 * @returns {null|Object} {null|node}
 */
function getNode(order) {
    for (let i=0;i<nodes.length;i++) {
        if (nodes[i].nodeOrder === order) {
            return nodes[i];
        }
    }
    return null;
}

/**
 * Creates array of links. Each link is defined by source node and target node.
 * @returns {Array.<Object>}
 */
function createLinks() {
    let links = [];
    for(let i=1; i < nodes.length; i++) {
        links.push( { source : nodes[i].parent, target : nodes[i] } );
    }
    return links;
}

/**
 * Adds marker definitions.
 * @param {svg} svg Canvas of elements
 */
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

/**
 * Adds links to canvas. SVG element line is used for link representation. Several properties of the link are justified.
 * @param {svg} canvas Canvas of elements
 */
function addLinks(canvas) {
    let i = 1;
    let links_group = canvas.append("g")
        .attr("class", "links");
    links_group.selectAll(".link")
        .data(links, function(d) { return d.id = nodes[i++].nodeOrder; })
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("id", function (d) {return "link-"+d.id})
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

/**
 * Counts the position of left edge label
 * @param {Object} line Link between node1 and node2 defined as { source: node1, target: node2 }
 * @returns {number} The position of the left edge label
 */
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

/**
 * Counts the position of right edge label
 * @param {Object} line Link between node1 and node2 defined as { source: node1, target: node2 }
 * @returns {number} The position of the right edge label
 */
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

/**
 * Adds edge labels. The edge label is represented by SVG element text.
 * @param {svg} canvas Canvas of elements
 */
function addEdgeLabels(canvas) {
    let edgeLabels = canvas.append("g")
        .attr("class", "edgeLabels")
        .attr("font-weight", "bold");
    links.forEach(function(d) {
       if (typeof d.target.edgeLabelRight !== "undefined") {
           edgeLabels.append("text")
               .attr("id", typeof d.target.actionOrder !== "undefined" ? "edgeLabelLeft-" + d.target.actionOrder : "edgeLabelLeft-" + d.target.nodeOrder)
               .attr("y", d.target.y - ((d.target.y - d.source.y) / 2))
               .attr("x", countRightLabelShift(d))
               .text(d.target.edgeLabelRight)
               .attr("visibility", "hidden")
       }
       if (typeof d.target.edgeLabelLeft !== "undefined") {
           edgeLabels.append("text")
               .attr("id", typeof d.target.actionOrder !== "undefined" ? "edgeLabelRight-" + d.target.actionOrder : "edgeLabelRight-" + d.target.nodeOrder)
               .attr("y", d.target.y - ((d.target.y - d.source.y) / 2))
               .attr("x", countLeftLabelShift(d))
               .text(d.target.edgeLabelLeft)
               .attr("visibility", "hidden")
       }
    });
}

/**
 * Creates a group for nodes and a selection which represents a reference to all the nodes.
 * @param {svg} canvas Canvas of elements
 * @returns {Object} node Selection of all the nodes.
 */
function addNodes(canvas) {
    let i = 0;
    return canvas.selectAll(".node")
        .data(nodes, function (d) { return d.id = nodes[i++].nodeOrder; })
        .enter()
        .append("g")
        .attr("id", function(d) { return "g-node-" +d.id})
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
}

/**
 * Adds nodes and specifies the shape using SVG element path.
 * @param {Object} node Selection of nodes.
 */
function addNodeShape(node) {
    node.append("path")
        .style("stroke", "black")
        .attr("visibility", "hidden")
        .attr("id",function(d){return "node-"+d.id})
        .style("fill", function(d) { return d.nodeColor === 'blank' ? "white" : d.nodeColor })
        .attr("d", d3.svg.symbol()
            .size(function() { return node_size})
            .type(function(d) { return d.shape === "rectangle" ? "square" : "circle"}));
}

/**
 * Adds node labels representing domain values using SVG element text.
 * @param {Object} node Selection of nodes
 */
function addNodeName(node) {
    node.append("text")
        .attr("class", "nodeName")
        .text(function (d) {return d.name; })
        .attr("id",function(d){return "text-"+d.id})
        .attr("visibility", "hidden")
        .style("fill", function(d) { return typeof d.nodeColor === "undefined" ? "white" : "black" })
        .attr({
            "text-anchor" : "middle",
            "y" : 7,
            "font-weight" : "bold"
        });
}

/**
 * Adds node bottom labels representing the constraints causing the inconsistency. Using SVG element text.
 * @param {Object} node
 */
function addBottomLabel(node) {
    node.append("text")
        .attr("class", "nodeLabel")
        .text(function(d) { return d.nodeLabel; })
        .attr({
            "id" : function(d) { return "nodeLabel1-"+d.id; },
            "visibility" : "hidden",
            "text-anchor" : "middle",
            "y" : function() { return node_size/between_node_label_gap},
            "font-weight" : "bold",
        });
}

/**
 * Adds node side labels representing the updated domains after forward-check/full look-ahead. Using SVG element text.
 */
function addSideLabels() {
    for(let i=0;i<nodes.length;i++) {
        if (typeof nodes[i].sideLabels !== "undefined") {
            for(let j=0; j<nodes[i].sideLabels.length; j++) {
                d3.select("#g-node-" + nodes[i].nodeOrder)
                    .append("text")
                    .attr("id","sideLabel-"+ nodes[i].nodeOrder)
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

/**
 * Adds tree labels representing CSP variables.
 * @param {svg} canvas Canvas of elements.
 */
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

/**
 * Reveals an element with given ID.
 * @param {string} element ID of element
 */
function reveal(element) {
    d3.select(element).attr("visibility", "visible");
}

/**
 * Reveals all the elements with given ID
 * @param {string} element ID of element
 */
function revealAll(element) {
    d3.selectAll(element).attr("visibility", "visible");
}

/**
 * Hide an element with given ID
 * @param {string} element ID of element
 */
function hide(element) {
    d3.select(element).attr("visibility", "hidden");
}

/**
 * Hide all the elements with given ID
 * @param {string} element ID of element
 */
function hideAll(element) {
    d3.selectAll(element).attr("visibility", "hidden");
}

/**
 * Reveals all the items. Represents graph skeleton for incomplete search algorithms.
 */
function showFrame() {
    if (show_frame) {
        for (let i = firstItem; i <= lastItem; i++) {
            reveal("#node-" + i);
            reveal("#link-" + i);
            if (getNode(i) != null) {
                reveal("#treeLabel-" + getNode(i).depth);
            }
        }
        counter = 2;
        treeRevealed = true;
    }
}

/**
 * Checks if the number of colored nodes exceed the total allowed.
 * @returns {boolean} False if limit of colored nodes exceeds, True otherwise.
 */
function checkColorLimit() {
    if (coloredLimit !== null) {
        return counter < coloredLimit+1;
    }
    return true;
}

/**
 * Represents one step in the animation. Reveals all the elements with given index i.
 * @param {number} i Index of elements to be revealed.
 */
function showElements(i) {
    if(treeRevealed) {
        if (checkColorLimit()) {
            reveal("#text-"+ (i));
            reveal("#nodeLabel1-"+ (i));
            reveal("#edgeLabelLeft-" + i);
            reveal("#edgeLabelRight-"+ i);
            revealAll("#sideLabel-"+ (i));
            d3.select("#link-" + i)
                .attr("stroke", "red")
                .attr("stroke-width", stroke_width*2);
            d3.select("#jump-" + i)
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
        reveal("#jump-" + i)
        revealAll("#sideLabel-"+ i);
        if (getNode(i) != null) {
            reveal("#treeLabel-" + getNode(i).depth);
        }
    }
}

/**
 * Represents step backward in the animation. Hide all the elements with given index i.
 * @param {number} i Index of elements to be revealed.
 */
function hideNode(i) {
    if (treeRevealed) {
        if (show_frame) {
            hide("#edgeLabelRight-"+ i);
            hide("#edgeLabelLeft-"+ i);
        }
        d3.select("#link-" + i)
            .attr("stroke", "black")
            .attr("stroke-width", stroke_width);
        d3.select("#jump-" + i)
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
}

/**
 * Reveals the whole tree (performs all the steps at once). Corresponds to ShowTree button.
 */
function showTree() {
    if (animationOn) {
        pause();
    }
    for (counter; counter<=lastItem && checkColorLimit(); counter++) {
        showElements(counter);
    }
    if (!treeRevealed) {
        counter = firstItem+1;
    }
    treeRevealed = true;
}

/**
 * Performs one step of the animation. Corresponds to Step button.
 */
function step() {
    if (animationOn) {
        pause();
    }
    if(counter <= lastItem && checkColorLimit()) {
        showElements(counter);
        counter++;
    }
}

/**
 *  Looping function used in animation. Performs one step every 500 milliseconds (default).
 */
function timeNodes() {
    if (!checkColorLimit()) {
        pause();
    }
    else {
        if(counter <= lastItem && checkColorLimit()) {
            showElements(counter);
            counter++;
        }
        else {
            pause();
        }
    }
}

/**
 * Represents an animation. External function timeNodes() used as a looping function inside the setInterval command.
 * Corresponds to button Animation.
 */
function animation() {
    if (animationOn) {
        pause();
    }
    else {
        if(counter <= lastItem) {
            document.getElementById("animation").innerHTML = "Pause";
            document.getElementById("animation").style.backgroundColor = "red";
            window.interval = setInterval(timeNodes, animation_speed);
            animationOn = true;
        }
    }
}

/**
 * Performs one step backward. Corresponds to StepBack.
 */
function stepBack() {
    if (animationOn) {
        pause();
    }
    if(counter > 2) {
        counter--;
        hideNode(counter);
    }
}

/**
 * Pauses the animation. Corresponding to Pause button which is displayed when the animation is on.
 */
function pause() {
    document.getElementById("animation").innerHTML = "Animation";
    document.getElementById("animation").style.backgroundColor = "";
    clearInterval(interval);
    animationOn = false;
}

/**
 * Resets the visualization. Removes and re-initializes the svg.
 */
function reset() {
    if (animationOn) {
        pause();
    }
    treeRevealed = false;
    d3.selectAll("svg").remove();
    init();
    nodeGap = 0;
    animationOn = false;
}

/**
 * Restores the original graph partially.
 * @param {number} restoreLimit The index of the last revealed element of the original graph.
 */
function restoreUntil(restoreLimit) {
    for(let i = firstItem; i < restoreLimit; i++) {
        step();
    }
}

/**
 * Restore the visualization to original state. This function is used if the height and width of the graph is adjusted and the graph needs to be re-generated.
 */
function restore() {
    let restoreLimit = counter;
    let wasRevealed = treeRevealed;
    reset();
    if(wasRevealed) {
        if (!show_frame) {
            showTree();
        }
        restoreUntil(restoreLimit-1);
    }
    else {
        restoreUntil(restoreLimit);
    }
}

/**
 * Adjusts the height of the graph. Corresponds to height range bar.
 */
heightSlider.oninput = function() {
    tree_height = this.value*36;
    restore();
};

/**
 * Adjusts the width of the graph. Corresponds to width range bar.
 */
widthSlider.oninput = function() {
    tree_width = this.value*320;
    restore();
};

/**
 * Saves canvas to PNG. This function requires library html2canvas.min.js. Corresponds to button SavePNG.
 */
function saveTreeToPng() {
    html2canvas(document.body).then(function(canvas) {
        let image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        window.location.href=image;
    });
}

/**
 * Shows the config file with an option to modify the file and re-generate the visualization. Corresponds to button ShowConfig.
 */
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