<template>
  <div class="EnerJava">
    <!-- 上方：文件上传部分 -->
    <div class="uploadContainer">
      <!-- 第二列：文件上传 -->
      <!-- <div class="uploadSection">
        <span class="uploadLabel">项目文件版本1：</span>
        <input
          type="file"
          class="hiddenInput"
          @change.prevent="handleDownFile"
          accept=".json"
        />
        <button class="uploadButton" @click="triggerIntrusive2">
          选择文件
        </button>
      </div> -->
      <!--div
      <label for="project_folder">Project Folder:</label>
      <input v-model="projectFolder" type="text" id="project_folder" placeholder="Enter project folder path">
    </div>
    <button @click="startSemanticAnalysis">Start Semantic Analysis</button>
    <button @click="startClustering">Start Clustering</button>
    <div v-if="resultMessage">
      <p>{{ resultMessage }}</p>
    </div>-->







    <!-- 第一个版本 -->
    <!-- <input v-model="repoUrl" placeholder="输入 Git 仓库 URL">
    <button @click="fetchRefs">获取分支和标签</button>

    <div v-if="branches.length > 0">
      <h3>分支列表</h3>
      <select v-model="selectedBranch">
        <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
      </select>
    </div>

    <div v-if="tags.length > 0">
      <h3>标签列表</h3>
      <select v-model="selectedTag">
        <option v-for="tag in tags" :key="tag" :value="tag">{{ tag }}</option>
      </select>
    </div> -->

      <!-- <div class="uploadContainer-half">
        <span style="color: black;margin-right: 2%;font-size: 38px">Git 仓库选择</span>
        <el-input style="width: 50%" v-model="repoUrl" placeholder="输入 Git 仓库 URL" />
        <button class="btn" style="width: 20%;margin-left: 1%" @click="fetchGitRefs">获取分支 & 标签</button>
      </div> -->
      <div class="uploadContainer-half" v-if="branches.length || tags.length">
          <span style="color: black;margin-right: 2%;font-size: 38px">Git 选择版本</span>
          <el-select v-model="selectedVersion" style="width: 50%" placeholder="请选择版本">
            <el-option-group label="分支">
              <el-option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}（分支）</el-option>
            </el-option-group>
            <el-option-group label="Tags">
              <el-option v-for="tag in tags" :key="tag" :value="tag">{{ tag }}（Tag）</el-option>
            </el-option-group>
          </el-select>
          <button class="btn" @click="submitVersion" style="width: 20%;margin-left: 1%">提交选择</button>
      </div>




    </div>
    <!-- 下方：内容展示部分 -->
    <div class="contentContainer">
      <!-- 集成的 Architecture 组件 -->
      <Architecture 
        :upstream-path="upstreamFilePath"
        :downstream-path="downstreamFilePath"
      />
      <!-- 显示生成完成 -->
      <div v-if="isCompleted" class="completedMessage">
        <h3>生成完毕！</h3>
      </div>
    </div>
  </div>
</template>

<script>
import Architecture from './DependencyGraph.vue'; // 引入 Architecture 组件
import axios from 'axios';
import EventBus from './eventBus';

export default {
  name: 'EnerJava',
  components: {
    Architecture,
  },
  data() {
    return {
      repoUrl: '',
      branches: [],
      tags: [],
      selectedVersion: '',
      selectedBranch: '',
      selectedTag: '',

      upstreamFilePath: '', // 上游项目路径
      downstreamFilePath: '', // 下游项目路径
      isCompleted: false, // 上传是否完成
      projectFolder: '',
      resultMessage: ''
    };
  },
  methods: {
    getGitData(){
      this.branches = EventBus.branches;
      this.tags = EventBus.tags;
      this.repoUrl = EventBus.repo_url;
    },  


    // async fetchRefs() {
    //   try {
    //     const response = await axios.post('http://localhost:5000/get_git_refs', { repo_url: this.repoUrl });
    //     this.branches = response.data.branches || [];
    //     this.tags = response.data.tags || [];
    //   } catch (error) {
    //     console.error("获取 Git 仓库信息失败", error);
    //   }
    // },


    async fetchGitRefs() {
      if (!this.repoUrl) {
        alert("请输入 Git 仓库 URL");
        return;
      }
      try {
        const response = await axios.post("http://localhost:5000/get_git_refs", {
          repo_url: this.repoUrl,
        });
        console.log("git_response.data:"+response.data);
        this.branches = response.data.branches || [];
        this.tags = response.data.tags || [];
        EventBus.branches = this.branches;
        EventBus.tags = this.tags;
      } catch (error) {
        alert("获取失败：" + (error.response?.data?.error || error.message));
      }
    },
    async submitVersion() {
      if (!this.selectedVersion) {
        alert("请选择一个版本");
        return;
      }
      try {
        const response = await axios.post("http://localhost:5000/select_version", {
          repo_url: this.repoUrl,
          selected_version: this.selectedVersion,
          
        });
        EventBus.sharedFile = response.data.run_clustering_modify_json
        console.log("EnerJavaleft_EventBus.sharedFile:"+EventBus.sharedFile);
        alert(response.data.message);
      } catch (error) {
        alert("提交失败：" + (error.response?.data?.error || error.message));
      }
    },




    // 文件上传
    async handleDownFile(event) {
      const file = event.target.files[0];

      // 通过事件总线共享文件
      EventBus.sharedFile = file;
      console.log("file:"+EventBus.sharedFile);
    },
    // 触发文件选择框
    triggerIntrusive2() {
      // 确保正确触发文件选择框
      this.$el.querySelector('.hiddenInput').click();
    },
    async startSemanticAnalysis() {
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
      const response = await fetch('http://localhost:5000/run_clustering', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ project_folder: this.projectFolder })
      });

      const data = await response.json();
      console.log("data.shareFile:"+data.sharedFile);
      console.log("this.projectFolder:"+this.projectFolder)
      if (data.error) {
        this.resultMessage = `Error: ${data.error}`;
        console.log("Error: "+data.error);
      } else {
        this.resultMessage = 'Clustering completed successfully!';
        EventBus.sharedFile = data.sharedFile;
        // EventBus.sharedFile = "D:\\SemArc_backend\\results\\"+ this.projectFolder + "\\"+this.projectFolder+"_GraphIDFunc.json";
        // console.log("Vue页面中EventBus.sharedFile:"+EventBus.sharedFile);
        // EventBus.sharedFile = "D:\\SemArc_backend\\results\\enre\\enre_GraphIDFunc.json"
      }
    }
  },
};
</script>

<style scoped>
/* 主容器 */
.EnerJava {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: rgb(255, 255, 255);
}

/* 文件上传部分 */
.uploadContainer {
  display: flex;
  flex-direction: column;
  /* justify-content: space-between; */
  /* align-items: center; */
  padding: 20px;
  background-color: white;
  border-bottom: 1px solid #ddd;
}

.uploadContainer-half {
  display: flex;
  width: 100%;
  height: 49%;
}

.uploadSection {
  display: flex;
  align-items: center;
  gap: 10px;
}

.uploadLabel {
  font-size: 16px;
  color: #333;
}

.uploadButton {
  padding: 10px 20px;
  font-size: 14px;
  color: #fff;
  background-color: #2973B2;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.uploadButton:hover {
  background-color: #9ACBD0;
}

.hiddenInput {
  display: none;
}

/* 内容展示部分 */
.contentContainer {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.completedMessage {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: rgb(32, 233, 79);
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


