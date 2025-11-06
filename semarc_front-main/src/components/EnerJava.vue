<template>
  <div class="EnerJava">
    <!-- 上方：文件上传部分 -->
    <div class="uploadContainer">
      <!-- 第二列：文件上传 -->
      <!-- <div class="uploadSection">
        <span class="uploadLabel">项目版本2json文件：</span>
        <input
          type="file"
          class="hiddenInput"
          @change.prevent="handleDownFile"
          accept=".json"
        />
        <button class="uploadButton" @click="triggerIntrusive2">
          选择文件
        </button>
      </div>
    </div> -->
    <!-- <div class="uploadContainer-half">
      <span style="color: black;margin-right: 2%;font-size: 38px">Git 仓库选择</span>
      <el-input style="width: 50%" v-model="repoUrl" placeholder="输入 Git 仓库 URL" />
      <button class="btn" style="width: 20%;margin-left: 1%" @click="fetchGitRefs">获取分支 & 标签</button>
    </div> -->
    <div class="uploadContainer-half" v-if="branches.length || tags.length">
        <span style="color: black;margin-right: 2%;font-size: 38px">Git 选择版本</span>
        <el-select v-model="selectedVersion" style="width: 50%" placeholder="请选择版本">
          <el-option-group label="分支" :key="branches">
            <el-option v-for="branch in branches" :key="branch" :value="branch" :label="branch">{{ branch }}（分支）</el-option>
          </el-option-group>
          <el-option-group label="Tags" :key="tags">
            <el-option v-for="tag in tags" :key="tag" :value="tag" :label="tag">{{ tag }}（Tag）</el-option>
          </el-option-group>
        </el-select>
        <button class="btn" @click="submitVersion" style="width: 20%;margin-left: 1%">提交选择</button>
    </div>
   

    
  </div>


    
    <!-- 下方：内容展示部分 -->
    <div class="contentContainer">
      <!-- 集成的 Architecture 组件 -->
      <Architectureright
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
import Architectureright from './DependencyGraphright.vue'; // 引入 Architecture 组件
import axios from 'axios';
import EventBus from './eventBus';
import PlantUMLViewer from '@/components/PlantUML.vue';

export default {
  name: 'EnerJava',
  components: {
    Architectureright,
    PlantUMLViewer
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
    };
  },
  methods: {
    getGitData(){
      this.branches = EventBus.branches;
      this.tags = EventBus.tags;
      this.repoUrl = EventBus.repo_url;
    },  


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
      } catch (error) {
        alert("获取失败：" + (error.response?.data?.error || error.message));
      }
    },
    async submitVersion() {
      // if (!this.selectedVersion) {
      //   alert("请选择一个版本");
      //   return;
      // }
      try {
        const response = await axios.post("http://localhost:5000/select_version_right", {
          repo_url: this.repoUrl,
          selected_version: this.selectedVersion,
        });
        EventBus.sharedFile = response.data.run_clustering_right_modify_json;
        alert(response.data.message);
      } catch (error) {
        alert("提交失败：" + (error.response?.data?.error || error.message));
      }
    },


    // 文件上传
    async handleDownFile(event) {
      const file = event.target.files[0];

      // 通过事件总线共享文件
      EventBusright.sharedFile = file;
      console.log("file:"+EventBusright.sharedFile);
    },
    // 触发文件选择框
    triggerIntrusive2() {
      // 确保正确触发文件选择框
      this.$el.querySelector('.hiddenInput').click();
    },
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

