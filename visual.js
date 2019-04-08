var circle_radius = 15;
var counter = 1;
var depth = 0;
init();


function getLinks(node, linksArray) {
    if (node.children !== undefined) {
        for (var i=0; i<node.children.length; i++) {
            linksArray.push( { source : node, target : node.children[i] } );
            getLinks(node.children[i], linksArray);
        }
        return linksArray;
    }
    return [];
}

function init() {
    window.canvas = d3.select("body").append("svg")
        .attr("width", 1200)
        .attr("height", 1200)
        .append("g")
        .attr("transform", "translate(50 ,50)");

    window.tree = d3.layout.tree()
        .size([1000,1000]);

    window.data = treeData;
    window.nodes = tree.nodes(data);

    var linksArray= [];
    window.links = getLinks(nodes[0], linksArray);

    addSideLabel();

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
        .data(nodes, function (d) { return d.id = ++j; })
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
        .style("fill", function(d) { if (d.color === 'red') return "red";
        else if (d.color === 'blank') { return "white"; }
        else { return "black"; }})
        .attr("d", d3.svg.symbol()
            .size(300)
            .type(function(d) { if (d.type === 'rectangle') return "square";
            else { return "circle"; }
            }));

    node.append("text")
        .text(function (d) {return d.name; })
        .attr("id",function(d){return "text-"+d.id})
        .attr("visibility", "hidden")
        .attr("y" , circle_radius / 2)
        .attr("x", -30);

    node.append("text")
        .text(function(d) { return d.constraintLabel; })
        .attr("id",function(d){return "con-"+d.id})
        .attr("visibility", "hidden")
        .attr("x" , -13)
        .attr("y", 25);
}

function showNode(i) {
    d3.select("#node-"+ i)
        .attr("visibility", "visible");
    d3.select("#text-"+ i)
        .attr("visibility", "visible");
    d3.select("#con-"+ i)
        .attr("visibility", "visible");
    d3.select("#link-" + (i-1))
        .attr("visibility", "visible");

    if(nodes[i-1].depth !==0 && nodes[i-1].depth > depth) {
        d3.select("#label-" + (depth))
            .attr("visibility", "visible");
        depth++;
    }
}

function step() {
    if(counter <= nodes.length) {
        showNode(counter);
        counter++;
    }
    else {
        console.log(counter);
        console.log(nodes.length);
    }
}

function addSideLabel() {
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
        .attr("id", function(d) { return "label-" + (d-1); })
        .attr("visibility", "hidden");
}

function showTree() {
    for (var i = counter; i<=nodes.length; i++) {
        showNode(i);
    }
}

function animation() {
    for (var i = counter; i<=nodes.length; i++) {
        d3.select("#node-"+ i)
            .attr("visibility", "visible")
            .transition().duration(500).delay(500*i)
            .style("stroke","green");

        d3.select("#text-"+ i)
            .attr("visibility", "visible")
            .transition().duration(500).delay(500*i)
            .style("fill","green").style("stroke","green");

        d3.select("#link-" + (i-1))
            .attr("visibility", "visible")
            .transition().duration(500).delay(500*i)
            .attr('stroke-width', '7')
            .style("fill","green").style("stroke","green")


        if(nodes[i-1].depth !==0 && nodes[i-1].depth > depth) {
            d3.select("#label-" + (depth))
                .attr("visibility", "visible");
            depth++;
        }
    }
}

function reset() {
    d3.selectAll("svg").remove();
    init();
    counter = 1;
}