<template>
    <div class="table">
        <div id="app">
            <div class="table-container">
                <table border="1">
                    <thead>
                        <tr>
                            <th>{{temporary_info_name}}</th>
                            <th>{{temporary_info_type}}</th>
                            <th>{{temporary_children_type}}</th>
                            <th>{{temporary_children_name}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(person,index) in paginatedTableData()" 
                        :key="person.id"
                        :class="{ highlight: selectedRowIndex === index }"
                        @click="handleSearch()">
                            <td>{{ fix_table_name }}</td>
                            <td>{{ fix_table_function }}</td>
                            <td>{{ person.name }}</td>
                            <td>{{ person.function }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 分页控件 -->
            <div class="pagination">
                <button @click="prevPage" :disabled="currentPage === 1" class="pagination-button">上一页</button>
                <span class="pagination-button">第 {{ currentPage }} / {{ totalPages() }}</span>
                <button @click="nextPage" class="pagination-button">下一页</button>
            </div>
        </div>
    </div>
</template>

<script>
import EventBusTable from './eventbustable';  // 引入事件总线

export default {
  name: 'table',
  data() {
    return {
      fix_table_name: '',
      fix_table_function: '',
      temporary_info_name: '',
      temporary_info_type : '',
      temporary_children_name: '',
      temporary_children_type: '',
      temporary_children_info: [],
      currentPage: 1,
      itemsPerPage: 2,
      selectedRowIndex: null,
      current_file_name: '',
    }
  },
  mounted() {
    // 监听事件，接收传递过来的数据
    EventBusTable.$on('sendData', (data) => {
      console.log('Received data:', data);
      this.temporary_info_name = data.temporary_info_name;
      this.temporary_info_type = data.temporary_info_type;
      this.temporary_children_name = data.temporary_children_name;
      this.temporary_children_type = data.temporary_children_type;
      this.temporary_children_info = data.temporary_children_info;
      this.fix_table_name = data.fix_table_name;
      this.fix_table_function = data.fix_table_function;
      this.current_file_name=data.current_file_name; 
      this.selectedRowIndex=data.selectedRowIndex;
    });
  },
  destroyed() {
    // 清理事件监听，避免内存泄漏
    EventBusTable.$off('sendTableData');
  },
  methods: {
    totalPages() {
      return Math.ceil(this.temporary_children_info.length / this.itemsPerPage);
    },
    // 当前页显示的数据
    paginatedTableData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
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
    // 处理搜索
    handleSearch() {
      this.highlightRow(this.current_file_name);
    },
    // 高亮符合搜索条件的行
    highlightRow(query) {
      // 在所有数据中查找匹配的行
      console.log("query:"+query)
      const rowIndexInAllData = this.temporary_children_info.findIndex(
        item => item.name===query
      );
      console.log("rowIndexInAllData:"+rowIndexInAllData)
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
  }
};
</script>

<style scoped>
/* 设置表格容器的滚动 */
.table-container {
  width: 1550px;
  height: 70%; 
  margin-bottom: 10px;
  display: flex;
  justify-content: center; 
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  overflow-y: auto;  
}

/* 设置表格样式 */
table {
  width: 100%;
  border-collapse: collapse; /* 合并边框 */
  background-color: rgb(211, 205, 205); /* 设置表格背景色为白色 */
  color: black; /* 设置表格内字体颜色为黑色 */
  border: 1px solid black; /* 设置边框为黑色 */
  
}

/* 设置表头样式 */
th {
  padding: 10px;
  background-color: #f2f2f2; /* 设置表头背景颜色 */
  text-align: left;
  border: 1px solid black; /* 表头边框 */
}

/* 设置表格单元格样式 */
td {
  padding: 8px;
  text-align: left;
  border: 1px solid black; /* 单元格边框 */
}

/* 设置分页按钮样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  background-color: white;
}

.pagination-button {
  background-color: black; /* 设置按钮背景色为黑色 */
  color: white; /* 设置按钮字体颜色为白色 */
  border: none;
  padding: 5px 15px;
  margin: 0 10px;
  cursor: pointer;
  border-radius: 4px;
}

.pagination-button:disabled {
  background-color: grey; /* 设置禁用按钮的背景色 */
  cursor: not-allowed; /* 禁用按钮的鼠标样式 */
}
</style>
