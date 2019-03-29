var canvas = d3.select("body").append("svg")
    .attr("width", 1200)
    .attr("height", 1200)
    .append("g")
    .attr("transform", "translate(50 ,50)");

var tree = d3.layout.tree()
    .size([1000,1000]);

var circle_radius = 15;
var data = treeData;
var nodes = tree.nodes(data);
var links = tree.links(nodes);

function addSideLabel() {
    nodes.forEach(function(d) { d.y = d.depth * 180; });
    var depthHash = _.uniq(_.pluck(nodes, "depth")).sort();
    console.log("depthHash", depthHash)
    canvas.selectAll("g.levels-svg").remove();
    var levelSVG = canvas.append("g").attr("class", "levels-svg");
    var levels = levelSVG.selectAll("g.level");
    levels.data(depthHash)
        .enter().append("g")
        .attr("class", "level")
        .attr("transform", function(d) { return "translate(" + 0 + "," + d*180 + ")"; })
        .append("text")
        .text(function(d){
            return d;
        });
}

function showTree() {
    addSideLabel();

    var i = 0;

    canvas.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("id", function (d) {return d.source.id + " -> " + d.target.id;})
        .attr('x1', function (d) {return d.source.x;})
        .attr('x2', function (d) {return d.target.x;})
        .attr('y1', function (d) {return d.source.y;})
        .attr('y2', function (d) {return d.target.y;})
        .attr("stroke", "black")
        .attr("stroke-width", 1.5);

    var node = canvas.selectAll(".node")
        .data(nodes, function (d) {
            return d.id = ++i;
        })
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

    node.append("path")
        .style("stroke", "black")
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
        .attr("y" , circle_radius / 2)
        .attr("x", -30);
}


function stepByStep() {
    var nodes = tree.nodes(data);
    var links = tree.links(nodes);

    addSideLabel();

    var i = 0;
    var node = canvas.selectAll(".node")
        .data(nodes, function(d) { return d.id || (d.id = ++i); })
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; })
    node.append("circle")
        .attr("id",function(d){return "node-"+d.id})
        .attr("r", 10)
        .attr("fill", "steelblue");
    node.append("text")
        .text(function (d) { return d.name; });

    var diagonal = d3.svg.diagonal();

    canvas.selectAll(".link")
        .data(links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("fill", "none")
        .attr("stroke", "#ADADAD")
        .attr("d", diagonal)
    dft(data);
}

function visitElement(element,animX){
    d3.select("#node-"+element.id)
        .transition().duration(500).delay(500*animX)
        .style("fill","red").style("stroke","red");
}

function dft(data){
    var stack=[];
    var animX=0;
    stack.push(data);
    while(stack.length!==0){
        var element = stack.pop();
        visitElement(element,animX);
        animX=animX+1;
        if(element.children!==undefined){
            for(var i=0; i<element.children.length; i++){
                stack.push(element.children[element.children.length-i-1]);
            }
        }
    }
}

function reset() {
    d3.select("svg").remove();
}