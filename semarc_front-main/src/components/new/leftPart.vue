<template>
    <div class="mainContainer">
        <div class="top">
            <strong class="title">分析项目选择</strong>
            <div class="gitSelect">
                <span style="font-size: 1rem;">Git 路径</span>
                <el-input style="width: 50%;" v-model="repoUrl" placeholder="输入 Git 仓库 URL" />
                <button class="btn" style="width: 24%;margin-left: 1%" @click="fetchGitRefs">获取分支</button>
            </div>

            <div class="gitSelect">
                <span style="font-size: 1rem;">版本1分支</span>
                <el-select v-model="selectedVersion1" style="width: 50%" placeholder="请选择版本1">
                    <el-option-group label="分支" :key="branches">
                        <el-option v-for="branch in branches" :key="branch" :value="branch" :label="branch">{{ branch }}（分支）</el-option>
                    </el-option-group>
                    <el-option-group label="Tags" :key="tags">
                        <el-option v-for="tag in tags" :key="tag" :value="tag" :label="tag">{{ tag }}（Tag）</el-option>
                    </el-option-group>
                </el-select>
            </div>
            
            <div class="gitSelect">
                <span style="font-size: 1rem;">版本2分支</span>
                <el-select v-model="selectedVersion2" style="width: 50%" placeholder="请选择版本2">
                    <el-option-group label="分支" :key="branches">
                        <el-option v-for="branch in branches" :key="branch" :value="branch" :label="branch">{{ branch }}（分支）</el-option>
                    </el-option-group>
                    <el-option-group label="Tags" :key="tags">
                        <el-option v-for="tag in tags" :key="tag" :value="tag" :label="tag">{{ tag }}（Tag）</el-option>
                    </el-option-group>
                </el-select>
            </div>
            <div style="width: 100%;display: flex;justify-content: center;">
                <button class="btn" style="width: 32%;margin-top:2%" @click="submitVersion">确认上传</button>
            </div>
        </div>
        <div class="middle">
            <strong class="title">系统配置选择</strong>
            <div class="gitSelect">
                <span style="font-size: 1rem;">大模型选择</span>
                <el-select v-model="largeModel" style="width: 50%;" placeholder="请选择大模型">
                    <el-option v-for="item in largeModelOption" :key="item" :value="item" :label="item">{{ item }}</el-option>
                </el-select>
            </div>
            <div class="gitSelect">
                <span style="font-size: 1rem;">逆向分辨率</span>
                <el-select v-model="resolution" style="width: 50%" placeholder="请选择架构逆向分辨率">
                    <el-option v-for="item in resolutionOption" :key="item" :value="item" :label="item">{{ item }}</el-option>
                </el-select>
            </div>
            <div class="gitSelect">
                <span style="font-size: 1rem;">先验知识</span>
                <el-select v-model="resolution" style="width: 50%" placeholder="（待做）用户可以上传包含该软件先验知识的文档">
                    <el-option v-for="item in resolutionOption" :key="item" :value="item" :label="item">{{ item }}</el-option>
                </el-select>
            </div>
            <div class="gitSelect">
                <span style="font-size: 1rem;">先验知识</span>
                <el-input style="width: 70%;" v-model="repoUrl" placeholder="（待做）用户可以输入先验知识" />
            </div>
        </div>
        <div class="bottom">
            <strong class="title">项目结构展示</strong>

            <div class="gitSelect">
                <span style="font-size: 1rem;">版本一</span>
            </div>
            <el-tree 
              :data="data1"
              :props="defaultProps"
              node-key="id"
              highlight-current
              :expand-on-click-node="false"
            >
              <template v-slot="{ data }">
                <span>
                  <span :style="{ color: data.color }">{{ data.name }}</span>
                  <span style="margin-left: 10px; font-size: 12px; color: #666;">({{ data.category }})</span>
                </span>
              </template>
            </el-tree>

            <div class="gitSelect">
                <span style="font-size: 1rem;">版本二</span>
            </div>
            <el-tree 
              :data="data2"
              :props="defaultProps"
              node-key="id"
              highlight-current
              :expand-on-click-node="false"
            >
              <template v-slot="{ data }">
                <span>
                  <span :style="{ color: data.color }">{{ data.name }}</span>
                  <span style="margin-left: 10px; font-size: 12px; color: #666;">({{ data.category }})</span>
                </span>
              </template>
            </el-tree>
        </div>
    </div>
</template>

<script>
import EventBus from '../eventBus';
import axios from 'axios';

export default {
    name: 'LeftPart',
    data() {
        return {
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
        };
    },
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
                const response = await axios.post("http://localhost:5000/select_version", {
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
                const response = await axios.post("http://localhost:5000/select_version_right", {
                    repo_url: this.repoUrl,
                    selected_version: this.selectedVersion2,
                });
                EventBus.sharedFile2 = response.data.run_clustering_right_modify_json;
                alert(response.data.message);
            } catch (error) {
                alert("提交失败：" + (error.response?.data?.error || error.message));
            } finally{
                this.getData2()
            }
            this.showChangeAnalysis();
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
        
    },
}
</script>

<style scoped>
.mainContainer {
    width: 100%;
    height: 100%;
    display: flex;
}

.top {
    height: 25%;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.middle {
    height: 25%;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.bottom {
    height: 50%;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.title {
    color: black;
    font-size: 1.5rem;
    margin: 4% 0 0 4%;
    display: flex;
    font-family: 'Microsoft YaHei';
}


.gitSelect {
    width: 100%;
    display: flex;
    /* margin: 1%; */
    font-family: 'Microsoft YaHei';
    align-items: center;
    margin-top:2%;
}

.gitSelect span {
    color: black;
    font-size: 1.25rem;
    margin: 1%;
    width: 22%;
    font-family: 'Microsoft YaHei';
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