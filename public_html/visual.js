const node_size = 400;
const padding_x = 50;
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
let counter = 1;

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
}

function getTextWidth(text, font) {
    let canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
    let context = canvas.getContext("2d");
    context.font = font;
    let metrics = context.measureText(text);
    return metrics.width;
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
        .attr("stroke-width", 1.5)
        .attr("stroke-dasharray", function(d) { return d.target.dashLine === "yes" ? ("3, 3") : ("0, 0")})
        .attr("visibility", "hidden")
        .attr("marker-end", function(d) { return d.target.arrowToNode === "yes" ? "url(#arrowToNode)" : "url()"})
        .attr("marker-start", function(d) { return d.target.arrowFromNode === "yes" ? "url(#arrowFromNode)" : "url()"});
}

function addRightEdgeLabels(canvas) {
    let id_counter = 0;
    canvas.selectAll(".edgeLabelsRight")
        .data(links, function(d) { return d.id = ++id_counter; })
        .enter()
        .append("text")
        .attr("class", "edgeLabelsRight")
        .attr("id", function(d) { return "edgeLabelRight-"+d.id })
        .attr("y", function(d) { return d.target.y - ((d.target.y - d.source.y) / 2) })
        .attr("x", function(d) {
            let tiny_padding = 5; // so the label wont be on the edge but lil far from it
            if(d.source.x > d.target.x) {
                return d.source.x - ((d.source.x-d.target.x)/2) + tiny_padding;
            }
            else if(d.source.x < d.target.x) {
                return d.target.x - ((d.target.x-d.source.x)/2) + tiny_padding;
            }
            else {
                return d.target.x + tiny_padding;
            }
        })
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
        .attr("x", function(d) {
            let word_padding = 0;
            if(typeof d.target.edgeLabelLeft !== "undefined") {
                word_padding = getTextWidth(d.target.edgeLabelLeft, "8pt monospace")
            }
            if(d.source.x > d.target.x) {
                return d.source.x - ((d.source.x-d.target.x)/2) - word_padding;
            }
            else if(d.source.x < d.target.x) {
                return d.target.x - ((d.target.x-d.source.x)/2) - word_padding - 20;
            }
            else {
                return d.target.x - word_padding; // adding a constant 8 to balance middle label a bit
            }
        })
        .attr("width", "100px")
        .text(function(d) { return d.target.edgeLabelLeft; })
        .style("overflow", "hidden")
        .attr("visibility", "hidden")
        .attr("font-weight", "bold");
}

function addNodes(canvas) {
    let id_counter = 0;
    let node = canvas.selectAll(".node")
        .data(nodes, function (d) { return d.id = nodes[id_counter++].nodeOrder; })
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
            .size(node_size)
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
            "y" : 5,
            "x" : -4,
            "font-weight" : "bold"
        });
}

function addBottomLabel(node) {
    node.append("text")
        .attr("class", "label1")
        .text(function(d) { return d.label1; })
        .attr({
            "id" : function(d) { return "nodeLabel1-"+d.id; },
            "visibility" : "hidden",
            "text-anchor" : "middle",
            "y" : node_size/between_node_label_gap,
            "font-weight" : "bold",
        });
}

/*
Because of the fact that doing node.append("text") I cannot append more than one text element i had to do external
function which uses original "nodes" data and nodeOrder as a transformation index to current node elements
 */
function addSideLabels() {
    for(let i=0;i<nodes.length;i++) {
        if (typeof nodes[i].sideLabels !== "undefined") {
            for(let j=0; j<nodes[i].sideLabels.length; j++) {
                d3.select("#g-node-" + nodes[i].nodeOrder)
                    .append("text")
                    .attr("id","sideLabel-"+nodes[i].nodeOrder)
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

function hideNode(i) {
    if(treeRevealed) {
        d3.select("#link-" + i)
            .attr("stroke", "black")
            .attr("stroke-width", 1.5);
    }
    else {
        hide("#link-" + (i-1));
        hide("#edgeLabelLeft-" + (i-1));
        hide("#edgeLabelRight-"+ (i-1));
        hide("#node-"+ i);
        hide("#text-"+ i);
        hide("#nodeLabel1-"+ i);
        hide("#nodeLabel2-"+ i);
        hideAll("#sideLabel-"+ i);
    }
}

function showNode(i) {
    if(treeRevealed) {
        d3.select("#link-" + i)
            .attr("stroke", "red")
            .attr("stroke-width", "5");
    }
    else {
        reveal("#link-" + (i-1));
        reveal("#edgeLabelLeft-" + (i-1));
        reveal("#edgeLabelRight-"+ (i-1));
        reveal("#node-"+ i);
        reveal("#text-"+ i);
        reveal("#nodeLabel1-"+ i);
        reveal("#nodeLabel2-"+ i);
        revealAll("#sideLabel-"+ i);

        let node = getNode(i);
        if (node !== -1) {
            reveal("#treeLabel-" + (node.depth-1));
        }
    }
}

function showTree() {
    for (let i = counter; i<=nodes.length; i++) {
        showNode(i);
    }
    treeRevealed = true;
    counter = 1;
}

function step() {
    if (animationOn) {
        pause();
    }
    if(counter <= nodes.length) {
        showNode(counter);
        counter++;
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
    clearInterval(interval);
}

function timeNodes() {
    if(counter <= nodes.length) {
        showNode(counter);
        counter++;
    }
    else {
        pause();
    }
}

function switchButton() {
    let elem = document.getElementById("animation");
    if (elem.innerHTML === "Animation") {
        elem.innerHTML = "Pause";
        elem.style.backgroundColor = "red";
    }
    else {
        elem.innerHTML = "Animation";
        elem.style.backgroundColor = "";
    }
}

function animation() {
    switchButton();
    if (animationOn) {
        animationOn = false;
        pause();
    }
    else {
        animationOn = true;
        window.interval = setInterval(timeNodes, 500)
    }
}

function addTreeLabel(canvas) {
    nodes.forEach(function(d) { d.y = d.depth * tree_height; });
    let depthHash = _.uniq(_.pluck(nodes, "depth")).sort();
    depthHash.shift();
    let levelSVG = canvas.append("g")
        .attr("class", "levels-svg");
    levelSVG.selectAll("g.level")
        .data(depthHash)
        .enter()
        .append("g")
        .attr("class", "level")
        .attr("transform", function(d) { return "translate(" + 0 + "," + d*tree_height + ")"; })
        .append("text")
        .text(function(d){ return labels[d-1]; })
        .attr({
            "id" : function(d) { return "treeLabel-" + (d-1); },
            "visibility" : "hidden",
            "font-weight" : "bold",
            "font-size" : "30px",
            "font-family" : "monospace"
        });
}

function reset() {
    d3.selectAll("svg").remove();
    init();
    nodeGap = 0;
    counter = 1;
    treeRevealed = false;
}

function restoreTree(restoreUntil) {
    for(let i=1; i < restoreUntil; i++) {
        step();
    }
}

function restore() {
    let restoreUntil = counter;
    let wasRevealed = treeRevealed;
    reset();
    if(wasRevealed) {
        showTree();
    }
    else {
        restoreTree(restoreUntil);
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