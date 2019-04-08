var labels=["A","B","C","D"];
var treeData = {
  "name": "0",
  "random" : 40,
  "id" : 100,
  "children": [
    {
      "name": "2",
      "children": [
        {
          "name": "1",
          "children": [
            {
              "name": "1",
              "children": [
                {
                  "name": "1",
                  "type": "rectangle",
                  "color": "red",
                  "constraintLabel" : "(c3,c4)"
                },
                {
                  "name": "2"
                }
              ]
            },
            {
              "name": "2",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c2)"
            },
            {
              "name": "3",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c2)"
            }
          ]
        },
        {
          "name": "2",
          "type": "rectangle",
          "color": "red",
          "constraintLabel" : "(c1)"
        },
        {
          "name": "3",
          "children": [
            {
              "name": "1",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c1)"
            },
            {
              "name": "2",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c1)"
            },
            {
              "name": "3",
              "children": [
                {
                  "name": "1",
                  "color":"blank"
                },
                {
                  "name": "2",
                  "color":"blank"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "3",
      "children": [
        {
          "name": "1",
          "children": [
            {
              "name": "1",
              "children": [
                {
                  "name": "1",
                  "type": "rectangle",
                  "color": "red",
                  "constraintLabel" : "(c3,c4)"
                },
                {
                  "name": "2",
                  "color": "blank"
                }
              ]

            },
            {
              "name": "2",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c2)"
            },
            {
              "name": "3",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c2)"
            }
          ]

        },
        {
          "name": "2",
          "children": [
            {
              "name": "1",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c2)"
            },
            {
              "name": "2",
              "children": [
                {
                  "name": "1",
                  "color": "blank"
                },
                {
                  "name": "2",
                  "type": "rectangle",
                  "color": "red",
                  "constraintLabel" : "(c3,c4)"
                }
              ]
            },
            {
              "name": "3",
              "type": "rectangle",
              "color": "red",
              "constraintLabel" : "(c2)"
            }
          ]
        },
        {
          "name": "3",
          "type": "rectangle",
          "color": "red",
          "constraintLabel" : "(c1)"
        },
      ]
    }
  ]
};