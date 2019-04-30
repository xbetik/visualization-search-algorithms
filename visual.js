var node_size = 300;
var between_node_label_gap = 10;
var counter = 1;
var treeRevealed = false;
var nodes;
var links;
init();

function findNode(index) {
    for (var i=0;i<nodes.length;i++) {
        if (nodes[i].nodeOrder === index) {
            return nodes[i];
        }
    }
}

function getLinks(node, linksArray) {
    var j = 0;
    var src = 1;
    while (j !== nodes.length-1) {
        var target_node = findNode(src+1);
        var source_node = target_node.parent;
        linksArray.push( { source : source_node, target : target_node } );
        src++;
        j++;
    }
    return linksArray;
}

function init() {
    var canvas = d3.select("body").append("svg")
        .attr("width", 1200)
        .attr("height", 1200)
        .append("g")
        .attr("transform", "translate(50 ,50)");

    var tree = d3.layout.tree()
        .size([1000,1000]);

    var data = treeData;
    nodes = tree.nodes(data);

    var linksArray= [];
    links = getLinks(nodes[0], linksArray);

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
            .type(function(d) { return d.nodeType === "rectangle" ? "square" : "circle"}));


    node.append("text")
        .text(function (d) {return d.name; })
        .attr("id",function(d){return "text-"+d.id})
        .attr("visibility", "hidden")
        .attr("y" , 7)
        .attr("x", -30);

    node.append("text")
        .text(function(d) { return d.label; })
        .attr("id",function(d){return "nodeLabel-"+d.id})
        .attr("visibility", "hidden")
        .attr("text-anchor", "middle")
        .attr("y", node_size/between_node_label_gap);
}

function getNodeIndex(index) {
    for(var i=0; i<nodes.length; i++) {
        if(nodes[i].nodeOrder === index) {
            return i
        }
    }
}

function showNode(i) {
    if(treeRevealed) {
        d3.select("#link-" + i)
            .attr("stroke", "red")
            .attr("stroke-width", "5");
    }
    else {
        d3.select("#node-"+ i)
            .attr("visibility", "visible");
        d3.select("#text-"+ i)
            .attr("visibility", "visible");
        d3.select("#nodeLabel-"+ i)
            .attr("visibility", "visible");
        d3.select("#link-" + (i-1))
            .attr("visibility", "visible");

        var index = getNodeIndex(i);

        d3.select("#treeLabel-" + (nodes[index].depth-1))
            .attr("visibility", "visible");
    }
}

function showTree() {
    for (var i = counter; i<=nodes.length; i++) {
        showNode(i);
    }
    treeRevealed = true;
}

function step() {
    if(counter > nodes.length) {
        document.getElementById("errorArea").innerHTML = "End of the tree has been reached";
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

function animation() {
    window.interval = setInterval(timeNodes, 500)
}

function addTreeLabel(canvas) {
    nodes.forEach(function(d) { d.y = d.depth * 180; });
    var depthHash = _.uniq(_.pluck(nodes, "depth")).sort();
    depthHash.shift();
    var levelSVG = canvas.append("g")
        .attr("class", "levels-svg");
    levelSVG.selectAll("g.level")
        .data(depthHash)
        .enter()
        .append("g")
        .attr("class", "level")
        .attr("transform", function(d) { return "translate(" + 0 + "," + d*180 + ")"; })
        .append("text")
        .text(function(d){ return labels[d-1]; })
        .attr("id", function(d) { return "treeLabel-" + (d-1); })
        .attr("visibility", "hidden");
}

function reset() {
    d3.selectAll("svg").remove();
    init();
    counter = 1;
    treeRevealed = false;
}