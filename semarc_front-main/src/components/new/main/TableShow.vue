<template> 
  <div class="a2amoduldiference">
    <div style="margin-bottom: 10px;">
      <button class="btn" @click="exportToExcel">导出为Excel</button>
    </div>
    <div class="table-container" style="overflow-x: auto;">
      <el-table
          style="min-width:200px;"
          :data="tableDatashowBack_to_front"
          highlight-current-row
          
          :scrollbar="true"
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
          <el-table-column prop="version1_change_file_number" label="版本1文件移动数量" sortable width="200"></el-table-column>
          <el-table-column prop="version2_total_file_number" label="版本2模块文件总量" sortable width="200"></el-table-column>
          <el-table-column prop="version2_change_file_number" label="版本2文件移动数量" sortable width="200"></el-table-column>
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
</template>

<script>
import axios from 'axios';
import EventBus from '../../eventBus';
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'
export default {
  
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
    };
  },
  mounted(){
     this.convertData();
  },
  methods: {  
    exportToExcel() {
      // 1. 生成表头和数据
      const header = [
        '版本一', '版本二', 'V1模块文件总量', '版本1文件移动数量', '版本2模块文件总量', '版本2文件移动数量', 'a2a指标中各模块权重大小', '模块中文件代码修改量总和', 'commit历史中各模块权重大小'
      ];
      const data = this.tableDatashowBack_to_front.map(row => [
        row.version1,
        row.version2,
        row.version1_total_file_number,
        row.version1_change_file_number,
        row.version2_total_file_number,
        row.version2_change_file_number,
        row.a2a_weight,
        row.LOC,
        row.commit_weight,
      ]);
      data.unshift(header);

      // 2. 创建 worksheet 和 workbook
      const worksheet = XLSX.utils.aoa_to_sheet(data);
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

      // 3. 导出
      const wbout = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '指标历史变更分析.xlsx');
    },
    convertData(){
        console.log('Main - table')
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
      console.log('后端传给前端a2a表中的查看数据:', this.tableDatashowBack_to_front);
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
  background-color: #f7f7f7;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* 表格容器样式 */
.table-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: auto;
  padding: 0;
  margin: 0;
  min-width: 900px;
  /* 添加平滑滚动效果 */
  scroll-behavior: smooth;
  /* 添加自定义滚动条样式 */
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

/* 确保表格填充整个容器 */
.el-table {
  width: 100%;
  height: 100%;
  min-width: 800px;
}

/* 自定义滚动条样式 */
.table-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 确保表格单元格内容不换行 */
.el-table .cell {
  white-space: nowrap;
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
  background-color: #1abc9c;
}

.btn {
padding: 8px 16px;
background-color: #4caf50;
color: #000;
border: none;
border-radius: 6px;
font-size: 14px;
cursor: pointer;
transition: all 0.3s ease;
}

.btn:hover {
background-color: #45a049;
transform: translateY(-2px);
box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.btn:active {
transform: translateY(0);
}
</style>

