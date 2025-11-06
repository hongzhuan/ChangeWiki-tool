<template>
  <div class="CommonGitRes">
    <div class="uploadContainer"> 
        <div class="uploadContainer-half">
        <span style="color: black;margin-right: 2%;font-size: 38px">Git 仓库选择</span>
        <el-input style="width: 50%" v-model="repoUrl" placeholder="输入 Git 仓库 URL" />
        <button class="btn" style="width: 20%;margin-left: 1%" @click="fetchGitRefs">获取分支 & 标签</button>
        </div>
    </div>
    <!-- <div class="uploadContainer-half" style="margin-top: 2%" v-if="branches.length || tags.length">
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
    </div> -->
  </div>
</template>
<script>
import EventBus from './eventBus';
import axios from 'axios';
export default {
  name: 'CommonGitRes',
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
  inject: ['getGitData'],
  methods: {
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
        EventBus.repo_url = this.repoUrl;
        EventBus.branches = this.branches;
        EventBus.tags = this.tags;
        this.getGitData();
      } catch (error) {
        alert("获取失败：" + (error.response?.data?.error || error.message));
      }
    },
},
}


</script>
<style >
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
