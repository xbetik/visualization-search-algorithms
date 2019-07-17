var labels=["A","B","C","D"];
var treeData = {
  "name" : "0",
  "nodeOrder" : 1,
  "children" : [
    {
      "name" : "2",
      "nodeOrder" : 2,
      "edgeLabelLeft" : "left",
      "edgeLabelRight" : "right",
      "children" : [
        {
          "name" : "1",
          "nodeOrder" : 4,
          "children" : [
            {
              "name" : "1",
              "nodeOrder" : 10,
              "children" : [
                {
                  "name" : "1",
                  "nodeOrder" : 13,
                  "nodeType" : "rectangle",
                  "nodeColor" : "red",
                  "label1" : "(c3, c4)",
                  "arrowToNode" : "yes",
                  "arrowFromNode" : "yes",
                  "edgeLabelLeft" : "left label",
                  "dashLine" : "yes",
                },
                {
                  "name" : "2",
                  "nodeOrder" : 14,
                  "edgeLabelRight" : "right label"
                }
              ]

            },
            {
              "name" : "2",
              "nodeOrder" : 11,
              "edgeLabelLeft" : "left label"
            },
            {
              "name" : "3",
              "nodeOrder" : 12,
            }
          ]

        },
        {
          "name" : "2",
          "nodeOrder" : 5,
          "shape" : "rectangle",
          "nodeColor" : "red",
          "arrowToNode" : "yes",
          "label1" : "c2 : C ∈ {1}",
          "sideLabels" : ["c3 : C ∈ {2}"]
        },
        {
          "name" : "3",
          "nodeOrder" : 6,
          "sideLabels" : ["c2 : C ∈ {1}", "c3 : D ∈ {2}"],
          "children" : [
            {
              "name" : "1",
              "nodeOrder" : 15,
              "shape" : "rectangle",
              "nodeColor" : "red",
              "label1" : "(c1)"
            },
            {
              "name" : "2",
              "nodeOrder" : 16,
              "shape" : "rectangle",
              "nodeColor" : "red",
              "label1" : "(c1)"
            },
            {
              "name" : "3",
              "nodeOrder" : 17,
              "children" : [
                {
                  "name" : "1",
                  "nodeOrder" : 18,
                  "nodeColor" : "blank",
                  "edgeLabelRight" : "D==3"
                },
                {
                  "name" : "2",
                  "nodeOrder" : 19,
                  "nodeColor" : "blank",
                  "edgeLabelRight" : "D==2"
                }
              ]

            }
          ]

        }
      ]

    },
    {
      "name" : "3",
      "nodeOrder" : 3,
      "edgeLabelLeft" : "left",
      "edgeLabelRight" : "right",
      "arrowFromNode" : "yes",
      "children" : [
        {
          "name" : "1",
          "nodeOrder" : 7,
          "children" : [
            {
              "name" : "1",
              "nodeOrder" : 20,
              "children" : [
                {
                  "name" : "1",
                  "nodeOrder" : 26,
                  "shape" : "rectangle",
                  "nodeColor" : "red",
                  "label1" : "(c3, c4)"
                },
                {
                  "name" : "2",
                  "nodeOrder" : 27,
                  "nodeColor" : "blank"
                }
              ]

            },
            {
              "name" : "2",
              "nodeOrder" : 21,
              "shape" : "rectangle",
              "nodeColor" : "red",
              "label1" : "(c2)"
            },
            {
              "name" : "3",
              "nodeOrder" : 22,
              "shape" : "rectangle",
              "nodeColor" : "red",
              "label1" : "(c2)"
            }
          ]

        },
        {
          "name" : "2",
          "nodeOrder" : 8,
          "children" : [
            {
              "name" : "1",
              "nodeOrder" : 23,
              "shape" : "rectangle",
              "nodeColor" : "red",
              "label1" : "(c2)"
            },
            {
              "name" : "2",
              "nodeOrder" : 24,
              "children" : [
                {
                  "name" : "1",
                  "nodeOrder" : 28,
                  "nodeColor" : "blank"
                },
                {
                  "name" : "2",
                  "nodeOrder" : 29,
                  "shape" : "rectangle",
                  "nodeColor" : "red",
                  "label1" : "(c3, c4)"
                }
              ]

            },
            {
              "name" : "3",
              "nodeOrder" : 25,
              "shape" : "rectangle",
              "nodeColor" : "red",
              "label1" : "(c2)"
            }
          ]

        },
        {
          "name" : "3",
          "nodeOrder" : 9,
          "shape" : "rectangle",
          "nodeColor" : "red",
          "sideLabels" : ["c2 : C ∈ {1}", "c3 : D ∈ {2}"],
          "label1" : "(c1)"
        }
      ]

    }
  ]
};
