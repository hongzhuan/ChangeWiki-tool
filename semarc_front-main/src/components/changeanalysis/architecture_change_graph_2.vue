<template> 
    <div class="architecturechangegraph">
      <!-- 第一个部分：搜索框和查看按钮 -->
      <div class="search-container">
        <!-- 文件输入框 -->
        <button class="btn" @click="fetchJsonData">获取版本二架构变更图</button>
      </div>
      
      <el-tabs v-model="activeName">
      <el-tab-pane label="整体项目概览" name="first">
        <el-card>
          <div class="entity">
            <div class="title-header">变更分析层次图：</div>
            <!-- <div v-for="(shape, index) in shapes" :key="index" class="shape-item">
            </div>
            <div class="shapes-container">
              <div v-for="(shape, index) in shapes" :key="index" class="shape-item">
                <div class="shape"> -->
                  <!-- 根据图形类型动态渲染 -->
                  <!-- <svg v-if="shape.type === 'circle'" width="50" height="50">
                    <circle cx="25" cy="25" r="20" stroke="black" stroke-width="3" fill="blue" />
                  </svg>
                  <svg v-if="shape.type === 'square'" width="50" height="50">
                    <rect width="50" height="50" stroke="black" stroke-width="3" fill="blue" />
                  </svg> -->
                  <!-- <svg v-if="shape.type === 'pentagon'" width="50" height="50">
                    <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="black" stroke-width="3" fill="blue" />
                  </svg> -->
                  <!-- <svg v-if="shape.type === 'pentagon' & shape.name =='——添加的文件名称' " width="50" height="50">
                  <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="black" stroke-width="3" fill="red" />
                </svg>
                <svg v-if="shape.type === 'pentagon' & shape.name =='——移除的文件名称'" width="50" height="50">
                  <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="black" stroke-width="3" fill="yellow" />
                </svg>
                <svg v-if="shape.type === 'pentagon' & shape.name =='——移动的文件名称'" width="50" height="50">
                  <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="black" stroke-width="3" fill="green" />
                </svg> -->
                  <!-- 可以继续添加其他图形 -->
                <!-- </div>
                <div class="shape-name">
                  {{ shape.name }}
                </div>
              </div>
            </div> -->
            <div class="cytoscape-png"></div>
  
            <el-tag type="warning">注：点击红框区域可关闭已展开节点</el-tag>
            <el-button type="text" icon="el-icon-refresh" size="mini"
              style="background-color:#2973B2; color: white; font-size: 1px; font-weight: bold;margin-left: 1%;"
              @click="getEntityAgain">重新加载</el-button>
            <!-- 执行 -->
            <!-- <button @click="handleFileChange">执行</button> -->
            <div ref="architecture_change_graph" class="architecture_change_graph"  style="margin-top: 1%"></div>
          </div>
          <div class="showList">
            <el-table 
                ref="table"
              :data="tableData" 
              row-key="id" 
              :tree-props="{ children: 'children' }" 
              :expand-row-keys="expandedKeys"
              @expand-change="changeExpand"
              highlight-current-row
              icon-size="50"
              border
              >
                <el-table-column prop="name" label="节点名" width="240"></el-table-column>
                <el-table-column prop="category" label="类别" width="100"></el-table-column>
                <el-table-column prop="function" label="功能"></el-table-column>
              </el-table>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    </div>
  </template>
  
  <script>
  import cytoscape from "cytoscape";
  import fcose from 'cytoscape-fcose';
  import EventBus from "../eventBus";
  import EventBusTable from '../eventbustable';
  
  export default {
    data() {
      return {
      tableData: [],
      expandedKeys: [], // 存储展开的节点 ID
      activeName: 'first',
      versionPath1: '',  // 版本1路径
      versionPath2: '',  // 版本2路径
      graphLoading: false,
      childIdMap: new Map(),
      parentIdMap: new Map(),
      fileData: [],
      entityRoot: [],
      entityIdMap: new Map(),
      treeRoot: undefined,
      showedIds: new Set(),
      temporary_info: "dsadsa",
      temporary_info_table: [],
      last_info_table: [],
      fix_table_name: '',
      last_fix_table_name: '',
      fix_table_function: '',
      last_fix_table_function: '',
      temporary_info_name: '',
      temporary_info_type: '',
      temporary_children_name: '',
      temporary_children_type: '',
      temporary_children_info: [],
      last_children_info: [],
      currentPage: 1,
      itemsPerPage: 2,
      current_file_name: '',
      selectedRowIndex: null,
      //shapes: [
        //{ type: 'circle', name: '——组件名称' },
        //{ type: 'square', name: '——模块名称' },
        //{ type: 'pentagon', name: '——添加的文件名称' },
    //  { type: 'pentagon', name: '——移除的文件名称' },
      //{ type: 'pentagon', name: '——移动的文件名称' },
        // 可以继续添加更多几何图形
      //]
      };
    },
    methods: {
      // 文件上传
      fetchJsonData(event) {
      // const file = event.target.files[0];  
      // const file = EventBus.sharedFile;
      // const file = "C:\\Users\\23100\\Desktop\\backend\\semarc_backend\\architecture_change\\updated_structure.json";
      // console.log("file:" + file)
      // console.log("file.type:" + file.type)
      // const fs = require('fs');
      // // 读取 JSON 文件内容
      // fs.readFile(path, 'utf8', (err, data) => {
      //   if (err) {
      //     console.error("读取文件时出错:", err);
      //     return;
      //   }
      //   try {
      //     const jsonData = JSON.parse(data);  // 解析 JSON 数据
      //     console.log(jsonData);  // 你可以处理这个 JSON 数据
      //   } catch (error) {
      //     alert('请选择一个有效的 JSON 文件');
      //   }});
      // if (file && file.type === 'application/json') {
      //   const reader = new FileReader();
      //   reader.onload = (e) => {
      //     try {
      //       this.jsonData = JSON.parse(e.target.result); // 解析 JSON 数据
      //       this.getEntity(); // 调用 getEntity 处理新数据
      //     } catch (error) {
      //       alert('文件格式不正确');
      //     }
      //   };
      //   reader.readAsText(file);
      // } else {
      //   alert('请选择一个有效的 JSON 文件');
      // }
        console.log("hahah")
        this.jsonData = EventBus.architecture2_change_json
        this.getEntity(); 
    },
      navigateToCodeChangeAnalysis() {
        // 使用编程式导航来跳转到新页面
        this.$router.push({ name: 'code-change-analysis' });
      },
      getEntityCategory(node) {
      // if (node["External"] === true) {
      //   return "External";
      // }
      return node["category"];
    },
    // getRelationCategory(cell) {
    //   for (const key of Object.keys(cell["values"])) {
    //     if (key === "loc" || key === "bindVar" || key === "modifyAccessible" || key === "invoke" || key === "arguments") {
    //       continue;
    //     }
    //     return key;
    //   }
    //   return undefined;
    // },
    // getRelationsByIds(entityIds) {
    //   const relations = []
    //   if (!this.data.cells) {
    //     return undefined;
    //   }
    //   for (const cell of this.data["cells"]) {
    //     if (entityIds.has(cell["src"]) && entityIds.has(cell["dest"])) {
    //       relations.push(cell);
    //     }
    //   }
    //   return relations;
    // },
    getChildrenById(entityId) {
      if (!this.parentIdMap.has(entityId)) {
        return [];
      }
      return this.parentIdMap.get(entityId);
    },
    SendData() {
      const dataToSend = {
        temporary_info_name: this.temporary_info_name,
        temporary_info_type: this.temporary_info_type,
        temporary_children_name: this.temporary_children_name,
        temporary_children_type: this.temporary_children_type,
        temporary_children_info: this.temporary_children_info,
        fix_table_name: this.fix_table_name,
        fix_table_function: this.fix_table_function,
        current_file_name: this.current_file_name,
        selectedRowIndex: this.selectedRowIndex,
      };
  
      // 通过事件总线发送这些数据
      EventBusTable.$emit('sendData', dataToSend);
      console.log('Event sent');
    },
    async getData() {
      // this.data = enreData;
      if (!this.jsonData) {
        return;
      }
      this.data = this.jsonData; // 使用上传的 JSON 数据
      for (const variable of this.data["structure"]) {
        this.entityIdMap.set(variable["id"], variable);
        if (!this.parentIdMap.has(variable["parentId"])) {
          this.parentIdMap.set(variable["parentId"], []);
        }
        this.parentIdMap.get(variable["parentId"]).push(variable);
      }
    },
    getEntityAgain() {
      console.log('Data loaded:', this.data);
      const ref = this;
  
      this.entityRoot = []
      let edgesParam = new Set();
      this.getChildrenById(-1).forEach((node) => {
        const cat = ref.getEntityCategory(node);
        this.entityRoot.push({
          group: 'nodes',
          // data: {id: node["id"], name: node["name"], parent: -1, classes: 'center-center', category: cat}
          data: { id: node["id"], name: node["name"], parent: -1, classes: 'center-center', category: cat, function: node["Functionality"],
            color: node["color"] || '#2B65EC' }
        });
        edgesParam.add(node["id"]);
      })
      // let relations = ref.getRelationsByIds(edgesParam);
      // if (relations !== undefined) {
      //   ref.getRelationsByIds(edgesParam).forEach((edge) => {
      //     const cat = ref.getRelationCategory(edge);
      //     if (cat !== 'Contain' && cat !== 'Define') {
      //       this.entityRoot.push({
      //         group: 'edges',
      //         data: {id: edge.id, source: String(edge["src"]), target: String(edge["dest"]), category: cat}
      //       });
      //     }
      //   });
      // }
  
  
      // let cytoscape = window.cytoscape; node.id+'\n'+node.entityName
      /* eslint-disable */
      cytoscape.use(fcose);
      let cy = cytoscape({
        container: this.$refs.architecture_change_graph,
        ready: function () {
          this.nodes().forEach(function (node) {
            let size = 50;
            node.css("width", size);
            node.css("height", size);
          });
          // this.layout({name: 'fcose', fit: true, nodeRepulsion: 99999,initialEnergyOnIncremental: 0.1,nestingFactor:0.1, animationEasing: 'ease-out'}).run();
        },
        layout: {
          name: "fcose",
          fit: true,
          nodeRepulsion: 99999,
          animationDuration: 300,
          spacingFactor: 2.4,
          nodeDimensionsIncludeLabels: false,
        },
        // zoomingEnabled: false,
        // userZoomingEnabled: false,
        maxZoom: 2,
        minZoom: 0.1,
        userZoomingEnabled: true,
        style: [
          {
            selector: 'node',
            style: {
              'label': 'data(name)',
              'shape': 'data(type)',
              'color': 'data(color)',
              "text-wrap": "wrap",
              'font-size': '14px',
              'background-opacity': 0.6,
              // 'background-color': '#2B65EC'
              'background-color': 'data(color)'
            }
          },
  
          {
            selector: ':parent',
            style: {
              'background-opacity': 0.2,
              'border-color': '#62f'
            }
          },
  
          {
            selector: 'edge',
            style: {
              'label': 'data(category)',
              'line-color': '#2B65EC'
            }
          },
  
          {
            selector: 'node:selected',
            style: {
              'background-color': '#F08080',
              'border-color': 'red'
            }
          },
          {
            selector: 'edge:selected',
            style: {
              'line-color': '#F08080'
            }
          }
        ],
        elements: this.entityRoot,
      });
      console.log('Cytoscape instance:', cy); // 打印 Cytoscape 实例信息
      console.log('Entity Root:', this.entityRoot);
      cy.on('tap', 'node', function (evt) {
        var target = evt.target;
        console.log("target" + target);
        let num = 0
        if (target.selected()) {
          console.log("tatget selected" + num)
          num++
          target.children().forEach(ele => {
            cy.remove(ele)
            // cy.add(ele)
          });
          
          ref.removeExpandTableNode(target.id())
  
          cy.remove(target);
          cy.add(target);
          // cy.add({group:target.group, data:{id:target.entityId, name: target.entityId+'\n'+target.entityName, type: 'nodes', parent: target.parent}})
        } else {
          ref.addExpandTableNode(target.id());

          let edgesParam = new Set();
          let relations = ref.getChildrenById((Number(target.id())));
          console.log("ref.entityRoot节点：" + ref.entityRoot)
          // let entity1= JSON.stringify(ref.entityRoot)
          ref.entityRoot.forEach((node1) => {
            console.log("entityxaiozhou" + node1.id)
            if (Number(node1['id']) === Number(target.id())) {
              // ref.temporary_children_info.push(node1);
              console.log("当前的节点已加入")
            }
          });
          // console.log(relations)
          // console.log("relation:"+JSON.stringify(relations))
          let num = 1
          if (relations !== undefined) {
            console.log("relation_num" + num)
            num++;
            if (ref.getChildrenById(Number(target.id())).length === 0) {
              ref.last_children_info = ref.temporary_children_info
            } else ref.temporary_children_info = []
            ref.getChildrenById(Number(target.id())).forEach((node) => {
              console.log("childern:" + num)
              const cat = ref.getEntityCategory(node);
  
              // 判断 node['category'] 是否为 "item"
              let fileName = node['name']; // 默认使用 node['name']
  
              if (node['category'] === 'item') {
                const filePath = node['name']; // 如果 category 为 "item"，提取文件路径中的最后部分
                fileName = filePath.split("/").pop(); // 获取文件路径中的文件名部分
              }
              ref.temporary_children_info.push({ name: node['name'], function: node['Functionality'] })
              // ref.temporary_children_info.push({name: fileName, function: node['Functionality']})
              cy.add({
                group: 'nodes',
                data: {
                  id: node["id"],
                  name: node["name"],
                  // name: fileName,
                  parent: target.id(),
                  type: ref.getShape(cat),
                  classes: 'center-center',
                  category: cat,
                  function: node["Functionality"],
                  color: node["color"] || '#2B65EC'
                }
              })
              // cy.nodes().forEach((node) => {
              //   console.log("node.name:"+node.data.name)
              //   console.log("node.function:"+node.data.function)
              //   let size = 50;
              //   node.css("width", size);
              //   node.css("height", size);
              // });
            })
  
          }
          // console.log("hahhaha")
  
          cy.elements().forEach(ele => {
            console.log("target是：" + target)
  
            if (Number(target.id()) === Number(ele.data().id)) {
  
              ref.temporary_info = ele.data().name + ": " + ele.data().function
              ref.fix_table_name = ele.data().name
              ref.fix_table_function = ele.data().function
  
              ref.temporary_info_table.push(
                {
                  name: ele.data().name,
                  function: ele.data().function
                }
              )
  
              ref.temporary_info_name = ele.data().name;
              if (ele.data().category === 'component') {
                ref.temporary_info_name = '组件名'
                ref.temporary_info_type = '组件功能';
                ref.temporary_children_type = 'cluster';
                ref.temporary_children_name = '模块功能';
              } else if (ele.data().category === 'cluster') {
                ref.last_info_table = ref.temporary_info_table
                ref.last_children_info = ref.temporary_children_info
                ref.last_fix_table_name = ref.fix_table_name
                ref.last_fix_table_function = ref.fix_table_function
                console.log("")
                ref.temporary_info_name = '模块名'
                ref.temporary_info_type = '模块功能';
                ref.temporary_children_type = 'item';
                ref.temporary_children_name = '文件功能';
              } else if (ele.data().category === 'item') {
                ref.temporary_info_name = '模块名'
                ref.temporary_info_type = '模块功能';
                ref.temporary_children_type = 'item';
                ref.temporary_children_name = '文件功能';
                // ref.current_file_name = ele.data().name.split("/").pop()
                ref.current_file_name = ele.data().name
                ref.temporary_info_table = ref.last_info_table
                ref.temporary_children_info = ref.last_children_info
                ref.fix_table_name = ref.last_fix_table_name
                ref.fix_table_function = ref.last_fix_table_function
                console.log("xaxaxaxa")
                ref.handleSearch()
                ref.SendData()
                console.log("current_file_name:" + ref.current_file_name)
              }
              // console.log("temporary_info_table_name"+ ele.data().name)
              // console.log("temporary_info_type:"+ref.temporary_info_type)
              // console.log("temporary_children_type:"+ref.temporary_children_type)
              // console.log("temporary_children_name:"+ref.temporary_children_name)
            }
            ref.SendData()
            console.log("小周" + ele.data().name + " id号:" + ele.data().id)
            edgesParam.add(ele.data().id)
          })
          // relations = ref.getRelationsByIds(edgesParam);
          // if (relations !== undefined){
          //   ref.getRelationsByIds(edgesParam).forEach((edge) => {
          //     const cat = ref.getRelationCategory(edge);
          //     if (cat !== 'Contain' && cat !== 'Define') {
          //       cy.add({
          //         group: 'edges',
          //         data: {id: edge.id, source: String(edge["src"]), target: String(edge["dest"]), category: cat}
          //       })
          //     }
          //   });
          // }
  
  
          let layout = cy.layout({
            name: "fcose",
            fit: true,
            nodeRepulsion: 999, // 节点排斥
            randomize: false,
            animationDuration: 300,
            padding: 30,
            nodeDimensionsIncludeLabels: false, // 标签包含文字
            initialEnergyOnIncremental: 0.5, // 初始能量增量
            nestingFactor: 0.5, // 嵌套因素
            spacingFactor: 5, // 间距因素
          })
          layout.run()
  
        }
      });
      // cy.nodes().on('right-click', (evt) => {
      //     console.log(evt.target)
      // });
      // cy.edges().on('click', (evt) => {
      //     console.log(evt.target)
      // });
      this.tableData.splice(0, this.tableData.length);
      console.log('前tableData', this.tableData)

      // 获取所有根节点（parentId=-1的节点）
      let rootNodes = this.getChildrenById(-1);
      
      // 遍历根节点，并递归获取子节点
      this.tableData = rootNodes.map(node => this.buildTree(node));
      console.log('全部tableData', this.tableData)
      
      this.expandedKeys = []
      console.log('tableData expandedKeys', this.expandedKeys)
    },
    async getEntity() {
      await this.getData();
      console.log('Data loaded:', this.data);
      const ref = this;
  
      this.entityRoot = []
      let edgesParam = new Set();
      this.getChildrenById(-1).forEach((node) => {
        const cat = ref.getEntityCategory(node);
        this.entityRoot.push({
          group: 'nodes',
          // data: {id: node["id"], name: node["name"], parent: -1, classes: 'center-center', category: cat}
          data: { id: node["id"], name: node["name"], parent: -1, classes: 'center-center', category: cat, function: node["Functionality"],
            color: node["color"] || '#2B65EC' }
        });
        edgesParam.add(node["id"]);
      })
      // let relations = ref.getRelationsByIds(edgesParam);
      // if (relations !== undefined) {
      //   ref.getRelationsByIds(edgesParam).forEach((edge) => {
      //     const cat = ref.getRelationCategory(edge);
      //     if (cat !== 'Contain' && cat !== 'Define') {
      //       this.entityRoot.push({
      //         group: 'edges',
      //         data: {id: edge.id, source: String(edge["src"]), target: String(edge["dest"]), category: cat}
      //       });
      //     }
      //   });
      // }
  
  
      // let cytoscape = window.cytoscape; node.id+'\n'+node.entityName
      /* eslint-disable */
      cytoscape.use(fcose);
      let cy = cytoscape({
        container: this.$refs.architecture_change_graph,
        ready: function () {
          this.nodes().forEach(function (node) {
            let size = 50;
            node.css("width", size);
            node.css("height", size);
          });
          // this.layout({name: 'fcose', fit: true, nodeRepulsion: 99999,initialEnergyOnIncremental: 0.1,nestingFactor:0.1, animationEasing: 'ease-out'}).run();
        },
        layout: {
          name: "fcose",
          fit: true,
          nodeRepulsion: 99999,
          animationDuration: 300,
          spacingFactor: 2.4,
          nodeDimensionsIncludeLabels: false,
        },
        // zoomingEnabled: false,
        // userZoomingEnabled: false,
        maxZoom: 2,
        minZoom: 0.1,
        userZoomingEnabled: true,
        style: [
          {
            selector: 'node',
            style: {
              'label': 'data(name)',
              'shape': 'data(type)',
              'color': 'data(color)',
              "text-wrap": "wrap",
              'font-size': '14px',
              'background-opacity': 0.6,
              // 'background-color': '#2B65EC'
              'background-color': 'data(color)'
            }
          },
  
          {
            selector: ':parent',
            style: {
              'background-opacity': 0.2,
              'border-color': '#62f'
            }
          },
  
          {
            selector: 'edge',
            style: {
              'label': 'data(category)',
              'line-color': '#2B65EC'
            }
          },
  
          {
            selector: 'node:selected',
            style: {
              'background-color': '#F08080',
              'border-color': 'red'
            }
          },
          {
            selector: 'edge:selected',
            style: {
              'line-color': '#F08080'
            }
          }
        ],
        elements: this.entityRoot,
      });
      console.log('Cytoscape instance:', cy); // 打印 Cytoscape 实例信息
      console.log('Entity Root:', this.entityRoot);
      cy.on('tap', 'node', function (evt) {
        var target = evt.target;
        console.log("target" + target);
        let num = 0
        if (target.selected()) {
          console.log("tatget selected" + num)
          num++
          target.children().forEach(ele => {
            cy.remove(ele)
            // cy.add(ele)
          });

          ref.removeExpandTableNode(target.id())
  
          cy.remove(target);
          cy.add(target);
          // cy.add({group:target.group, data:{id:target.entityId, name: target.entityId+'\n'+target.entityName, type: 'nodes', parent: target.parent}})
        } else {
          ref.addExpandTableNode(target.id());

          let edgesParam = new Set();
          let relations = ref.getChildrenById((Number(target.id())));
          console.log("ref.entityRoot节点：" + ref.entityRoot)
          // let entity1= JSON.stringify(ref.entityRoot)
          ref.entityRoot.forEach((node1) => {
            console.log("entityxaiozhou" + node1.id)
            if (Number(node1['id']) === Number(target.id())) {
              // ref.temporary_children_info.push(node1);
              console.log("当前的节点已加入")
            }
          });
          // console.log(relations)
          // console.log("relation:"+JSON.stringify(relations))
          let num = 1
          if (relations !== undefined) {
            console.log("relation_num" + num)
            num++;
            if (ref.getChildrenById(Number(target.id())).length === 0) {
              ref.last_children_info = ref.temporary_children_info
            } else ref.temporary_children_info = []
            ref.getChildrenById(Number(target.id())).forEach((node) => {
              console.log("childern:" + num)
              const cat = ref.getEntityCategory(node);
  
              // 判断 node['category'] 是否为 "item"
              let fileName = node['name']; // 默认使用 node['name']
  
              if (node['category'] === 'item') {
                const filePath = node['name']; // 如果 category 为 "item"，提取文件路径中的最后部分
                fileName = filePath.split("/").pop(); // 获取文件路径中的文件名部分
              }
              ref.temporary_children_info.push({ name: node['name'], function: node['Functionality'] })
              // ref.temporary_children_info.push({name: fileName, function: node['Functionality']})
              cy.add({
                group: 'nodes',
                data: {
                  id: node["id"],
                  name: node["name"],
                  // name: fileName,
                  parent: target.id(),
                  type: ref.getShape(cat),
                  classes: 'center-center',
                  category: cat,
                  function: node["Functionality"],
                  color: node["color"] || '#2B65EC'
                }
              })
              // cy.nodes().forEach((node) => {
              //   console.log("node.name:"+node.data.name)
              //   console.log("node.function:"+node.data.function)
              //   let size = 50;
              //   node.css("width", size);
              //   node.css("height", size);
              // });
            })
  
          }
          // console.log("hahhaha")
  
          cy.elements().forEach(ele => {
            console.log("target是：" + target)
  
            if (Number(target.id()) === Number(ele.data().id)) {
  
              ref.temporary_info = ele.data().name + ": " + ele.data().function
              ref.fix_table_name = ele.data().name
              ref.fix_table_function = ele.data().function
  
              ref.temporary_info_table.push(
                {
                  name: ele.data().name,
                  function: ele.data().function
                }
              )
  
              ref.temporary_info_name = ele.data().name;
              if (ele.data().category === 'component') {
                ref.temporary_info_name = '组件名'
                ref.temporary_info_type = '组件功能';
                ref.temporary_children_type = 'cluster';
                ref.temporary_children_name = '模块功能';
              } else if (ele.data().category === 'cluster') {
                ref.last_info_table = ref.temporary_info_table
                ref.last_children_info = ref.temporary_children_info
                ref.last_fix_table_name = ref.fix_table_name
                ref.last_fix_table_function = ref.fix_table_function
                console.log("")
                ref.temporary_info_name = '模块名'
                ref.temporary_info_type = '模块功能';
                ref.temporary_children_type = 'item';
                ref.temporary_children_name = '文件功能';
              } else if (ele.data().category === 'item') {
                ref.temporary_info_name = '模块名'
                ref.temporary_info_type = '模块功能';
                ref.temporary_children_type = 'item';
                ref.temporary_children_name = '文件功能';
                // ref.current_file_name = ele.data().name.split("/").pop()
                ref.current_file_name = ele.data().name
                ref.temporary_info_table = ref.last_info_table
                ref.temporary_children_info = ref.last_children_info
                ref.fix_table_name = ref.last_fix_table_name
                ref.fix_table_function = ref.last_fix_table_function
                console.log("xaxaxaxa")
                ref.handleSearch()
                ref.SendData()
                console.log("current_file_name:" + ref.current_file_name)
              }
              // console.log("temporary_info_table_name"+ ele.data().name)
              // console.log("temporary_info_type:"+ref.temporary_info_type)
              // console.log("temporary_children_type:"+ref.temporary_children_type)
              // console.log("temporary_children_name:"+ref.temporary_children_name)
            }
            ref.SendData()
            console.log("小周" + ele.data().name + " id号:" + ele.data().id)
            edgesParam.add(ele.data().id)
          })
          // relations = ref.getRelationsByIds(edgesParam);
          // if (relations !== undefined){
          //   ref.getRelationsByIds(edgesParam).forEach((edge) => {
          //     const cat = ref.getRelationCategory(edge);
          //     if (cat !== 'Contain' && cat !== 'Define') {
          //       cy.add({
          //         group: 'edges',
          //         data: {id: edge.id, source: String(edge["src"]), target: String(edge["dest"]), category: cat}
          //       })
          //     }
          //   });
          // }
  
  
          let layout = cy.layout({
            name: "fcose",
            fit: true,
            nodeRepulsion: 999, // 节点排斥
            randomize: false,
            animationDuration: 300,
            padding: 30,
            nodeDimensionsIncludeLabels: false, // 标签包含文字
            initialEnergyOnIncremental: 0.5, // 初始能量增量
            nestingFactor: 0.5, // 嵌套因素
            spacingFactor: 5, // 间距因素
          })
          layout.run()
  
        }
      });
      // cy.nodes().on('right-click', (evt) => {
      //     console.log(evt.target)
      // });
      // cy.edges().on('click', (evt) => {
      //     console.log(evt.target)
      // });
      this.tableData.splice(0, this.tableData.length);
      console.log('前tableData', this.tableData)

      // 获取所有根节点（parentId=-1的节点）
      let rootNodes = this.getChildrenById(-1);
      
      // 遍历根节点，并递归获取子节点
      this.tableData = rootNodes.map(node => this.buildTree(node));
      console.log('全部tableData', this.tableData)
      
      this.expandedKeys = []
      console.log('tableData expandedKeys', this.expandedKeys)
    },
    buildTree(node) {
      const children = this.getChildrenById(node.id).map(child => this.buildTree(child));
      if(this.getEntityCategory(node) === 'item'){
        return {
        id: node.id,
        name: node.name,
        category: 'file',
        function: node.Functionality,
        children: children.length > 0 ? children : [] // 只有有子节点才添加 children
      };
      }
      return {
        id: node.id,
        name: node.name,
        category: this.getEntityCategory(node),
        function: node.Functionality,
        children: children.length > 0 ? children : [] // 只有有子节点才添加 children
      };
    },
    addExpandTableNode(nodeId) {
      // 如果 ID 不在 expandedKeys 列表中，则添加
      if (!this.expandedKeys.includes(nodeId)) {
        this.expandedKeys = [...this.expandedKeys, nodeId]; 
      }
      console.log('添加 expandedKeys', this.expandedKeys)
      const targetRow = this.findRowById(this.tableData, nodeId);
      console.log(`找到的行数据:`, targetRow); 
      if (targetRow) {
        this.$refs.table.setCurrentRow(targetRow);
      }
    },
    findRowById(data, id) {
      if (!Array.isArray(data)) return null;

      for (const item of data) {
        console.log("正在检查:", item.id, "目标ID:", id); // 调试信息

        if (String(item.id) === String(id)) { 
          console.log("找到目标行:", item);
          return item;
        }

        if (item.children && Array.isArray(item.children)) {
          const found = this.findRowById(item.children, id);
          if (found) return found;
        }
      }
      return null;
    },
    removeExpandTableNode(nodeId) {
      console.log('移除前 expandedKeys', this.expandedKeys);
      const index = this.expandedKeys.indexOf(nodeId);
      if (index !== -1) {
        this.expandedKeys.splice(index, 1);
        // 直接更新 expandedKeys 为新的数组
        this.expandedKeys = this.expandedKeys.slice();
      }
      console.log('移除后 expandedKeys', this.expandedKeys);
    },
    changeExpand(row){
      console.log('折叠变化：', row.id)
      const nodeId = row.id
      console.log(nodeId)
    },
    existSourceTarget(id) {
      console.log(id)
    },
    getShape(cate) {
      if (cate == 'component') {
        return 'cut-rectangle'
      } else if (cate == 'cluster') {
        return 'round-triangle'
      } else if (cate == 'item') {
        return 'pentagon'
      }
      // if (cate == 'Package') {
      //   return 'cut-rectangle'
      // } else if (cate == 'File') {
      //   return 'round-triangle'}
      // else if (cate == 'Class') {
      //   return 'pentagon'}
      // } else if (cate == 'Enum Constant') {
      //   return 'star'
      // } else if (cate == 'Annotation') {
      //   return 'right-rhomboid'
      // } else if (cate == 'Annotation Member') {
      //   return 'rhomboid'
      // } else if (cate == 'Interface') {
      //   return 'diamond'
      // } else if (cate == 'Method') {
      //   return 'concave-hexagon'
      // } else if (cate == 'Module') {
      //   return 'round-tag'
      // } else if (cate == 'Type Parameter') {
      //   return 'hexagon'
      // } else if (cate == 'Variable') {
      //   return 'vee'
      // } else {
      //   return 'ellipse'
      // }
    },
    }
  };
  </script>  
  
  <style scoped>
  /* 容器样式 */
  .architecturechangegraph {
    width: min(98%, 90vh);
    padding: 20px;
    background-color: #f7f7f7;
    overflow: auto
  }
  
  /* 搜索框容器样式 */
  .search-container {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .search-item {
    display: flex;
    gap: 10px;
    width: 100%;
  }
  
  .search-item input {
    flex: 1;
    padding: 6px;
    font-size: 14px;
  }
  
  .select-button {
    padding: 6px 12px;
    background-color: #34495e;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .select-button:hover {
    background-color: #9ACBD0;
  }
  
  /* 表格容器样式 */
  .table-container {
    margin-bottom: 20px;
    overflow: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    color: black;
  }
  
  th, td {
    padding: 8px 12px;
    text-align: center;
    border: 1px solid #100f0f;
  }
  
  th {
    background-color: #f1f1f1;
  }
  
  /* 按钮容器样式 */
  .button-container {
    display: flex;
    justify-content: flex-start;
    gap: 20px;
  }
  
  .action-button {
    padding: 10px 15px;
    font-size: 16px;
    background-color: #34495e;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .action-button:hover {
    background-color: #9ACBD0;
  }
  
  .shapes-container {
  display: flex;
  flex-wrap: wrap;
  /* 如果图形数量太多，自动换行 */
  gap: 20px;
  justify-content: start;
  }
  
  .shape-item {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  }
  
  .shape-name {
  font-size: 14px;
  font-weight: bold;
  }
  
  .architecture_change_graph {
  width: 75vh;
  height: 55vh;
  overflow: visible;
  border: 1px solid #69f;
  position: relative;
  /* 确保定位正确 */
  z-index: 10;
  /* 确保内容不会被其他元素遮挡 */
  text-align: start;
  }
  .btn {
    width: 20%;
    background-color: green; /* 设置背景颜色为绿色 */
    color: white; /* 设置字体颜色为白色 */
    padding: 10px 20px; /* 添加一些内边距 */
    border: none; /* 移除边框 */
    border-radius: 5px; /* 添加圆角 */
    cursor: pointer; /* 鼠标悬停时显示为指针 */
}

.showList {
  margin-top: 1%;
  /* width: 100%; */
  /* display: flex; */
  /* justify-content: center; */
  /* align-items: center; */
  /* text-align: center; */
}
  </style>  