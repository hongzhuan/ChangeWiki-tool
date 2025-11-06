<template>
  <div class="mainContainer">
    <div class="header">
      <div class="navButton-div">
        <button 
          class="navButton" 
          :class="{ navButtonActive: isReverseActive }"
          @click="toggleReverse"
        >
          架构逆向
        </button>
        <button 
          class="navButton" 
          :class="{ navButtonActive: isChangeAnalysisActive }"
          @click="showChangeAnalysis"
        >
          变更分析
        </button>
      </div>
    </div>
    <!-- 左侧菜单部分 -->
    <!-- <div class="menuSection"> -->
      <!-- <div class="searchContainer">          
        <div class="searchItem">
          <input v-model="projectFolder" type="text" id="project_folder" placeholder="输入项目文件夹路径">
        </div>
        <div v-if="resultMessage">
          <p>{{ resultMessage }}</p>
        </div>
      </div> -->
      
        <!-- <div class="buttonContainer"> -->
        <!-- <div class="buttonRow">        
          <button class="menuButton" @click="startSemanticAnalysis">代码摘要</button>
          <button class="menuButton" @click="startClustering">LLM架构模式识别</button>
        </div> -->
        <!-- <div class="buttonRow">
          <button 
            class="menuButton" 
            :class="{ activeButton: isReverseActive }"
            @click="toggleReverse"
          >
            架构逆向
          </button>
          <button 
            class="menuButton" 
            :class="{ activeButton: isChangeAnalysisActive }"
            @click="showChangeAnalysis"
          >
            变更分析
          </button>
        </div>
        </div>
    </div> -->

    <!-- 右侧内容部分 -->
    <div class="contentSection">
      <router-view name="right"></router-view>
      <!-- 原架构逆向内容部分：仅在点击“架构逆向”按钮时显示 -->
      
      <div v-show="activeComponent === 'reverse'" class="contentTop">
      <div class="commonGitRes">
          <CommonGitRes />
      </div>
        <div class="showRow">
            <div class="contentLeft">
            <EnerJavaleft @updateData="handleDataUpdateleft" ref="childEnerLeft"/>
          </div>
          <div class="contentRight">
            <EnerJava @updateData="handleDataUpdate" ref="childEnerRight"/>
          </div>
        </div>
      </div>

      <!-- 变更分析内容部分：仅在点击“变更分析”按钮时显示 -->
      <div v-show="activeComponent === 'changeAnalysis'" class="contentchange">
        <!-- 第一个空白容器 -->
        <div class="emptyContainer">
          <a2amoduldiference ref="childRef"/>
        </div>
        
        <!-- 第二个空白容器 -->
        <!-- <div class="emptyContainer">
          <architecturechangegraph />
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import EnerJava from '@/components/EnerJava.vue';
import EnerJavaleft from '@/components/EnerJavaleft.vue';
import a2amoduldiference from '@/components/changeanalysis/a2amoduldiference.vue';
import EventBus from '../components/eventBus';
import architecturechangegraph from '@/components/changeanalysis/architecture_change_graph.vue'
import CommonGitRes from '@/components/CommonGitRes.vue';




export default {
  name: 'HomePage',
  components: {
    EnerJava,
    EnerJavaleft,
    a2amoduldiference,
    architecturechangegraph,
    CommonGitRes,
  },
  data() {
    return {
      activeComponent: '',
      isReverseActive: false,         // 用于控制架构逆向功能的显示状态
      isChangeAnalysisActive: false,  // 用于控制变更分析内容的显示
      versionPath1: '',              // 第一个版本路径
      versionPath2: '',              // 第二个版本路径
      projectFolder: '',
      resultMessage: '',
      a2a_value : '',
      module_weight : '',
      architecture1_change_json : '',
      file_unit_operation_change_json:''
    };
  },
  provide() {
    return {
      getGitData: this.getGitData,
    };
  },
  methods: {
    getGitData(){
      this.$refs.childEnerLeft.getGitData();
      this.$refs.childEnerRight.getGitData();
    },
    // 切换架构逆向功能的显示状态
    toggleReverse() {
      this.isReverseActive = true;
      this.isChangeAnalysisActive = false;  // 点击架构逆向时隐藏变更分析
      this.setActiveComponent('reverse');
    },
    setActiveComponent(component)
    {
      // 设置当前活动组件
      this.activeComponent = component;
    },
    // 选择第一个版本路径
    selectPath1() {
      console.log('选择了版本路径1:', this.versionPath1);
    },
    // 选择第二个版本路径
    selectPath2() {
      console.log('选择了版本路径2:', this.versionPath2);
    },
    // 显示变更分析页面
    // showChangeAnalysis() {
    //   this.isChangeAnalysisActive = true;
    //   this.isReverseActive = false;  // 点击变更分析时隐藏架构逆向
    // },
    async startSemanticAnalysis() {
      // this.isChangeAnalysisActive = false;
      // this.isReverseActive = true;  // 点击变更分析时隐藏架构逆向
      //http://localhost:5000/get_semantic
      this.setActiveComponent('reverse')
      const response = await fetch('http://localhost:5000/get_semantic', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ project_folder: this.projectFolder })
      });

      const data = await response.json();
      if (data.error) {
        this.resultMessage = `Error: ${data.error}`;
      } else {
        this.resultMessage = `Semantic analysis completed: Code semantics saved to ${data.code_sem_file}, Architecture semantics saved to ${data.arch_sem_file}`;
      }
    },

    async startClustering() {
      // this.isChangeAnalysisActive = false;
      // this.isReverseActive = true;  // 点击变更分析时隐藏架构逆向
      //localhost:5000
      this.setActiveComponent('reverse')
      const response = await fetch('http://localhost:5000/run_clustering', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ project_folder: this.projectFolder })
      });

      const data = await response.json();
      console.log("hahhaa:"+data);
      console.log("reverse_layer_graph:"+data.reverse_layer_graph);
      console.log("data.shareFile:"+data.sharedFile);
      console.log("this.projectFolder:"+this.projectFolder)
      if (data.error) {
        this.resultMessage = `Error: ${data.error}`;
        console.log("Error: "+data.error);
      } else {
        this.resultMessage = 'Clustering completed successfully!';
        if(this.resultMessage!='')
        {
          alert("json文件已生成！");
        }
        EventBus.sharedFile = data.sharedFile;
        // EventBus.sharedFile = "D:\\SemArc_backend\\results\\"+ this.projectFolder + "\\"+this.projectFolder+"_GraphIDFunc.json";
        // console.log("Vue页面中EventBus.sharedFile:"+EventBus.sharedFile);
        // EventBus.sharedFile = "D:\\SemArc_backend\\results\\enre\\enre_GraphIDFunc.json"
      }
    },
    async showChangeAnalysis() {
      this.isChangeAnalysisActive = true;
      this.isReverseActive = false;  // 点击变更分析时隐藏架构逆向
            try {
                const response = await fetch('http://localhost:5000/compare_architecture_change', {
                    method: 'POST',
                    // body: new FormData(document.getElementById('uploadForm'))
                });
                
                const result = await response.json();
                if (result.status === 'success') {
                    // populateTable(result.data);
                    console.log(result)
                    this.a2a_value = result.a2a_value
                    this.module_weight = result.module_weight
                    // this.architecture_change_json = result.architecture1_change_json
                    this.file_unit_operation_change_json = result.file_unit_operation_change_json
                    EventBus.module_weight = result.module_weight
                    this.architecture1_change_json = result.architecture1_change_json
                    EventBus.architecture1_change_json = result.architecture1_change_json
                    EventBus.architecture2_change_json = result.architecture2_change_json
                    EventBus.a2a_tableInfo = result.a2a_tableInfo
                    EventBus.a2a_tableInfo_json_add_fileInfo = result.a2a_tableInfo_json_add_fileInfo
                    console.log("a2a_tableInfo:")
                    console.log(result.a2a_tableInfo)
                    // console.log("architecture1_change_json:")
                    // console.log(this.architecture1_change_json)
                    // console.log("architecture2_change_json:")
                    // console.log(result.architecture2_change_json)
                    // console.log("file_unit_operation_change_json:")
                    // console.log(this.file_unit_operation_change_json)
                    // console.log("Home EventBus module_weight")
                    // console.log(EventBus.module_weight)
                    // console.log(result.module_weight)
                } else {
                    alert('错误: ' + result.message);
                    console.log(result)
                }
            } catch (error) {
                alert('请求失败: ' + error);
            } finally {
                console.log('showChangeAnalysis activeComponent 1', this.activeComponent)
                this.setActiveComponent('changeAnalysis');
                this.$refs.childRef.convertData();
                console.log('showChangeAnalysis activeComponent', this.activeComponent)
            }
        }

  },
};
</script>

<style scoped>
/* 主容器布局 */
.mainContainer {
  height: 100%;
  width: 100%;
  display: inline-block;
  overflow-y: auto;
  background-color: #F1F0E8;
}

/* 左侧菜单部分 */
.menuSection {
  width: 300px;
  background-color: #2c3e50;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* padding: 20px; */
  gap: 10px;
}

/* 搜索框和按钮的样式 */
.searchContainer {
  margin:20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.searchItem {
  display: flex;
  gap: 10px;
  width: 100%;
}

.searchItem input {
  flex: 1;
  padding: 5px;
  font-size: 14px;
}

.selectButton {
  padding: 6px 12px;
  background-color: #34495e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.selectButton:hover {
  background-color: #9ACBD0;
}

.selectButton:active {
  transform: scale(0.95);
}

/* 空容器样式 */
.emptyContainer {
  height: 100%;
  width: 100%;
  background-color: white;
  overflow-y: auto;
}

/* 按钮容器样式 */
.buttonContainer {
  /* margin:20px; */
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

/* 按钮行（每行最多两个按钮） */
.buttonRow {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.menuButton {
  width: 48%; /* 每个按钮占据 48% 的宽度 */
  padding: 10px 15px;
  font-size: 16px;
  color: white;
  background-color: #34495e;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.menuButton:hover {
  background-color: #9ACBD0;
}

.activeButton {
  background-color: #e74c3c; /* 激活状态的按钮颜色 */
}

.menuButton:active {
  transform: scale(0.95);
}

/* 右侧内容部分 */
.contentSection {
  flex: 1;
  display: flex;
  flex-direction: column; /* 垂直排列 */
  overflow-y: auto;
}
.showRow {
  flex: 1;
  display: flex;
  flex-direction: row; /* 垂直排列 */
  /* gap: 20px; */
  /* padding: 20px; */
  background-color: #F1F0E8;
  border-bottom: 1px solid #ddd;
  overflow-y: auto; 
}
/* 右上内容部分 */
.contentTop {
  flex: 1;
  display: flex;
  flex-direction: column; /* 垂直排列 */
  gap: 10px;
  /* padding: 20px; */
  background-color: #F1F0E8;
  border-bottom: 1px solid #ddd;
  overflow-y: auto; 
}

.commonGitRes {
  
  /* display: flex; */
  flex-direction: column; /* 垂直排列 */
  width: 100%;
  align-items: center;
  /* margin-top: 10%; */
  padding: 10px;
  border-right: 1px solid #ddd;
  background-color: #ffffff;
}

/* 左侧部分 */
.contentLeft {
  flex: 1; /* 占据一半宽度 */
  padding: 10px;
  border-right: 1px solid #ddd;
  background-color: #ffffff;
}

/* 右侧部分 */
.contentRight {
  flex: 1; /* 占据一半宽度 */
  padding: 10px;
  background-color: #ffffff;
}

.contentchange {
  flex: 1;
  display: flex;
  flex-direction: column; /* 垂直排列 */
  gap: 20px;
  padding: 20px;
  background-color: #F1F0E8;
  border-bottom: 1px solid #ddd;
  overflow-y: auto;
}

.aside .el-menu-item {
  font-size: 40px;
  width: 100%;
  height: 10%;
  margin-top: 10%;
}
</style>
