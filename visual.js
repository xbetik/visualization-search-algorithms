var node_size = 300;
var tree_width = 1000;
var tree_height = 180;
var padding_x = 50;
var padding_y = 50;
var between_node_label_gap = 10;
var counter = 1;
var treeRevealed = false;
var animationOn = false;
var nodes;
var links;
var nodeGap = 0;
init();

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
        .attr("width", tree_width+padding_x)
        .attr("height", tree_height*5)
        .append("g")
        .attr("transform", "translate(" + padding_x + "," + padding_y + ")");

    let dfs = svg.append("defs");

    dfs.append("marker")
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

    dfs.append("marker")
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

    var tree = d3.layout.tree()
        .size([tree_width]);

    var data = treeData;
    nodes = tree.nodes(data);

    var linksArray= [];
    links = getLinks(linksArray);

    addTreeLabel(canvas);

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
        .attr("visibility", "hidden")
        .attr("marker-end", function(d) { return d.target.arrowToNode === "yes" ? "url(#arrowToNode)" : "url()"})
        .attr("marker-start", function(d) { return d.target.arrowFromNode === "yes" ? "url(#arrowFromNode)" : "url()"});

    j = 0;
    canvas.selectAll(".edgeLabelsRight")
        .data(links, function(d) { return d.id = ++j; })
        .enter()
        .append("text")
        .attr("class", "edgeLabelsRight")
        .attr("id", function(d) { return "edgeLabelRight-"+d.id })
        .attr("y", function(d) { return d.target.y - ((d.target.y - d.source.y) / 2) })
        .attr("x", function(d) { return d.target.x })
        .text(function(d) { return d.target.edgeLabelRight; })
        .attr("visibility", "hidden");

    j = 0;
    canvas.selectAll(".edgeLabelsLeft")
        .data(links, function(d) { return d.id = ++j; })
        .enter()
        .append("text")
        .attr("class", "edgeLabelsLeft")
        .attr("id", function(d) { return "edgeLabelLeft-"+d.id })
        .attr("y", function(d) { return d.target.y - ((d.target.y - d.source.y) / 2) })
        .attr("x", function(d) { return d.target.x - 50})
        .text(function(d) { return d.target.edgeLabelLeft; })
        .attr("visibility", "hidden");

    j=0;
    var node = canvas.selectAll(".node")
        .data(nodes, function (d) { return d.id = nodes[j++].nodeOrder; })
        .enter()
        .append("g")
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

    node.append("text")
        .attr("class", "label2")
        .text(function(d) { return d.label2; })
        .attr("id",function(d){return "nodeLabel2-"+d.id})
        .attr("visibility", "hidden")
        .style("font-size", "15px")
        .attr("x", 10)
        .attr("y", 7);
}

function showNode(i) {
    if(treeRevealed) {
        d3.select("#link-" + i)
            .attr("stroke", "red")
            .attr("stroke-width", "5");
    }
    else {
        d3.select("#link-" + (i-1))
            .attr("visibility", "visible");

        i = i + nodeGap;
        var j = 0;
        while (getNode(i) === -1 && i < maxNumberOfNodeOrder()) {
            i++;
            j++;
        }

        d3.select("#node-"+ i)
            .attr("visibility", "visible");
        d3.select("#text-"+ i)
            .attr("visibility", "visible");
        d3.select("#nodeLabel1-"+ i)
            .attr("visibility", "visible");
        d3.select("#nodeLabel2-"+ i)
            .attr("visibility", "visible");
        d3.select("#edgeLabelLeft-"+ i)
            .attr("visibility", "visible");
        d3.select("#edgeLabelRight-"+ i)
            .attr("visibility", "visible");

        var node = getNode(i);
        if (node !== -1) {
            d3.select("#treeLabel-" + (node.depth-1))
                .attr("visibility", "visible");
        }
        nodeGap+=j;
    }
}

function showTree() {
    for (var i = counter; i<=maxNumberOfNodeOrder(); i++) {
        showNode(i);
    }
    treeRevealed = true;
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

heightSlider.oninput = function() {
    tree_height = this.value*90;
    //document.getElementById("area").innerHTML = "height: " + tree_height + " width: " + tree_width + " canvas: " + tree_height*5 + " " + tree_width;
    reset();
    showTree();
};

widthSlider.oninput = function() {
    tree_width = this.value*300;
    //document.getElementById("area").innerHTML = "height: " + tree_height + " width: " + tree_width + " canvas: " + tree_height*5 + " " + tree_width;
    reset();
    showTree();
};
