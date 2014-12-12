import json
import webbrowser
import os.path

class Process():
    def __init__(self, pid):
        self.pid = pid
        self.files = {}
        self.name = 'Unknown'

    def set_name(self, name):
        self.name = name

    def add_file_access(self, filename, rwx):
        i = 0
        if rwx == 'r':
            i = 0
        elif rwx == 'w':
            i = 1
        elif rwx == 'x':
            i = 2
        if filename in self.files:
            self.files[filename][i] = rwx
        else:
            accesses = ['-', '-', '-']
            accesses[i] = rwx
            self.files[filename] = accesses


html = ["""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Bipartite Graph</title>
</head>
<body>
  <script src="d3.min.js"></script>

  <script>

  // define global variables
  var width = 1200;
  var height = 1200;
  var radius = 20;
  var xcoords = [200, 600]; // x-coordinates of columns

  var body = d3.select("body");
  var svg = body.append("svg")
                .attr("height", height)
                .attr("width", width);

  // setup containers
  var group = svg.append("g")
              .classed("column", true);
  var hovercolor = "#088A08";

  var jsonCircles = """, '', ";\n  var edges = ", '', """;

  function plotGraph(data) {
    // bind valid data to a d3 selection
    var nodes = group.selectAll(".node")
      .data(data, function(d){
        return d.name;
      });

    // draw nodes
    nodes.enter()
      .append("circle")
      .attr("class", function(d, i) {
        return "node node" + d.column + "_" + i;
      })
      .attr("r", radius)
      .attr("cx", function(d) {
        return xcoords[d.column];
      })
      .attr("cy", function(d, i) {
        return (i+1)*100;
      })
      .style("fill", "#000000")
      .on('mouseover', function(d) {
        d3.select(this).style("fill", hovercolor);
        d3.selectAll(".edge" + d.column + "_" + d.id).style("stroke", hovercolor);
        for (var i = 0; i < d.adjacencies.length; i++) {
          d3.select(".node" + (d.column == 1 ? 0 : 1) + "_" + d.adjacencies[i]).style("fill", hovercolor);
        }
       })
      .on('mouseout', function(d) {
        d3.selectAll(".node").style("fill", "#000000");
        d3.selectAll(".edge").style("stroke", "#000000");
      });
    svg.selectAll(".text").data(data).enter().append("text")
            .style("font-size",12)
            .style("text-anchor", function(d) { return d.column == 0 ? "end" : "left"; })
            .style("fill", function(d) { return d.column == 0 ? "#0000FF" : "#B40404"; })
            .attr("x", function(d) { return xcoords[d.column] + (d.column == 0 ? -1 : 1) * 25; })
            .attr("y", function(d, i) { return (i+1)*100 + 5; })
            .text(function(d) { return d.name; });

  }

  function plotEdges(data) {
    var edges = group.selectAll(".edge")
      .data(data, function(d){
        return jsonCircles[0][d.source].name + "_" + jsonCircles[1][d.target].name;
      });

    // draw edges
    edges.enter()
      .append("line")
      .attr("class", function(d, i) {
        return "edge edge" + "0_" + d.source + " " + "edge" + "1_" + d.target;
      })
      .attr("x1", function(d) {
        return xcoords[0];
      })
      .attr("y1", function(d, i) {
        return (d.source+1)*100;
      })
      .attr("x2", function(d) {
        return xcoords[1];
      })
      .attr("y2", function(d, i) {
        return (d.target+1)*100;
      })
      .style("stroke-width", 2)
      .style("stroke", "#000000");

    edges.enter()
      .append("text")
      .attr("transform", function(d, i) { return "translate("
       + (xcoords[0] + 160 + (d.target - d.source)*60) + ","
       + ((d.source+1)*100 + (d.target - d.source)*50 + 20)
       + ") rotate("
       + (d.target - d.source) * 15
       + ",0,0)"; })
      .text(function(d) {return d.type });
  }


  plotEdges(edges);
  plotGraph(jsonCircles[0]);
  plotGraph(jsonCircles[1]);


  </script>
</body>
</html>
"""]



def main():
    global html
    processes = {}
    with open('log.txt', 'r') as f:
        for line in f:
            (filename, access_type, junk1, junk2, pid) = line.strip().rstrip('.').split(' ')
            rwx = ''
            if access_type == 'read':
                rwx = 'r'
            elif access_type == 'modified':
                rwx = 'w'
            else:
                continue
            if pid in processes:
                processes[pid].add_file_access(filename, rwx)
            else:
                process = Process(pid)
                process.add_file_access(filename, rwx)
                processes[pid] = process

    with open('map.txt', 'r') as f:
        for line in f:
            (pid, name) = line.strip().split(': ')
            if pid in processes:
                processes[pid].set_name(name)

    process_id = 0
    file_ids = {}
    file_processes = {}
    processes_json = []
    edges = []
    for process in processes.itervalues():
        process_json = {}
        process_json['id'] = process_id
        process_json['name'] = process.name + '/' + str(process.pid)
        process_json['column'] = 0
        process_json['adjacencies'] = []

        for (filename, filename_accesses) in process.files.iteritems():
            if filename not in file_ids:
                file_ids[filename] = len(file_ids)
                file_processes[filename] = []
            process_json['adjacencies'].append(file_ids[filename])
            file_processes[filename].append(process_id)
            edges.append({'source':process_id, 'target':file_ids[filename], 'type':''.join(filename_accesses)})

        processes_json.append(process_json)
        process_id += 1

    files_json = []
    for (filename, uid) in file_ids.iteritems():
        file_json = {'id':uid, 'name':filename, 'column':1, 'adjacencies':file_processes[filename]}
        files_json.append(file_json)

    html[1] = json.dumps((processes_json, files_json))
    html[3] = json.dumps(edges)

    with open('view.html', 'w') as f:
        f.write(''.join(html))
    webbrowser.open('file://' + os.path.abspath('view.html'))

if __name__ == '__main__':
    main()
