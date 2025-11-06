<template>
  <div class="home-container" @click="createClickEffect">
    <div class="user-info" @click.stop="toggleUserMenu">
      <span class="avatar-emoji">👤</span>
      <span style="font-size: 1.2rem;
  color: #666;">{{ username }}</span>
    </div>
    <div v-if="showUserMenu" class="user-dropdown">
      <div class="dropdown-item" @click="goUserInfo" style="font-size: 1.2rem;
  color: #666;">用户信息</div>
      <div class="dropdown-item" @click="logout" style="font-size: 1.2rem;
  color: #666;">退出登录</div>
    </div>

    <div class="history-sidebar">
      <h3>历史分析</h3>
      <ul>
        <li v-for="item in historyList" :key="item.id" @click="selectHistory(item)" :class="{active: selectedHistory && selectedHistory.id === item.id}">
          <div class="history-title">{{ item.title }}</div>
          <div class="history-time">{{ item.time }}</div>
        </li>
      </ul>
    </div>
    <div class="welcome-section" @click.stop>
      <h1 class="welcome-title">欢迎使用架构分析工具</h1>
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
      <div class="gitSelect flex-align" v-if="show_version">
        <span class = "version_one_css label-align" style="font-family: 'Courier New', Courier, monospace;">版本1</span>
        <el-select v-model="selectedVersion1" style="width: 50%" placeholder="请选择版本1">
          <el-option-group label="分支" :key="branches">
            <el-option v-for="branch in branches" :key="branch" :value="branch" :label="branch">{{ branch }}（分支）</el-option>
          </el-option-group>
          <el-option-group label="Tags" :key="tags">
            <el-option v-for="tag in tags" :key="tag" :value="tag" :label="tag">{{ tag }}（Tag）</el-option>
          </el-option-group>
        </el-select>
      </div>
      
      <div class="gitSelect flex-align" v-if="show_version">
        <span class = "version_two_css label-align" style="font-family: 'Courier New', Courier, monospace;">版本2</span>
        <el-select v-model="selectedVersion2" style="width: 50%" placeholder="请选择版本2">
          <el-option-group label="分支" :key="branches">
            <el-option v-for="branch in branches" :key="branch" :value="branch" :label="branch">{{ branch }}（分支）</el-option>
          </el-option-group>
          <el-option-group label="Tags" :key="tags">
            <el-option v-for="tag in tags" :key="tag" :value="tag" :label="tag">{{ tag }}（Tag）</el-option>
          </el-option-group>
        </el-select>
      </div>

      <!-- 新增领域知识输入框 -->
      <div class="gitSelect flex-align" v-if="show_version">
        <span class = "version_two_css label-align" style="font-family: 'Courier New', Courier, monospace;">领域知识</span>
        <textarea
          v-model="domainKnowledge"
          placeholder="请输入领域知识"
          class="domain-input"
          rows="3"
          style="resize: vertical;"
        ></textarea>
      </div>

      <div v-if="show_version" style="width: 100%;display: flex;justify-content: center;">
        <button class="btn" style="width: 32%; color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" @click="submitVersion">开始分析</button>

          <!-- 进度条 -->
          <el-progress 
            v-if="progressVisible" 
            :percentage="progress" 
            status="active" 
            style="width: 50%;"
          />
          
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
      showUserMenu: false,
      username: localStorage.getItem("username") || "用户",
      /* 历史数据由后端取，先置空 */
      historyList: [],
      selectedHistory: null,
      domainKnowledge: '', // 新增领域知识输入框的绑定变量
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
      file_unit_operation_change_json:'',
      
      //进度条数据
      progress: 0, // 进度条的进度
      progressVisible: false, // 是否显示进度条
    }
  },
  created() {
    this.loadHistory()
    // /* 组件创建后立刻加载历史记录 */
    // const uname = localStorage.getItem('username')
    // if (uname) {
    //   try {
    //     const res = await fetch(`http://localhost:5000/api/history/${uname}`)
        
    //       this.historyList = await res.json()
    //       console.log('http://localhost:5000/api/history/加载历史记录:', this.historyList)
    //       EventBus.time = this.historyListtime // 同步到 EventBus

        
    //   } catch (e) {
    //     console.error('加载历史失败', e)
    //   }
    // }
  },
  methods: {
    
    // 用户信息相关
    logout() {
      localStorage.removeItem("isLogin");
      localStorage.removeItem("username");
      this.$router.push("/");
    },
    async loadHistory() {
         /* 组件创建后立刻加载历史记录 */
      const uname = localStorage.getItem('username')
      if (uname) {
        try {
          const res = await axios.post(`http://localhost:5000/api/history`,{
              username: uname
          })
          if (res.ok) {
            this.historyList = await res.json()
            console.log(`http://localhost:5000/api/history/${uname}/历史记录`, this.historyList[0].time)
            EventBus.time = this.historyList[0].time // 同步到 EventBus
          }
        } catch (e) {
          console.error('加载历史失败', e)
        }
      }
      },
    goUserInfo() {
      this.$router.push("/userInfo");
    },
    // 点击页面其它地方关闭菜单
    handleClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.showUserMenu = false;
      }
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    selectHistory(item) {
      this.selectedHistory = item;
      // 这里可以根据需要填充主界面内容
      // 例如 this.repoUrl = item.repoUrl;
    },
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

            /* ---------- ① 先把“分析记录”写进数据库 ---------- */
            try {
              const addRes = await fetch('http://localhost:5000/api/history', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  username: this.username,           // 当前登录用户名
                  projectUrl: this.repoUrl,          // 仓库 URL
                  version1:  this.selectedVersion1,  // 版本1
                  version2:  this.selectedVersion2,  // 版本2
                  domainKnowledge: this.domainKnowledge // 领域知识（可为空）
                })
              })

              if (addRes.status === 201) {
                const newItem = await addRes.json() // { id, title, time }
                /* 把最新记录插到 historyList 最前面 */
                this.historyList.unshift(newItem)
              } else {
                const msg = (await addRes.json()).message || '写入历史失败'
                console.warn(msg)
                // ❗ 写库失败不会阻塞后续分析，只是侧边栏不立即刷新
              }
            } catch (err) {
              console.error('写入历史时发生异常:', err)
            }

            // 显示进度条并初始化进度
              this.progressVisible = true;
              this.progress = 0;

            try {
                // 调用第一个版本的后端接口
                
                const response = await axios.post("http://127.0.0.1:5000/select_version", {
                    repo_url: this.repoUrl,
                    selected_version: this.selectedVersion1,
                    // domain_knowledge: this.domainKnowledge, // 新增
                });
                EventBus.sharedFile1 = response.data.run_clustering_modify_json
                console.log("EnerJavaleft_EventBus.sharedFile:"+EventBus.sharedFile1);
                // alert(response.data.message);
            } catch (error) {
                alert("提交失败：" + (error.response?.data?.error || error.message));
            } finally{
                this.progress = 20; // 更新进度
                this.getData1()
            }

            try {
                // 调用第二个版本的后端接口
                const response = await axios.post("http://127.0.0.1:5000/select_version_right", {
                    repo_url: this.repoUrl,
                    selected_version: this.selectedVersion2,
                });
                EventBus.sharedFile2 = response.data.run_clustering_right_modify_json;
                // alert(response.data.message);
                console.log("提交成功")
                // 更新进度到 100%
                
            } catch (error) {
                alert("提交失败：" + (error.response?.data?.error || error.message));
            } finally{
              this.progress = 40; // 更新进度
                this.getData2()
                this.showCodeChangeAnalysis();
                // this.showChangeAnalysis();
            }
            
        },
    createClickEffect(event) {
      // const emoji = this.emojis[Math.floor(Math.random() * this.emojis.length)]
      // const clickEffect = document.createElement('div')
      // clickEffect.className = 'click-effect'
      // clickEffect.textContent = emoji
      
      // const x = event.clientX
      // const y = event.clientY
      
      // clickEffect.style.left = `${x}px`
      // clickEffect.style.top = `${y}px`
      
      // document.body.appendChild(clickEffect)
      
      // setTimeout(() => {
      //   clickEffect.remove()
      // }, 1000)
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
        async showCodeChangeAnalysis() {
          try {
                const response = await fetch('http://localhost:5000/generate_code_changes', {
                    method: 'POST',
                });
                const result = await response.json();
                if (result.status === 'success') {

                }
            } catch (error) {
                alert('请求失败: ' + error);
            }finally {
                // this.$router.push({name:'ReverseAndChangesTotalPage'})
                this.progress = 80; // 更新进度
                this.showChangeAnalysis();
            }
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
                    EventBus.version1 = result.version1
                    EventBus.version2 = result.version2
                    console.log("EventBus.architecture1_change_json",EventBus.architecture1_change_json)
                    console.log("EventBus.architecture2_change_json",EventBus.architecture2_change_json)
                    console.log("EventBus.shareFile1",EventBus.sharedFile1)
                    console.log("a2a_tableInfo:")
                    console.log(result.a2a_tableInfo)
                    console.log('version1:', EventBus.version1);
                    console.log('version2:', EventBus.version2);
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
                this.progress = 100; // 更新进度
                this.$router.push({name:'ReverseAndChangesTotalPage'})
                // this.showCodeChangeAnalysis();
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
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeInDown 1s ease-out;
}

.version_two_css
{
  font-size: 1.2rem;
  color: #666;
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
  margin: 5px auto 10px auto;
  position: relative;
  margin-bottom: 10px;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out 0.6s both;
  justify-content: center; /* 水平居中 */
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

.domain-input {
  width: 50%;
  min-height: 80px;
  padding: 8px 11px;
  border: 1px solid #2973B2;
  border-radius: 4px;
  color: black;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  background:rgba(229, 232, 235, 0.9);
  font-size: 14px;
  font-family: 'Courier New', Courier, monospace;
  box-sizing: border-box;
  transition: border-color .2s cubic-bezier(.645,.045,.355,1);
  outline: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  text-align: left;
  resize: vertical;
}
.domain-input:focus {
  width: 50%;
  min-height: 40px;
  padding: 8px 11px;
  border: 1px solid rgba(229, 232, 235, 0.9);
  border-radius: 4px;
  color: black;
  background:rgba(229, 232, 235, 0.9);
  font-size: 14px;
  font-family: 'Courier New', Courier, monospace;
  box-sizing: border-box;
  transition: border-color .2s cubic-bezier(.645,.045,.355,1);
  outline: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  text-align: left;
  resize: vertical;
  vertical-align: middle;
}
.label-align {
  display: inline-block;
  min-width: 90px;
  text-align: left;
  font-family: 'Courier New', Courier, monospace;
  font-size: 1.2rem;
  color: #666;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  animation: fadeInDown 1s ease-out;
  margin-right: 5px;
}


.flex-align {
  display: flex;
  align-items: flex-start; /* 顶部对齐，方便多行textarea */
  gap: 10px;
}

.avatar-emoji {
  font-size: 28px;
  margin-right: 8px;
  vertical-align: middle;
}
.user-info {
  position: absolute;
  top: 24px;
  right: 36px;
  display: flex;
  align-items: center;
  cursor: pointer;
  background: #f5f5f5;
  border-radius: 18px;
  padding: 4px 12px;
  z-index: 100;
}
.user-dropdown {
  position: absolute;
  top: 56px; /* 距离顶部略大于 .user-info */
  right: 36px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  min-width: 120px;
  z-index: 101;
  margin:2px
}


.dropdown-item {
  padding: 12px 18px;
  cursor: pointer;
  font-size: 1.2rem;
  color: #666;
  transition: background 0.2s;
}

.dropdown-item + .dropdown-item {
  margin-top: 10px; /* 两项之间增加10px间隔 */
}

.dropdown-item:hover {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.history-sidebar {
  position: fixed;
  top: 0.5rem;
  left: 24px;
  width: 240px;
  height: 94vh;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 18px rgba(41, 115, 178, 0.10);
  padding: 24px 16px 16px 16px;
  z-index: 20;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.history-sidebar h3 {
  font-size: 1.2rem;
  margin-bottom: 18px;
  color: #2973B2;
  text-align: center;
}

.history-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.history-sidebar li {
  padding: 10px 8px;
  margin-bottom: 10px;
  border-radius: 8px;
  cursor: pointer;
  background: #f7f8fa;
  transition: background 0.2s, border 0.2s;
  border: 1px solid transparent;
}

.history-sidebar li.active,
.history-sidebar li:hover {
  background: #e6f0fa;
  border: 1px solid #2973B2;
}

.history-title {
  font-weight: bold;
  font-size: 1rem;
  color: #333;
}

.history-time {
  font-size: 0.85rem;
  color: #888;
  margin-top: 2px;
}
</style>
