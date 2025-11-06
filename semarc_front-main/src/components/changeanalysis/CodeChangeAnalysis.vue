<template> 
    <div class="a2amoduldiference">
      <!-- 第一个部分：搜索框和查看按钮 -->
      <div class="search-container">
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
      </div>
  
      <!-- 第二个部分：表格 -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>版本一</th>
              <th>版本二</th>
              <th>a2a</th>
              <th>commit分析</th>
              <th>加权</th>
            </tr>
          </thead>
          <tbody>
            <!-- 10行数据 -->
            <tr v-for="(row, index) in tableData" :key="index">
              <td>{{ row.versionChange }}</td>
              <td>{{ row.movementDistance }}</td>
              <td>{{ row.a2a }}</td>
              <td>{{ row.commitAnalysis }}</td>
              <td>{{ row.weight }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- 第三个部分：按钮容器 -->
      <div class="button-container">
        <button class="action-button" @click="navigateToCodeChangeAnalysis">代码变更分析</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        versionPath1: '',  // 版本1路径
        versionPath2: '',  // 版本2路径
        tableData: [       // 表格数据
          { versionChange: 'v1 -> v2', movementDistance: '10', a2a: '0.5', commitAnalysis: '20', weight: '0.4' },
          { versionChange: 'v1 -> v3', movementDistance: '15', a2a: '0.7', commitAnalysis: '25', weight: '0.6' },
          { versionChange: 'v2 -> v3', movementDistance: '12', a2a: '0.6', commitAnalysis: '15', weight: '0.5' },
          { versionChange: 'v3 -> v4', movementDistance: '20', a2a: '0.8', commitAnalysis: '30', weight: '0.7' },
          { versionChange: 'v1 -> v2', movementDistance: '11', a2a: '0.4', commitAnalysis: '12', weight: '0.3' },
          { versionChange: 'v2 -> v3', movementDistance: '13', a2a: '0.6', commitAnalysis: '18', weight: '0.6' },
          { versionChange: 'v3 -> v4', movementDistance: '18', a2a: '0.9', commitAnalysis: '28', weight: '0.9' },
          { versionChange: 'v1 -> v4', movementDistance: '14', a2a: '0.5', commitAnalysis: '22', weight: '0.4' },
          { versionChange: 'v2 -> v4', movementDistance: '19', a2a: '0.7', commitAnalysis: '27', weight: '0.8' },
          { versionChange: 'v1 -> v3', movementDistance: '10', a2a: '0.5', commitAnalysis: '20', weight: '0.5' }
        ]
      };
    },
    methods: {
      selectPath1() {
        console.log('查看版本路径1:', this.versionPath1);
      },
      selectPath2() {
        console.log('查看版本路径2:', this.versionPath2);
      },
      navigateToCodeChangeAnalysis() {
        // 使用编程式导航来跳转到新页面
        this.$router.push({ name: 'code-change-analysis' });
      }
    }
  };
  </script>  
  
  <style scoped>
  /* 容器样式 */
  .a2amoduldiference {
    padding: 20px;
    background-color: #f7f7f7;
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
  </style>
  
  