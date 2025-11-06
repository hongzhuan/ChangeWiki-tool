<template> 
  <div class="a2amoduldiference">
    <div class="top">
            <!-- 第一个部分：搜索框和查看按钮 -->
    <!-- <div class="search-container">
      <div class="search-item">
        <input 
          type="text" 
          v-model="versionPath1"
          placeholder="请选择版本1路径" 
        />
        <button class="select-button" @click="selectPath1">查看</button>
      </div>
      <div class="search-item">
        <input 
          type="text" 
          v-model="versionPath2"
          placeholder="请选择版本2路径" 
        />
        <button class="select-button" @click="selectPath2">查看</button>
      </div>
    </div> -->

    <!-- 第二个部分：表格 -->
    <div class="table-container">
      <el-table
          :data="tableDatashowBack_to_front"
          :height="'calc(50vh - 200px)'"
          highlight-current-row
          :cell-style="getCellStyle"
          :header-cell-style="getHeaderStyle"
          :default-sort = "{prop: 'date', order: 'descending'}"
        >
        
        <el-table-column label="版本分析">
          <el-table-column prop="version1" label="版本一"></el-table-column>
          <el-table-column prop="version2" label="版本二"></el-table-column>
        </el-table-column>
        <el-table-column label="模块文件信息分析">
          <el-table-column prop="version1_total_file_number" label="V1模块文件总量" sortable width="200"></el-table-column>
          <el-table-column prop="version1_change_file_number" label="V1文件移动数量" sortable width="200"></el-table-column>
          <el-table-column prop="version2_total_file_number" label="V2模块文件总量" sortable width="200"></el-table-column>
          <el-table-column prop="version2_change_file_number" label="V2文件移动数量" sortable width="200"></el-table-column>
        </el-table-column>
        <el-table-column label="结构变更分析">
          <el-table-column prop="a2a_weight" label="a2a指标中各模块权重大小" sortable width="280"></el-table-column>
        </el-table-column>
        <el-table-column label="历史变更分析">
          <el-table-column prop="LOC" label="模块中文件代码修改量总和" sortable width="280"></el-table-column>
          <el-table-column prop="commit_weight" label="commit历史中各模块权重大小" sortable width="290"></el-table-column>
        </el-table-column>
          <!-- <el-table-column prop="commitAnalysis" label="commit分析" sortable></el-table-column>
          <el-table-column prop="weight" label="加权平均" sortable></el-table-column> -->
          <!-- <el-table-column label="操作" width="180">
            <template slot-scope="scope">
              <button class="btn" @click="showDetail(scope.row)">
                查看详情
              </button>
            </template>
          </el-table-column> -->
          
      </el-table>
    </div>
    </div>
    
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
                <!-- <svg v-if="shape.type === 'pentagon'" width="50" height="50">
                  <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="black" stroke-width="3" fill="blue" />
                </svg> -->
                <svg v-if="shape.type === 'pentagon' & shape.name =='——添加的文件名称' " width="50" height="50">
                  <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="rgba(0,0,0,0.7)" stroke-width="3" fill="rgba(255, 0, 0, 0.7)" />
                </svg>
                <svg v-if="shape.type === 'pentagon' & shape.name =='——移除的文件名称'" width="50" height="50">
                  <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="rgba(0,0,0,0.7)" stroke-width="3" fill="rgba(255, 255, 0, 0.7)" />
                </svg>
                <svg v-if="shape.type === 'pentagon' & shape.name =='——移动的文件名称'" width="50" height="50">
                  <polygon points="25,5 45,15 37,40 13,40 5,15" stroke="rgba(0,0,0,0.7)" stroke-width="3" fill="rgba(0, 255, 0, 0.7)" />
                </svg>
                <!-- 可以继续添加其他图形 -->
              </div>
              <div class="shape-name">
                {{ shape.name }}
              </div>
            </div>
          </div>
    
    <!-- 第三个部分：按钮容器 -->
    <div class="botton">
      <div class="botton-half">
        <architecturechangegraph />
      </div>
      <div class="botton-half">
        <architecturechangegraph2 />
      </div>
    </div>

    <el-dialog :title="showDetailDialogTitle" :visible.sync="showDetailDialog" width="70%">
        <div style="padding: 2% 0;display: flex;gap: 1%;">
          <el-table
            :data="showDetailCluster1Table"
            highlight-current-row
            :cell-style="getCellStyle"
            :header-cell-style="getHeaderStyle"
          >
            <el-table-column prop="module_name" label="模块名"></el-table-column>
            <el-table-column prop="total_file_number" label="总文件数目" width="150"></el-table-column>
            <el-table-column prop="change_file_number" label="改变的文件数目" width="150"></el-table-column>
          </el-table>
          <el-table
            :data="showDetailCluster2Table"
            highlight-current-row
            :cell-style="getCellStyle"
            :header-cell-style="getHeaderStyle"
          >
            <el-table-column prop="module_name" label="模块名"></el-table-column>
            <el-table-column prop="total_file_number" label="总文件数目" width="150"></el-table-column>
            <el-table-column prop="change_file_number" label="改变的文件数目" width="150"></el-table-column>
          </el-table>
        </div>
      </el-dialog>
  </div>
</template>

<script>
import architecturechangegraph from '@/components/changeanalysis/architecture_change_graph.vue'
import architecturechangegraph2 from '@/components/changeanalysis/architecture_change_graph_2.vue'
import axios from 'axios';
import EventBus from '../eventBus';
export default {
  components: {
    architecturechangegraph,
    architecturechangegraph2,
  },
  data() {
    return {
      mergedCellContent1: "结构变更分析",
      mergedCellContent2: "历史变更分析",
      versionPath1: '',  // 版本1路径
      versionPath2: '',  // 版本2路径
      tableDatashowBack_to_front: [],
      tableData: null,
      showDetailDialog: false,
      showDetailDialogTitle: null,
      showDetailDialogTable: null,
      shapes: [
        { type: 'circle', name: '——组件名称' },
        { type: 'square', name: '——模块名称' },
        // { type: 'pentagon', name: '——文件名称' },
        { type: 'pentagon', name: '——添加的文件名称' },
        { type: 'pentagon', name: '——移除的文件名称' },
        { type: 'pentagon', name: '——移动的文件名称' },
        // 可以继续添加更多几何图形
      ]
    };
  },
  mounted(){
    // this.convertData();
  },
  methods: {  
    
    convertData(){
      // console.log('查看module_weight数据:', EventBus.module_weight);
      // this.tableDatashowBack_to_front = Object.entries(EventBus.module_weight).map(([key, value]) => {
      //   // 去掉括号并分割字符串
      //   const [x1, x2] = key.replace(/[()]/g, '').split(',');
      //   console.log("x1:"+x1)
      //   return {
      //     x1: x1.trim(),  // 去掉多余的空格
      //     x2: x2.trim(),
      //     value: value
      //   };
      // });
      console.log('a2a页面中a2a_tableInfo:', EventBus.a2a_tableInfo);
      console.log('a2a页面中a2a_tableInfo.structure:', EventBus.a2a_tableInfo.structure);
      this.tableDatashowBack_to_front = EventBus.a2a_tableInfo_json_add_fileInfo.structure.map(item => {
            return {
              version1: item.version1,
              version2: item.version2,
              a2a_weight: Number(item.a2a_weight).toFixed(5),
              LOC: item.LOC,
              commit_weight: Number(item.commit_weight).toFixed(5),
              version1_total_file_number: item.version1_total_file_number,
              version1_change_file_number: item.version1_change_file_number,
              version2_total_file_number: item.version2_total_file_number,
              version2_change_file_number: item.version2_change_file_number,
            };
          });
      console.log('查看数据:', this.tableDatashowBack_to_front);
    },
    selectPath1() {
      console.log('查看版本路径1:', this.versionPath1);
    },
    selectPath2() {
      console.log('查看版本路径2:', this.versionPath2);
    },
    navigateToCodeChangeAnalysis() {
      // 使用编程式导航来跳转到新页面
      this.$router.push({ name: 'code-change-analysis' });
    },
    showDetail(row){
      console.log('查看详情 row', row)

      this.showDetailDialog = true
      this.showDetailDialogTitle = row.versionChange + ' : ' + row.movementDistance + ' 的变更详情'
      this.showDetailCluster1Table = row.cluster1_information
      this.showDetailCluster2Table = row.cluster2_information
    },
    getHeaderStyle() {
      return 'background-color:transparent; color: #000000; text-align: center; padding: 0;'
    },
    getCellStyle() {
      return 'background-color:transparent; color: #000000; text-align: center; padding: 0;'
    },
  },
  // watch: {
  //   // 监听EventBus中的module_weight数据变化
  //   'EventBus.module_weight': {
  //     handler: function (val) {
  //       console.log('module_weight changed:', val);
  //       this.convertData();
  //     },
  //     deep: true,
  //     immediate: true,
  //   },
  // }
};
</script>  

<style scoped>
/* 容器样式 */
.a2amoduldiference {
  padding: 20px;
  background-color: #f7f7f7;
  height: 100%;
  width: 98%;
  display: flex;
  flex-direction: column;
}

.top {
  height: 50%;
  width: 98%;
  overflow-y: auto;
}

.botton {
  margin-top: 1%;
  height: 50%;
  width: 100%;
  display: flex;
}

.botton-half {
  height: 100%;
  width: 50%;
  display: flex;
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
  /* margin-bottom: 20px; */
  height: 80%;
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
.shapes-container {
  display: flex;
}

.shape-item {
display: inline-flex;
align-items: center;
gap: 5px;
}

.shape-name {
  font-size: 14px;
  font-weight: bold;
  color: black;
  margin-right: 10px;
}

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

.btn {
padding: 8px 16px;
background-color: #2973B2;
color: #000;
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

