var node_size = 300;
var tree_width = 1600;
var tree_height = 180;
var padding_x = 50;
var padding_y = 50;
var last_text_label_padding = 150;
var between_node_label_gap = 10;
var counter = 1;
var treeRevealed = false;
var animationOn = false;
var nodes;
var links;
var nodeGap = 0;

init();
dragElement(document.getElementById("infoPanel"));

function getTextWidth(text, font) {
    var canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
    var context = canvas.getContext("2d");
    context.font = font;
    var metrics = context.measureText(text);
    return metrics.width;
}

function getNode(index) {
    for (var i=0;i<nodes.length;i++) {
        if (nodes[i].nodeOrder === index) {
            return nodes[i];
        }
    }
    return -1;
}

function maxNumberOfNodeOrder() {
    var max = 0;
    for (var i=0;i<nodes.length;i++) {
        if (nodes[i].nodeOrder > max) {
            max = nodes[i].nodeOrder
        }
    }
    return max;
}

function getLinks(linksArray) {
    var src = 1;
    while (src !== maxNumberOfNodeOrder()) {
        var target = getNode(src+1);
        if (target !== -1) {
            var target_node = target;
            var source_node = target_node.parent;
            linksArray.push( { source : source_node, target : target_node } );
        }
        src++;
    }
    return linksArray;
}

function init() {
    var svg = d3.select("body").append("svg");
    var canvas = svg
        .attr("width", tree_width+padding_x+last_text_label_padding)
        .attr("height", padding_y + (tree_height*(labels.length+1)))
        .append("g")
        .attr("transform", "translate(" + padding_x + "," + padding_y + ")");

    var tree = d3.layout.tree()
        .size([tree_width]);

    var data = treeData;
    nodes = tree.nodes(data);

    var linksArray= [];
    links = getLinks(linksArray);

    addTreeLabel(canvas);

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

    var i = 0;
    var j = 0;

    canvas.selectAll(".link")
        .data(links, function(d) { return d.id = ++j; })
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

    j = 0;

    /*
    Padding on edge labels is pretty difficult, it rely on 2 characteristics of given edge
        1) if its right or left edge
        2) if its left or right label
     */
    canvas.selectAll(".edgeLabelsRight")
        .data(links, function(d) { return d.id = ++j; })
        .enter()
        .append("text")
        .attr("class", "edgeLabelsRight")
        .attr("id", function(d) { return "edgeLabelRight-"+d.id })
        .attr("y", function(d) { return d.target.y - ((d.target.y - d.source.y) / 2) })
        .attr("x", function(d) {
            var tiny_padding = 5; // so the label wont be on the edge but lil far from it
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
        .attr("visibility", "hidden");

    j = 0;
    canvas.selectAll(".edgeLabelsLeft")
        .data(links, function(d) { return d.id = ++j; })
        .enter()
        .append("text")
        .attr("class", "edgeLabelsLeft")
        .attr("id", function(d) { return "edgeLabelLeft-"+d.id })
        .attr("y", function(d) { return d.target.y - ((d.target.y - d.source.y) / 2)})
        .attr("x", function(d) {
            var word_padding = 0;
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
        //.attr("word-wrap", "break-word")
        .attr("visibility", "hidden");

    j=0;
    var node = canvas.selectAll(".node")
        .data(nodes, function (d) { return d.id = nodes[j++].nodeOrder; })
        .enter()
        .append("g")
        .attr("id", function(d) { return "g-node-" +d.id})
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

    node.append("path")
        .style("stroke", "black")
        .attr("visibility", "hidden")
        .attr("id",function(d){return "node-"+d.id})
        .style("fill", function(d) { return d.nodeColor === 'blank' ? "white" : d.nodeColor })
        .attr("d", d3.svg.symbol()
            .size(node_size)
            .type(function(d) { return d.shape === "rectangle" ? "square" : "circle"}));


    node.append("text")
        .attr("class", "nodeName")
        .text(function (d) {return d.name; })
        .attr("id",function(d){return "text-"+d.id})
        .attr("visibility", "hidden")
        .attr("y" , 7)
        .attr("x", -30);

    node.append("text")
        .attr("class", "label1")
        .text(function(d) { return d.label1; })
        .attr("id",function(d){return "nodeLabel1-"+d.id})
        .attr("visibility", "hidden")
        .attr("text-anchor", "middle")
        .attr("y", node_size/between_node_label_gap);

    addSideLabels();

    /*
    Because of the fact that doing node.append("text") I cannot append more than one text element i had to do external
    function which uses original "nodes" data and nodeOrder as a transformation index to current node elements
     */
    function addSideLabels() {
        for(var i=0;i<nodes.length;i++) {
            if (typeof nodes[i].sideLabels !== "undefined") {
                for(var j=0; j<nodes[i].sideLabels.length; j++) {
                    d3.select("#g-node-" + nodes[i].nodeOrder)
                        .append("text")
                        .attr("id","sideLabel-"+nodes[i].nodeOrder)
                        .attr("class", "sideLabels")
                        .attr("visibility", "hidden")
                        .text(nodes[i].sideLabels[j])
                        .attr("x", 20)
                        .attr("y", (j*18)+5);
                }
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

function showNode(i) {
    if(treeRevealed) {
        d3.select("#link-" + i)
            .attr("stroke", "red")
            .attr("stroke-width", "5");
    }
    else {
        reveal("#link-" + (i-1));
        reveal("edgeLabelLeft-" + (i-1));
        reveal("#edgeLabelRight-"+ (i-1));

        i = i + nodeGap;
        var j = 0;
        while (getNode(i) === -1 && i < maxNumberOfNodeOrder()) {
            i++;
            j++;
        }

        reveal("#node-"+ i);
        reveal("#text-"+ i);
        reveal("#nodeLabel1-"+ i);
        reveal("#nodeLabel2-"+ i);
        revealAll("#sideLabel-"+ i);
        //d3.selectAll(".sideLabel-6").attr("visibility", "visible");

        var node = getNode(i);
        if (node !== -1) {
            reveal("#treeLabel-" + (node.depth-1));
        }
        nodeGap+=j;
    }
}

function showTree() {
    for (var i = counter; i<=maxNumberOfNodeOrder(); i++) {
        showNode(i);
    }
    treeRevealed = true;
    counter = 1;
}

function step() {
    if (animationOn) {
        pause();
    }
    if(counter > nodes.length) {
        //document.getElementById("errorArea").innerHTML = "End of the tree has been reached";
    }
    else {
        showNode(counter);
        counter++
    }
}

function pause() {
    clearInterval(interval);
}

function timeNodes() {
    if(counter > nodes.length-1){
        pause();
    }
    showNode(counter);
    counter++;
}

function switchButton()
{
    var elem = document.getElementById("animation");
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
    var depthHash = _.uniq(_.pluck(nodes, "depth")).sort();
    depthHash.shift();
    var levelSVG = canvas.append("g")
        .attr("class", "levels-svg");
    levelSVG.selectAll("g.level")
        .data(depthHash)
        .enter()
        .append("g")
        .attr("class", "level")
        .attr("transform", function(d) { return "translate(" + 0 + "," + d*tree_height + ")"; })
        .append("text")
        .text(function(d){ return labels[d-1]; })
        .attr("id", function(d) { return "treeLabel-" + (d-1); })
        .attr("visibility", "hidden");
}

function reset() {
    d3.selectAll("svg").remove();
    init();
    nodeGap = 0;
    counter = 1;
    treeRevealed = false;
}

var heightSlider = document.getElementById("heightSlider");
var widthSlider = document.getElementById("widthSlider");

function restoreTree(restoreUntil) {
    for(var i=1; i < restoreUntil; i++) {
        step();
    }
}

function restore() {
    var restoreUntil = counter;
    var wasRevealed = treeRevealed;
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
        //document.body.appendChild(canvas);
        var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        window.location.href=image;
    });
}

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(elmnt.id + "header")) {
        /* if present, the header is where you move the DIV from:*/
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    } else {
        /* otherwise, move the DIV from anywhere inside the DIV:*/
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        /* stop moving when mouse button is released:*/
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

function infoIncrease() {
    document.getElementById("description").style.fontSize = "x-large";
}

function infoDecrease() {
    document.getElementById("description").style.fontSize = "small";
}

function infoDefault() {
    document.getElementById("description").style.fontSize = "medium";
}
