<template>
  <div class="home-container" @click="createClickEffect">
    <div class="welcome-section" @click.stop>
      <h1 class="welcome-title">欢迎使用胡杨林项目</h1>
      <p class="welcome-subtitle">请输入需要分析的项目仓库？</p>
    </div>
    
    <div class="search-container" @click.stop>
      <div class="search-box">
        <input 
          type="text" 
          class="search-input" 
          placeholder="路径输入..."
          v-model="repoUrl"
          @keyup.enter="handleSearch"
        />
        <button class="search-button" @click="fetchGitRefs">
          <span class="search-icon">🔍</span>
        </button>
      </div>
      <div class="gitSelect" v-if="show_version">
        <span class = "version_one_css">版本1</span>
        <el-select v-model="selectedVersion1" style="width: 50%" placeholder="请选择版本1">
          <el-option-group label="分支" :key="branches">
            <el-option v-for="branch in branches" :key="branch" :value="branch" :label="branch">{{ branch }}（分支）</el-option>
          </el-option-group>
          <el-option-group label="Tags" :key="tags">
            <el-option v-for="tag in tags" :key="tag" :value="tag" :label="tag">{{ tag }}（Tag）</el-option>
          </el-option-group>
        </el-select>
      </div>
      
      <div class="gitSelect" v-if="show_version">
        <span class = "version_two_css">版本2</span>
        <el-select v-model="selectedVersion2" style="width: 50%" placeholder="请选择版本2">
          <el-option-group label="分支" :key="branches">
            <el-option v-for="branch in branches" :key="branch" :value="branch" :label="branch">{{ branch }}（分支）</el-option>
          </el-option-group>
          <el-option-group label="Tags" :key="tags">
            <el-option v-for="tag in tags" :key="tag" :value="tag" :label="tag">{{ tag }}（Tag）</el-option>
          </el-option-group>
        </el-select>
      </div>
      <div v-if="show_version" style="width: 100%;display: flex;justify-content: center;">
        <button class="btn" style="width: 32%;" @click="submitVersion">开始逆向</button>
      </div>
    </div>
  </div>
</template>

<script>
import EventBus from '../components/eventBus';
import axios from 'axios';
export default {
  name: 'HomePage',
  data() {
    return {
      show_version : false,
      emojis: ['✨', '🌟', '💫', '⭐', '🎈', '🎀', '🌸', '🌺', '🌼', '🍀'],
      repoUrl: '',
      branches: [],
      tags: [],
      selectedVersion1: null,
      selectedVersion2: null,

      largeModel: null,
      largeModelOption: ['ChatGPT', 'CNN'],
      resolution: null,
      resolutionOption: ['0.1', '0.5'],

      data1: null,
      jsonData1: null,
      data2: null,
      jsonData2: null,
      defaultProps: {
        label: "name",
        children: "children"
       },


      versionPath1: '',              // 第一个版本路径
      versionPath2: '',              // 第二个版本路径
      projectFolder: '',
      resultMessage: '',
      a2a_value : '',
      module_weight : '',
      architecture1_change_json : '',
      file_unit_operation_change_json:''
    }
  },
  methods: {
    async fetchGitRefs() {
      if (!this.repoUrl) {
                alert("请输入 Git 仓库 URL");
                return;
            }
            try {
                const response = await axios.post("http://127.0.0.1:5000/get_git_refs", {
                    repo_url: this.repoUrl,
                });
                console.log("git_response.data:"+response.data);
                this.branches = response.data.branches || [];
                this.tags = response.data.tags || [];
                if(this.branches!=[]||this.tags!=[])
                  {
                    this.show_version=true
                  }
            } catch (error) {
                alert("获取失败：" + (error.response?.data?.error || error.message));
            }
    },
    async submitVersion() {
            if (!this.repoUrl) {
                alert("请输入 Git 仓库 URL");
                return;
            }
            if (!this.selectedVersion1) {
                alert("版本1 未选择");
                return;
            }
            if (!this.selectedVersion2) {
                alert("版本2 未选择");
                return;
            }

            try {
                const response = await axios.post("http://127.0.0.1:5000/select_version", {
                    repo_url: this.repoUrl,
                    selected_version: this.selectedVersion1,
                });
                EventBus.sharedFile1 = response.data.run_clustering_modify_json
                console.log("EnerJavaleft_EventBus.sharedFile:"+EventBus.sharedFile1);
                alert(response.data.message);
            } catch (error) {
                alert("提交失败：" + (error.response?.data?.error || error.message));
            } finally{
                this.getData1()
            }

            try {
                const response = await axios.post("http://127.0.0.1:5000/select_version_right", {
                    repo_url: this.repoUrl,
                    selected_version: this.selectedVersion2,
                });
                EventBus.sharedFile2 = response.data.run_clustering_right_modify_json;
                alert(response.data.message);
                console.log("提交成功")
            } catch (error) {
                alert("提交失败：" + (error.response?.data?.error || error.message));
            } finally{
                this.getData2()
                this.$router.push({name:'ReverseAndChangesTotalPage'})
            }
            this.showChangeAnalysis();
        },
    createClickEffect(event) {
      const emoji = this.emojis[Math.floor(Math.random() * this.emojis.length)]
      const clickEffect = document.createElement('div')
      clickEffect.className = 'click-effect'
      clickEffect.textContent = emoji
      
      const x = event.clientX
      const y = event.clientY
      
      clickEffect.style.left = `${x}px`
      clickEffect.style.top = `${y}px`
      
      document.body.appendChild(clickEffect)
      
      setTimeout(() => {
        clickEffect.remove()
      }, 1000)
    },
    async getData1() {
            this.jsonData1 = EventBus.sharedFile1
            if (!this.jsonData1) {
                return;
            }
            this.jsonData1 = this.jsonData1["structure"];

            let tree = [];
            let map = {};

            // 先创建 id -> 节点的映射
            this.jsonData1.forEach(item => {
                map[item.id] = { 
                    ...item, 
                    category: item.category === "item" ? "file" : item.category, // 替换 category
                    color: item.color ? item.color : "black",
                    children: [] 
                };
            });

            // 组装树结构
            this.jsonData1.forEach(item => {
                if (item.parentId === -1) {
                    tree.push(map[item.id]); // 根节点
                } else  {
                if (map[item.parentId]) {
                    map[item.parentId].children.push(map[item.id]); // 追加到父节点的 children
                }
                }
            });

            this.data1 = tree;
            
        },
        async getData2() {
            this.jsonData2 = EventBus.sharedFile2
            if (!this.jsonData2) {
                return;
            }
            this.jsonData2 = this.jsonData2["structure"];

            let tree = [];
            let map = {};

            // 先创建 id -> 节点的映射
            this.jsonData2.forEach(item => {
                map[item.id] = { 
                    ...item, 
                    category: item.category === "item" ? "file" : item.category, // 替换 category
                    color: item.color ? item.color : "black",
                    children: [] 
                };
            });

            // 组装树结构
            this.jsonData2.forEach(item => {
                if (item.parentId === -1) {
                    tree.push(map[item.id]); // 根节点
                } else {
                if (map[item.parentId]) {
                    map[item.parentId].children.push(map[item.id]); // 追加到父节点的 children
                }
                }
            });

            this.data2 = tree;
        },
    async showChangeAnalysis() {
    
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
                    this.$emit('left-done'); // 触发父组件的事件
                } else {
                    alert('错误: ' + result.message);
                    console.log(result)
                }
            } catch (error) {
                alert('请求失败: ' + error);
            } finally {
                
            }
        },
        
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.home-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
  animation: backgroundMove 20s linear infinite;
}

@keyframes backgroundMove {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 100% 100%;
  }
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
}

.welcome-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeInDown 1s ease-out;
}
.version_one_css {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeInDown 1s ease-out;
}

.version_two_css
{
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeInDown 1s ease-out;
}

.welcome-subtitle {
  font-size: 1.2rem;
  color: #666;
  animation: fadeInUp 1s ease-out 0.3s both;
}

.search-container {
  width: 100%;
  max-width: 600px;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out 0.6s both;
}

.gitSelect {
  width: 100%;
  max-width: 500px;
  margin-top: 5px;
  margin-bottom: 10px;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out 0.6s both;
}

.search-box {
  display: flex;
  background: white;
  border-radius: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.search-input {
  flex: 1;
  padding: 15px 20px;
  border: none;
  outline: none;
  font-size: 1.1rem;
}

.search-button {
  padding: 0 20px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-icon {
  font-size: 1.2rem;
}

.search-input:focus {
  outline: none;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
  }
  
  .search-container {
    width: 90%;
  }
}

.click-effect {
  position: fixed;
  pointer-events: none;
  font-size: 2rem;
  animation: clickAnimation 1s ease-out forwards;
  z-index: 9999;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

@keyframes clickAnimation {
  0% {
    transform: scale(0.5) translateY(0);
    opacity: 1;
  }
  50% {
    transform: scale(1.2) translateY(-20px);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.5) translateY(-40px);
    opacity: 0;
  }
}
</style>
