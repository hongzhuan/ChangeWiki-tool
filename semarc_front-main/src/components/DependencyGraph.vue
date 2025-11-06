<template>
  <div class="Architecture">
    <!-- <div class="searchContainer">          
        <div class="searchItem">
          <input v-model="projectFolder" type="text" id="project_folder" placeholder="输入项目第一个版本文件夹路径">
        </div>
        <div v-if="resultMessage">
          <p>{{ resultMessage }}</p>
        </div>
      </div> -->
    <el-tabs v-model="activeName">
      <el-tab-pane label="整体项目概览" name="first">
        <el-card>
          <div class="entity">
            <div class="title-header">架构逆向层次图：</div>
            <!-- <div v-for="(shape, index) in shapes" :key="index" class="shape-item">
            </div> -->
            <div class="shapes-container">
              <div v-for="(shape, index) in shapes" :key="index" class="shape-item">
                <div class="shape">
                  <!-- 根据图形类型动态渲染 -->
                  <svg v-if="shape.type === 'circle'" width="50" height="50">
                    <circle cx="25" cy="25" r="20" stroke="rgba(0,0,0,0.7)" stroke-width="3" fill="rgba(43, 101, 236, 0.7)" />
                  </svg>
                  <svg v-if="shape.type === 'square'" width="50" height="50">
                    <rect width="50" height="50" stroke="rgba(0,0,0,0.7)" stroke-width="3" fill="rgba(43, 101, 236, 0.7)" />
                  </svg>
                  <svg v-if="shape.type === 'pentagon'" width="50" height="50">
                    <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="rgba(0,0,0,0.7)" stroke-width="3" fill="rgba(43, 101, 236, 0.7)" />
                  </svg>
                  <!-- 可以继续添加其他图形 -->
                </div>
                <div class="shape-name">
                  {{ shape.name }}
                </div>
              </div>
            </div>
            <div class="cytoscape-png"></div>

            <el-tag type="warning">注：点击红框区域可关闭已展开节点</el-tag>
            <el-button type="text" icon="el-icon-refresh" size="mini"
              style="background-color: #2973B2; color: #000;font-size: 1px; font-weight: bold;margin: 0 1%"
              @click="getEntityAgain">重新加载</el-button>
            <!-- 执行 前一个版本 通过选择文件来上传json文件-->
            <!-- <button @click="handleFileUpload">执行</button> -->
            <button class="btn" style="margin: 0 1%" @click="startClustering">执行</button> 
            <button class="btn" @click="showDialog">PlantUML </button>
            <!-- 对话框 -->
            <PlantUML v-if="isDialogVisible" @close="isDialogVisible = false" />
            <div id="network" style="margin-top: 1%"></div>
          </div>
          <!-- <div class="temporary_info">
            <span>{{temporary_info}}</span>
            </div> -->
          <!-- <div id="app"> -->
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
            <!-- <table border="1">
              <thead>
                <tr>
                  <th :title="fix_table_name + ' 的功能：'+ fix_table_function">{{ fix_table_name }}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colspan="4">
                    <ul>
                      <li v-for="( child, index ) in  temporary_children_info " :key=" index " :title="child.name + ' 的功能：' + child.function "
                        style="padding: 2% 0;">
                        {{ child.name }}
                      </li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table> -->
            <!-- <table border="1">
              <thead>
                <tr>
                <th>{{temporary_info_name}}</th>
                <th>{{temporary_info_type}}</th>
                <th>{{temporary_children_type}}</th>
                <th>{{temporary_children_name}}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(person, index) in paginatedTableData()" 
                  :key="person.id"
                  :class="{ highlight: selectedRowIndex === index }"
                  @click="selectRow(index)"
              >
              <td>{{ fix_table_name }}</td>
              <td>{{ fix_table_function }}</td>
              <td>{{ person.name }}</td>
              <td>{{ person.function }}</td>
              </tr>
            </tbody>
            </table> -->
            <!-- 分页控件 -->
            <!-- <div class="pagination">
                <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
                <span>Page {{ currentPage }} of {{ totalPages() }}</span> -->
            <!-- <button @click="nextPage" :disabled="currentPage === totalPages">Next</button> -->
            <!-- <button @click="nextPage" >Next</button> -->
            <!-- </div> -->
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
// @ts-ignore
import cytoscape from "cytoscape";
import fcose from 'cytoscape-fcose';
import EventBus from './eventBus';
import EventBusTable from './eventbustable';
import { compileString } from "sass";
import PlantUML  from "@/components/PlantUML.vue";

export default {
  /* eslint-disable */
  components: { PlantUML  },
  name: 'Architecture',
  data() {
    return {
      isDialogVisible: false,

      showModal: false,
      tableData: [],
      expandedKeys: [], // 存储展开的节点 ID
      activeName: 'first',
      resultMessage: '',
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
      shapes: [
        { type: 'circle', name: '——组件名称' },
        { type: 'square', name: '——模块名称' },
        { type: 'pentagon', name: '——文件名称' },
        // 可以继续添加更多几何图形
      ]
    }
  },
  created() {
    this.getEntity();
  },
  setup() {
    const sharedFile = computed(() => EventBus.sharedFile);
    return { sharedFile };
  },
  methods: {
    //PlantUML
    showDialog() {
      this.isDialogVisible = true;
    },




    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    // async startSemanticAnalysis() {
    //   // this.isChangeAnalysisActive = false;
    //   // this.isReverseActive = true;  // 点击变更分析时隐藏架构逆向
    //   //http://localhost:5000/get_semantic
    //   this.setActiveComponent('reverse')
    //   const response = await fetch('http://localhost:5000/get_semantic', {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ project_folder: this.projectFolder })
    //   });

    //   const data = await response.json();
    //   if (data.error) {
    //     this.resultMessage = `Error: ${data.error}`;
    //   } else {
    //     this.resultMessage = `Semantic analysis completed: Code semantics saved to ${data.code_sem_file}, Architecture semantics saved to ${data.arch_sem_file}`;
    //   }
    // },
    toggleReverse() {
      // this.isReverseActive = true;
      // this.isChangeAnalysisActive = false;  // 点击架构逆向时隐藏变更分析
      this.setActiveComponent('reverse');
    },
    setActiveComponent(component)
    {
      // 设置当前活动组件
      this.activeComponent = component;
    },
    async startClustering() {
      // this.isChangeAnalysisActive = false;
      // this.isReverseActive = true;  // 点击变更分析时隐藏架构逆向
      //localhost:5000
      this.setActiveComponent('reverse')
      // const response = await fetch('http://localhost:5000/run_clustering', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({ project_folder: this.projectFolder })
      // });

      // const data = await response.json();
      // 访问返回的数据
      // const message = data.message;
      // const codeSemFile = data.code_sem_file;
      // const archSemFile = data.arch_sem_file;
      // const startClustering = data.reverse_layer_graph;
      // console.log("hahhaa:"+data);
      // console.log("reverse_layer_graph:"+reverseLayerGraph);
      // console.log("data.shareFile:"+data.sharedFile);
      // EventBus.reverse1_change_json = startClustering
      this.jsonData = EventBus.sharedFile // 解析 JSON 数据
      this.getEntity()
      // console.log("this.projectFolder:"+this.projectFolder)
      // if (data.error) {
      //   this.resultMessage = `Error: ${data.error}`;
      //   console.log("Error: "+data.error);
      // } else {
      //   this.resultMessage = 'Clustering completed successfully!';
      //   if(this.resultMessage!='')
      //   {
      //     alert("json文件已生成！");
      //   }
      //   EventBus.sharedFile = data.sharedFile;
        // EventBus.sharedFile = "D:\\SemArc_backend\\results\\"+ this.projectFolder + "\\"+this.projectFolder+"_GraphIDFunc.json";
        // console.log("Vue页面中EventBus.sharedFile:"+EventBus.sharedFile);
        // EventBus.sharedFile = "D:\\SemArc_backend\\results\\enre\\enre_GraphIDFunc.json"
      // }
    },
    // 总页数
    totalPages() {
      return Math.ceil(this.temporary_children_info.length / this.itemsPerPage);
    },
    // 当前页显示的数据
    paginatedTableData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      console.log("this.temporary_children_info:" + this.temporary_children_info.slice(start, end))
      return this.temporary_children_info.slice(start, end);
    },
    // 上一页
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    // 下一页
    nextPage() {
      if (this.currentPage < this.totalPages()) {
        this.currentPage++;
      }
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
    // 处理搜索
    handleSearch() {
      this.highlightRow(this.current_file_name);
    },
    // 高亮符合搜索条件的行
    highlightRow(query) {
      // 在所有数据中查找匹配的行
      console.log("query:" + query)
      const rowIndexInAllData = this.temporary_children_info.findIndex(
        item => item.name === query
      );
      console.log("rowIndexInAllData:" + rowIndexInAllData)
      if (rowIndexInAllData !== -1) {
        // 计算该行在当前页的索引位置
        const rowIndexInCurrentPage = rowIndexInAllData - (this.currentPage - 1) * this.itemsPerPage;
        if (rowIndexInCurrentPage >= 0 && rowIndexInCurrentPage < this.itemsPerPage) {
          this.selectedRowIndex = rowIndexInCurrentPage;  // 高亮行
        } else {
          // 计算该行所在的页码
          const pageIndex = Math.floor(rowIndexInAllData / this.itemsPerPage) + 1;
          this.changePage(pageIndex);  // 切换到包含目标行的页面
          this.selectedRowIndex = null; // 等待页面加载完再设置选中的行
        }
      } else {
        this.selectedRowIndex = null;  // 如果没有找到匹配的行，取消高亮
      }
    },
    // 选择行
    selectRow(index) {
      this.selectedRowIndex = index;
    },
    // 更改页数
    changePage(page) {
      if (page >= 1 && page <= this.totalPages()) {
        this.currentPage = page;
        // this.selectedRowIndex = null;  // 页面切换时取消高亮
      }
    },
    handleFileUpload(event) {
      const file = EventBus.sharedFile;
      // const file = "D:\\SemArc_backend\\results\\enre\\enre_GraphIDFunc.json";
      console.log("file:" + file)
      console.log("file.type:" + file.type)
      if (file && file.type === 'application/json') {
        const reader = new FileReader();
        reader.onload = (e) => {
          try {
            this.jsonData = JSON.parse(e.target.result); // 解析 JSON 数据
            this.getEntity(); // 调用 getEntity 处理新数据
          } catch (error) {
            alert('文件格式不正确');
          }
        };
        reader.readAsText(file);
      } else {
        alert('请选择一个有效的 JSON 文件');
      }

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
          data: { id: node["id"], name: node["name"], parent: -1, classes: 'center-center', category: cat, function: node["Functionality"] }
        });
        edgesParam.add(node["id"]);
      })
      
      cytoscape.use(fcose);
      let cy = cytoscape({
        container: document.getElementById('network'),
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
              // 'shape': 'data(type)',
              // 'color': 'data(color)',
              "text-wrap": "wrap",
              'font-size': '14px',
              'background-opacity': 0.6,
              'background-color': '#2B65EC'
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
                  function: node["Functionality"]
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
        

      // this.tableData = []
      this.tableData.splice(0, this.tableData.length);
      console.log('前tableData', this.tableData)

      // 获取所有根节点（parentId=-1的节点）
      let rootNodes = this.getChildrenById(-1);
      
      // 遍历根节点，并递归获取子节点
      this.tableData = rootNodes.map(node => this.buildTree(node));
      console.log('全部tableData', this.tableData)
      
      // this.expandedKeys = []
      this.expandedKeys.splice(0, this.expandedKeys.length);
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
          data: { id: node["id"], name: node["name"], parent: -1, classes: 'center-center', category: cat, function: node["Functionality"] }
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
        container: document.getElementById('network'),
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
              'background-color': '#2B65EC'
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
                  function: node["Functionality"]
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

      // this.tableData = []
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
}
</script>

<style scoped>
.title-header {
  margin: 0em 0 0.5em;
}

.over-view {
  width: max(50vw, 800px);
}

.title-header {
  font-family: 'Arial', sans-serif;
  /* 修改字体 */
  font-size: 17px;
  /* 设置字体大小 */
  font-weight: bold;
  /* 设置加粗 */
  color: rgb(51, 53, 58);
  /* 设置字体颜色 */
  text-align: center;
  /* 设置文本居中 */
}

.temporary_info {
  font-size: 15px;
  color: #333;
  border: 1px solid #ccc;
  /* 边框设置 */
  border-radius: 5px;
  /* 可选：圆角边框 */
  padding: 10px;
  /* 可选：内边距，使内容不贴近边框 */
  margin-top: 10px;
  /* 添加外边距，避免边框重叠 */
}

#network {
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

#callgraph {
  width: 100%;
  height: 350px;
  overflow: auto;
  text-align: center;
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #69f;
}

#circle-box {
  width: 100px;
  height: 100px;
  background-color: #3498db;
  border-radius: 50%;
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

table {
  table-layout: fixed;
  /* 强制表格列宽固定 */

}

tr {
  height: 10px;
  /* 设置每行的高度 */
}

.highlight {
  background-color: #fff0f0;
  /* 高亮颜色 */
}

.pagination {
  margin-top: 10px;
}

.showList {
  margin-top: 1%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.btn {
  padding: 8px 16px;
  background-color: #2973B2;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:hover {
  background-color: #9ACBD0;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.btn:active {
  transform: translateY(0);
}
</style>