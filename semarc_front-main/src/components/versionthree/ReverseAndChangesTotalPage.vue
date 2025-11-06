<template>
  <div class="vscode-layout">
    
    <!-- 左侧树形结构 -->
    <div class="sidebar" :style="{ width: sidebarWidth + 'px' }">
      <div class="user-info" @click.stop="toggleUserMenu">
        <span class="avatar-emoji">👤</span>
        <span style=" width: 40%; color: white; border-color: white; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;">{{ username }}</span>
      </div>
      <div v-if="showUserMenu" class="user-dropdown">
        <div class="dropdown-item" @click="goUserInfo" style=" width: 40%; color: white; border-color: white; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;">用户信息</div>
        <div class="dropdown-item" @click="logout" style=" width: 40%; color: white; border-color: white; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;">退出登录</div>
      </div>
      <div class="tree-container">
        <div class="tree-header">
          <div class="header-row">
          <svg t="1750470595517" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4829" width="24" height="24"><path d="M870.627556 589.198222h-105.130667v-17.635555a78.734222 78.734222 0 0 0-77.937778-78.336c-29.184-0.227556-58.481778 0-87.779555 0H533.504v-56.206223h92.899556c30.72 0 55.580444-24.803556 55.580444-55.523555V154.282667a55.523556 55.523556 0 0 0-55.466667-55.466667h-226.986666a55.580444 55.580444 0 0 0-55.523556 55.466667v226.986666c0 30.606222 24.803556 55.409778 55.466667 55.523556h89.6v56.32H335.644444a82.147556 82.147556 0 0 0-26.965333 3.868444c-23.210667 8.021333-41.415111 26.168889-49.436444 49.436445-4.209778 12.060444-3.868444 24.689778-3.868445 37.262222v3.925333H153.372444a55.637333 55.637333 0 0 0-55.580444 55.409778v226.986667a55.182222 55.182222 0 0 0 55.523556 55.523555h226.986666c30.72 0 55.523556-24.803556 55.523556-55.523555v-226.986667a55.466667 55.466667 0 0 0-55.523556-55.523555h-80.782222v-15.473778a64.625778 64.625778 0 0 1 0.284444-6.257778c0.113778-0.455111 0.113778-0.853333 0.113778-1.365333v0.796444c0.568889-2.844444 1.479111-5.688889 2.503111-8.419555a44.032 44.032 0 0 1 2.958223-5.12c0.739556-1.024 1.536-1.934222 2.104888-3.072l-0.512 0.910222 0.113778-0.113778c1.536-1.706667 3.185778-3.185778 4.835556-4.778667l1.592889-1.194666c1.706667-1.137778 3.413333-2.104889 5.290666-3.015111l-1.024 0.227555c1.024-0.227556 1.934222-0.739556 2.901334-1.137778 2.218667-0.682667 4.551111-1.251556 6.826666-1.763555l2.616889-0.341334h360.049778l1.934222 0.113778 0.910222 0.227556a56.888889 56.888889 0 0 1 5.859556 1.592889c1.194667 0.398222 2.275556 0.967111 3.527111 1.308444l-0.910222-0.227555c2.275556 1.194667 4.551111 2.503111 6.599111 3.925333l0.796444 0.682667 4.323556 4.209777 0.056889 0.170667-0.455111-0.967111c0.455111 0.910222 1.137778 1.706667 1.706666 2.503111 1.137778 1.763556 2.275556 3.697778 3.413334 5.688889l0.568889 1.479111 0.398222 1.137778a39.537778 39.537778 0 0 1 1.592889 5.859555l0.113778 0.341334v-1.308445l0.170666 2.503111c0.113778 1.763556 0.113778 3.584 0.113778 5.404445v16.782222H643.413333a55.523556 55.523556 0 0 0-55.523555 55.580444v226.986667c0 30.72 24.803556 55.523556 55.523555 55.523556h226.986667a55.637333 55.637333 0 0 0 55.580444-55.466667v-226.986667a55.751111 55.751111 0 0 0-16.270222-39.310222 55.352889 55.352889 0 0 0-39.082666-15.928889z" fill="#7997E4" p-id="4830"></path></svg>
          <h3>架构变更</h3>
          
        </div>
          <!-- <svg t="1750470595517" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4829" width="200" height="200"><path d="M870.627556 589.198222h-105.130667v-17.635555a78.734222 78.734222 0 0 0-77.937778-78.336c-29.184-0.227556-58.481778 0-87.779555 0H533.504v-56.206223h92.899556c30.72 0 55.580444-24.803556 55.580444-55.523555V154.282667a55.523556 55.523556 0 0 0-55.466667-55.466667h-226.986666a55.580444 55.580444 0 0 0-55.523556 55.466667v226.986666c0 30.606222 24.803556 55.409778 55.466667 55.523556h89.6v56.32H335.644444a82.147556 82.147556 0 0 0-26.965333 3.868444c-23.210667 8.021333-41.415111 26.168889-49.436444 49.436445-4.209778 12.060444-3.868444 24.689778-3.868445 37.262222v3.925333H153.372444a55.637333 55.637333 0 0 0-55.580444 55.409778v226.986667a55.182222 55.182222 0 0 0 55.523556 55.523555h226.986666c30.72 0 55.523556-24.803556 55.523556-55.523555v-226.986667a55.466667 55.466667 0 0 0-55.523556-55.523555h-80.782222v-15.473778a64.625778 64.625778 0 0 1 0.284444-6.257778c0.113778-0.455111 0.113778-0.853333 0.113778-1.365333v0.796444c0.568889-2.844444 1.479111-5.688889 2.503111-8.419555a44.032 44.032 0 0 1 2.958223-5.12c0.739556-1.024 1.536-1.934222 2.104888-3.072l-0.512 0.910222 0.113778-0.113778c1.536-1.706667 3.185778-3.185778 4.835556-4.778667l1.592889-1.194666c1.706667-1.137778 3.413333-2.104889 5.290666-3.015111l-1.024 0.227555c1.024-0.227556 1.934222-0.739556 2.901334-1.137778 2.218667-0.682667 4.551111-1.251556 6.826666-1.763555l2.616889-0.341334h360.049778l1.934222 0.113778 0.910222 0.227556a56.888889 56.888889 0 0 1 5.859556 1.592889c1.194667 0.398222 2.275556 0.967111 3.527111 1.308444l-0.910222-0.227555c2.275556 1.194667 4.551111 2.503111 6.599111 3.925333l0.796444 0.682667 4.323556 4.209777 0.056889 0.170667-0.455111-0.967111c0.455111 0.910222 1.137778 1.706667 1.706666 2.503111 1.137778 1.763556 2.275556 3.697778 3.413334 5.688889l0.568889 1.479111 0.398222 1.137778a39.537778 39.537778 0 0 1 1.592889 5.859555l0.113778 0.341334v-1.308445l0.170666 2.503111c0.113778 1.763556 0.113778 3.584 0.113778 5.404445v16.782222H643.413333a55.523556 55.523556 0 0 0-55.523555 55.580444v226.986667c0 30.72 24.803556 55.523556 55.523555 55.523556h226.986667a55.637333 55.637333 0 0 0 55.580444-55.466667v-226.986667a55.751111 55.751111 0 0 0-16.270222-39.310222 55.352889 55.352889 0 0 0-39.082666-15.928889z" fill="#7997E4" p-id="4830"></path></svg>
          <h3 style="font-size: 1.2rem">架构变更</h3> -->
          <p style="font-size: 0.8rem">选择组件、模块和文件查看变更详情</p>
        </div>


        <div class="tree-content">
          <ul class="tree-list">
            <!-- 一级分类 -->
            <li v-for="(item, index) in treeData" :key="index" class="parent-node">
              <!-- <div class="tree-item" @click="selectItem(item)"> -->
                <div class="tree-item">
                <span class="icon" :class="item.icon"></span>
                <span class="label" @click="selectItem(item)">{{ item.label }}</span>
                <span v-if="item.children" class="arrow"
                      :class="{ 'expanded': item.expanded }"
                      @click.stop="toggleExpand(item)">
                  ▲
                </span>
              </div>

              <!-- 对项目逆向结果层次图做横向展示 -->
              <div v-if="item.label === '项目逆向结果层次图' && item.expanded" class="subtree">
                <div class="horizontal-children">
                  <div v-for="child in item.children"
                      :key="child.label"
                      :class="['child-card', { active: selectedItem === child }]"
                      @click.stop="selectItem(child)"
                      style="padding: 2px;">
                    <div class="tree-item">
                      <span class="icon" :class="child.icon"></span>
                      <span class="label">{{ child.label }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="selectedTreeParent && selectedTreeParent.type" class="child-detail">
                  <div class="meta-info">
                    <div><strong>版本：</strong>{{ selectedTreeParent.version }}</div>
                    <!-- <div><strong>分支：</strong>{{ selectedItem.brench }}</div> -->
                    <div><strong>时间：</strong>{{ selectedTreeParent.time }}</div>
                  </div>

                  <div class="divider-line"></div>

                  <el-tree
                    v-if="selectedTreeParent && selectedTreeParent.isTree"
                    :data="selectedTreeParent.treeData"
                    :props="{ label: 'label' , children: 'children'}"
                    :expand-on-click-node="false"
                    
                    class="sub-el-tree"
                  >
                  <!-- :render-content="renderContent" -->
                     <template #default="{ data }">
                      <span class="custom-tree-node" @click.stop="handleTreeNodeClick(data)">
                        {{ data.label }}
                        <span v-if="getChangeSymbol(data.changes_number)" style="display: inline-flex; align-items: center; gap: 6px; margin-left: 8px;">
                          <!-- 数字圆圈 -->
                          <span
                            class="change-indicator"
                            :class="getChangeColorClass(data.changeColor)"
                          >
                            {{ getChangeSymbol(data.changes_number) }}
                          </span>
                          <!-- 含义圆圈 -->
                          <span
                            class="change-indicator"
                            :class="getChangeColorClass(data.changeColor)"
                            style="font-size: 10px;"
                          >
                            {{ getChangeMeaning(data.changeColor) }}
                          </span>
                        </span>
                      </span>
                    </template>
                  </el-tree>
                </div>
              </div>

              <!-- 普通树形展示：变更分析结果（保持不变） -->
              <ul v-if="item.label !== '项目逆向结果层次图' && item.children && item.expanded" class="subtree">
                <li v-for="(child, childIndex) in item.children"
                    :key="childIndex"
                    :class="{ 'active': selectedItem === child }">
                  <div class="tree-item" @click.stop="selectItem(child)">
                    <span class="icon" :class="child.icon"></span>
                    <span class="label">{{ child.label }}</span>

                    <button v-if="['指标历史变更分析', '架构变更报告'].includes(child.label)"
                            class="download-btn"
                            @click.stop="downloadNode(child)">
                      下载
                    </button>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>

      </div>
      <!-- 这是新的拖拽条 -->
      <div 
        class="drag-bar" 
        @mousedown="startDrag"
      ></div>
      <!-- 返回按钮，放在sidebar底部 -->
      <button class="sidebar-back-btn" @click="goHomePageCopy">返回首页</button>
    </div>

    <!-- 右侧内容区域 -->
    <div class="content-area">
      <div v-if="selectedItem" class="content-container">
        <div class="content-header">
          <h2>{{ selectedItem.label }}</h2>
        </div>
        <div class="content-body">
          <!-- 如果有mdContent，就优先显示md内容 -->
          <div v-if="mdContent" class="markdown-content"
          :style="{
            height: before_code || after_code || temporary_node_category=='Function'
              ? 'calc(100% - ' + codeDiffHeight + 'px - 8px)'
              : '100%'
          }"
          ref="contentBody"
          >
            <div v-html="renderedContent"></div>
            <!-- 使用 markdown-it 渲染后的内容 -->
          </div>
          <!-- 拖拽条：只有 Function 节点才显示 -->
          <div
            v-if="before_code || after_code || temporary_node_category=='Function'"
            class="resize-bar"
            @mousedown="startResize"
          ></div>
          <!-- 新增代码对比窗口 -->
          <div v-if="before_code || after_code || temporary_node_category=='Function'" class="code-diff-container" :style="{height: codeDiffHeight + 'px', overflow: 'auto'}">
            <div class="diff-header">
              <span class="diff-label">{{version1}}</span>
              <span class="diff-label">{{version2}}</span>
            </div>
            <vue-code-diff
              :old-string="before_code || ''"
              :new-string="after_code || ''"
              :context="10"
              output-format="side-by-side"
              language="diff"
              :render-nothing-when-empty="true"
              style="height: calc(100% - 32px); background: #fff;"
            />
          </div>
          <!-- 如果没有mdContent，就显示组件内容 -->

          <!-- 这里根据选中的项目类型显示不同的内容 -->
          <template v-else-if="selectedItem && selectedItem.component">
            <component :is="selectedItem.component" ref="tableShow" />
          </template>
  <!-- <component v-else-if="selectedItem && selectedItem.component" :is="selectedItem.component" ref="tableShow" /> -->
          <!-- <div v-else class="default-content">
            <p>请选择左侧项目查看详情</p>
          </div> -->
          <!-- <template v-else>
            <div class="default-content">
              <p>请选择左侧项目查看详情</p>
            </div>
          </template> -->
        </div>
      </div>
      <div v-else class="empty-content">
        <p>请选择左侧项目查看详情</p>
      </div>

      <!-- 右侧侧边栏 -->
      <div v-if="sidebarVisible" class="right-sidebar">
        <div class="sidebar-header">
          <h3>{{ sidebarTitle }}</h3>
          <button class="close-btn" @click="closeSidebar">关闭</button>
        </div>
        <div class="sidebar-content">
          <p v-html="sidebarContent"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ArchitectureView from './ArchitectureView.vue'
import TableShow from '@/components/new/main/TableShow.vue'
import ArchitectureChange from '@/components/new/main/architectureChange.vue';
import { marked } from 'marked'
import axios from 'axios'
import EventBus from '@/components/eventBus.js'
import VMdPreview from "@kangc/v-md-editor/lib/preview"
import VMdEditor from '@kangc/v-md-editor'
import githubTheme from '@kangc/v-md-editor/lib/theme/github'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import MarkdownIt from 'markdown-it';
import MermaidGraph from '../new/main/MermaidGraph.vue';
import VueCodeDiff from 'vue-code-diff';
import { version } from 'cytoscape';
VMdEditor.use(githubTheme)
VMdPreview.use(githubTheme)

export default {
  name: 'ReverseAndChangesTotalPage',
  components: {
    ArchitectureView,
    TableShow,
    ArchitectureChange,
    VMdEditor,
    VMdPreview,
    MermaidGraph,
    VueCodeDiff,
  },
  data() {
    return {
      showUserMenu: false,
      username: localStorage.getItem("username") || "用户",
      loading: true,
      sidebarWidth: 250,   // 初始宽度（px）
      isDragging: false,   // 是否正在拖动
      startX: 0,           // 开始拖动时鼠标位置
      startWidth: 0,        // 开始拖动时sidebar宽度
      selectedItem: null,
      selectedTreeParent: null, // 新增
      treeData: [
        {
          label: '项目逆向结果层次图',
          icon: 'icon-folder',
          expanded: false,
          horizontal: true,
          children: [
            { label: 'V1层次结构图', icon: 'icon-file', expanded: false, type: 'v1', isTree: true, treeData: [], version: EventBus.version1, time: '2023'},
            { label: 'V2层次结构图', icon: 'icon-file', expanded: false, type: 'v2', isTree: true, treeData: [], version: EventBus.version2, time: EventBus.time}
          ]
        },
        {
          label: '变更分析结果',
          icon: 'icon-folder',
          expanded: false,
          horizontal: false,
          children: [
            { label: '指标历史变更分析', 
              icon: 'icon-file',
              component:'TableShow' },
            { 
              label: '架构变更视图', 
              icon: 'icon-file',
              // component: 'ArchitectureChange'
              component: 'MermaidGraph',
            },
            { 
              label: '架构变更报告', 
              icon: 'icon-file',
            }
          ]
        },
      ],
      jsonData1: null,
      jsonData2: null,
      defaultProps: {
        label: "name",
        children: "children"
      },
      mdContent: '',
      before_code : '',
      after_code :'',
      version1: EventBus.version1,
      version2: EventBus.version2,
      temporary_node_category: '', // 用于存储临时节点的 category
      codeDiffHeight: 400, // 代码对比窗口初始高度
      isResizing: false,
      startY: 0,
      startHeight: 400,


      //使用markdown-it插件展示md文档内容
      markdownIt :new MarkdownIt(),
      renderContent: '',// 用于el-tree
      //侧边栏
      sidebarVisible: false, // 控制右侧侧边栏的显示
      sidebarTitle: '', // 侧边栏标题
      sidebarContent: '', // 侧边栏内容
    }
  },
  mounted(){
    this.showChildTreeData();
    this.treeData[0].children[0].version = EventBus.version1;
    // this.treeData[0].children[0].branch = 'master';
    this.treeData[0].children[0].time = EventBus.time;
    this.treeData[0].children[1].version = EventBus.version2;
    // this.treeData[0].children[1].branch = 'main2';
    this.treeData[0].children[1].time = EventBus.time;
    // this.treeData[0].children[0].treeData = [
    //      { label: '模块1', children:[{label: '模块3'}]},
    //      { label: '模块2'}
    // ]
    this.setNodeLevels(this.treeData)
  },
  methods: {
    // 给当前点击的孩子节点添加超链接功能
    bindChildLinks() {
    const links = document.querySelectorAll('.md-child-link');
    links.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const label = link.dataset.label;
        // 找到对应的子节点
        const child = this.selectedItem.children.find(c => c.label === label);
        if (child) {
          this.handleTreeNodeClick(child); // 或 this.selectItem(child)
        }
      });
    });
  },
    // 处理窗口大小 代码差异
    startResize(e) {
      this.isResizing = true;
      this.startY = e.clientY;
      this.startHeight = this.codeDiffHeight;
      document.addEventListener('mousemove', this.onResize);
      document.addEventListener('mouseup', this.stopResize);
    },
    onResize(e) {
      if (!this.isResizing) return;
      const delta = e.clientY - this.startY;
      let newHeight = this.startHeight - delta;
      if (newHeight < 100) newHeight = 100;
      if (newHeight > this.$refs.contentBody.offsetHeight - 100) newHeight = this.$refs.contentBody.offsetHeight - 100;
      this.codeDiffHeight = newHeight;
    },
    stopResize() {
      this.isResizing = false;
      document.removeEventListener('mousemove', this.onResize);
      document.removeEventListener('mouseup', this.stopResize);
    },
     getChangeMeaning(color) {
      const map = {
        green: 'ADD',
        red: 'DEL',
        blue: 'STABLE',
        yellow: 'MOVE'
      };
      return map[color] || '';
    },
    getChangeSymbol(changes_number) {
      // 这里只返回数字，color 只用于 class
      return changes_number !== undefined ? changes_number : '';
    },
    // 获取对应颜色 class
    getChangeColorClass(color) {
      return {
        green: 'circle-green',
        red: 'circle-red',
        blue: 'circle-blue',
        yellow: 'circle-yellow'
      }[color] || '';
    },
    goHomePageCopy() {
      this.$router.push('/HomePagecopy');
    },
     toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    goUserInfo() {
      this.$router.push("/userInfo");
    },
    logout() {
      localStorage.removeItem("isLogin");
      localStorage.removeItem("username");
      this.$router.push("/");
    },
    handleClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.showUserMenu = false;
      }
    },
    setNodeLevels(nodes, level = 1) {
      nodes.forEach(node => {
        node._level = level;
        if (node.children) {
          this.setNodeLevels(node.children, level + 1);
        }
      });
    },
    showChildTreeData(){
      // v1
      // this.jsonData1 = EventBus.sharedFile1
      this.jsonData1 = EventBus.architecture1_change_json
      console.log("this.jsonData1",this.jsonData1)
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
              changeColor: item.color,
              color: item.color,
              label: item.name,
              changes_number: item.changes_num,
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

      this.treeData[0].children[0].treeData = tree;
      console.log("V1----tree")
      console.log(tree)
      // v2
      // this.jsonData2 = EventBus.sharedFile2
      this.jsonData2 = EventBus.architecture2_change_json
      console.log("this.jsonData2",this.jsonData2)
      if (!this.jsonData2) {
          return;
      }
      this.jsonData2 = this.jsonData2["structure"];

      tree = [];
      map = {};

      // 先创建 id -> 节点的映射
      this.jsonData2.forEach(item => {
          map[item.id] = { 
              ...item, 
              category: item.category === "item" ? "file" : item.category, // 替换 category
              changeColor: item.color,
              color: item.color,
              label: item.name,
              changes_number: item.changes_num,
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

        this.treeData[0].children[1].treeData = tree;
        console.log("V2----tree")
        console.log(tree)
    },
    renderContent(h, { node, data, store }) {
    return h(
      'span',
      {
        class: 'custom-tree-node',
        on: {
            click: (e) => {
            // 只有一级节点（父节点）才允许切换展开状态
            if (node.level === 1) {
              node.expanded = !node.expanded;
            }
            // 无论父子节点都处理选中逻辑
            this.handleTreeNodeClick(node);
            // 阻止事件冒泡，避免 el-tree 默认行为
            e.stopPropagation();
          }
        }
      },
      [
        h('span', data.label),
        data.changeColor
          ? h(
              'span',
              {
                class: ['change-indicator', this.getChangeColorClass(data.changeColor)]
              },
              this.getChangeSymbol(data.changeColor)
            )
          : null
      ]
    )
    },
    handleTreeNodeClick(node) {
      // 每次点击节点都先清空代码内容
      this.before_code = '';
      this.after_code = '';
      this.temporary_node_category = node.category;
      // 判断是否是父节点
      if (node._level === 1) {
        // 是父节点，不加载Markdown
        this.selectedItem = node;  // 选中该父节点
        // 保证父节点始终展开
        if (this.treeData[0].children[0]) {
          this.treeData[0].children[0].expanded = true;
        }
        this.mdContent = '';  // 清空Markdown内容
        return;
      }
      
      // 如果是子节点，加载Markdown
      this.selectedItem = node; // 选中该子节点
      console.log("选中子节点:", node);
      this.mdContent = ''; // 清空Markdown内容
      console.log("选中的label:", this.selectedItem.label);
      this.loadMarkdown(node);
      
    },
    async loadMarkdown(node) {
      // try {
      //   const response = await axios.get(mdPath);
      //   const text = response.data;  // 获取md文件内容
      //   this.mdContent = marked(text);  // 转成HTML显示
      // } catch (error) {
      //   console.error('加载MD文件失败', error);
      //   this.mdContent = '<p>加载失败</p>';
      // }
      try {
          const response = await axios.post("http://localhost:5000/get_markdown",
            {
              label: node.label,
              category: node.category,
              function: node.Functionality,
              node_allInfo:node 
            }
          );
          console.log("http://localhost:5000/get_markdown中的节点label:", node.label);
          this.mdContent = response.data.content;
          this.before_code = response.data.before_code;
          this.after_code = response.data.after_code;
          this.temporary_node_category = node.category; // 存储临时节点的 category
          // 使用 markdown-it 渲染 Markdown 内容为 HTML
          // this.renderedContent = this.markdownIt.render(this.mdContent);
          // this.loading = false;

          // 先用 markdown-it 渲染
          let html = this.markdownIt.render(this.mdContent);

          // 1. 在顶部插入一排子节点链接
          // if (node.children && node.children.length > 0) {
          //   let linksHtml = `<div class="md-children-links">`;
          //   node.children.forEach(child => {
          //     linksHtml += `<a href="#" class="md-child-link" data-label="${child.label}     </a> `;
            
          //     });
          //   linksHtml += `</div>`;
          //   html = linksHtml + html;
          // }

          // 2. 替换内容中所有子节点label为超链接
          if (node.children && node.children.length > 0) {
            node.children.forEach(child => {
              // 正则全局替换，注意转义特殊字符
              const reg = new RegExp(child.label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
              html = html.replace(
                reg,
                `<a href="#" class="md-child-link" data-label="${child.label}" style="color:#1976d2;text-decoration:underline;">${child.label}</a>`
              );
            });
          }
          this.renderedContent = html;
          this.loading = false;


          console.log("http://localhost:5000/get_markdown的label",node.label);
          console.log("http://localhost:5000/before_code",this.before_code);
          console.log("http://localhost:5000/get_markdown的after_code",this.after_code);
          console.log("http://localhost:5000/get_markdown的category",node.category);
          console.log("http://localhost:5000/get_markdown的function",node.Functionality);
      // 渲染后添加折叠效果（需延迟执行）
          this.$nextTick(() => {
            this.addCollapsibleBehavior();
            this.bindChildLinks();
          });
        } catch (error) {
          console.error("获取 Markdown 失败:", error);
          this.loading = false;
        }
    },
    // addCollapsibleBehavior() {
    //   const preview = document.querySelector('.v-md-editor-preview');
    //   if (!preview) return;

    //   let html = preview.innerHTML;

    //     // 识别函数名如：processData()
    //   html = html.replace(/\b(\w+)\(\)/g, (match, p1) => {
    //       return `<a href="#" class="md-key" data-key="${p1}">${match}</a>`;
    //   });

    //     // 识别 commitID 如 abc1234
    //   html = html.replace(/\b[a-f0-9]{7,}\b/gi, (match) => {
    //     return `<a href="#" class="md-key" data-key="${match}">${match}</a>`;
    //   });

    //   preview.innerHTML = html;

    //   // this.bindLinkClicks();


    //   const headers = preview.querySelectorAll("h1, h2, h3"); // 你也可以只选 h1 或 h2

    //   headers.forEach(header => {
    //     header.style.cursor = 'pointer';
    //     header.style.userSelect = 'none';

    //     let next = header.nextElementSibling;
    //     const children = [];

    //     while (next && !/^H[1-3]$/.test(next.tagName)) {
    //       children.push(next);
    //       next = next.nextElementSibling;
    //     }

    //     const wrapper = document.createElement('div');
    //     wrapper.classList.add('collapsible-content');
    //     children.forEach(child => wrapper.appendChild(child));

    //     header.after(wrapper);

    //     // 初始折叠状态
    //     wrapper.style.display = 'none';

    //     header.addEventListener('click', () => {
    //       wrapper.style.display = wrapper.style.display === 'none' ? 'block' : 'none';
    //     });
    //   });
    // },
    addCollapsibleBehavior() {
      const container = document.querySelector('.markdown-content');
      if (!container) return;

      // 获取所有标题标签
      const headers = container.querySelectorAll('h1, h2, h3');

      headers.forEach((header) => {
        // 设置标题样式
        header.style.cursor = 'pointer';
        header.style.userSelect = 'none';

        // 找到标题后的所有兄弟节点，直到下一个标题
        let next = header.nextElementSibling;
        const siblings = [];
        while (next && !/^H[1-3]$/.test(next.tagName)) {
          siblings.push(next);
          next = next.nextElementSibling;
        }

        // 创建一个容器包裹这些兄弟节点
        const wrapper = document.createElement('div');
        wrapper.classList.add('collapsible-content');
        siblings.forEach((sibling) => wrapper.appendChild(sibling));

        
        // 初始状态为展开
        wrapper.style.display = 'block'; // 将默认状态设置为展开
        header.classList.add('expanded'); // 添加展开样式
        header.after(wrapper);

        // 添加点击事件
        header.addEventListener('click', () => {
          const isCollapsed = wrapper.style.display === 'none';
          wrapper.style.display = isCollapsed ? 'block' : 'none';
          header.classList.toggle('expanded', isCollapsed);
        });
      });
    },
    bindLinkClicks() {
      const links = document.querySelectorAll(".md-key");
      links.forEach((link) => {
        link.addEventListener("click", async (e) => {
          e.preventDefault();
          const key = link.dataset.key;
          // 根据点击的内容动态更新侧边栏
        if (link.classList.contains("commit-id")) {
          this.sidebarTitle = `Commit ID: ${key}`;
          this.sidebarContent = `详细信息：这是 Commit ID 为 ${key} 的相关内容。`;
        } else if (link.classList.contains("function-name")) {
          this.sidebarTitle = `函数名: ${key}`;
          this.sidebarContent = `详细信息：这是函数 ${key} 的相关内容。`;
        } else if (link.classList.contains("file-name")) {
          this.sidebarTitle = `文件名: ${key}`;
          this.sidebarContent = `详细信息：这是文件 ${key} 的相关内容。`;
        }

        // 显示侧边栏
        this.sidebarVisible = true;
        });
      });
    },

    async downloadNode(child) {
        try {
            let url = '';
            let filename = '';
            let params = {};
            let blob;

            if (child.label === '指标历史变更分析') {
              // 假设TableShow组件有ref="tableShow"
              this.$refs.tableShow.exportToExcel();
              return;
            } else if (child.label === '架构变更视图') {
              url = 'http://localhost:5000/download_arch_view';
              filename = '架构变更视图.png';
              const response = await axios.post(url, params, { responseType: 'blob' });
              blob = new Blob([response.data]);
            } else if (child.label === '架构变更报告') {
              // 直接将右侧栏的md内容下载为md文件
              filename = '架构变更报告.md';
              // this.mdContent 是原始markdown文本
              blob = new Blob([this.mdContent], { type: 'text/markdown' });
            }

            if (blob) {
              const link = document.createElement('a');
              link.href = URL.createObjectURL(blob);
              link.download = filename;
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              URL.revokeObjectURL(link.href);
            }
          } catch (e) {
            this.$message && this.$message.error ? this.$message.error('下载失败') : alert('下载失败');
          }
      },


    async selectItem(item) {
      this.selectedItem = item;
      // item.expanded = true; // 确保展开
      console.log("SelectItem选中项目:", item);
      this.mdContent = ''; // 清空Markdown内容
      // 架构变更报告：访问后端获取md并渲染
      if (item.label === '架构变更报告') {
        try {
          const response = await axios.post('http://localhost:5000/get_markdown_architecture_change_report',{
            label: item.label,
          });
          this.mdContent = response.data.content;
          this.renderedContent = this.markdownIt.render(this.mdContent);
        } catch (e) {
          this.mdContent = '';
          this.renderedContent = '<p>加载失败</p>';
        }
      }else if (item.label === 'V2层次结构图' || item.label === 'V1层次结构图') {
        this.selectedTreeParent = item; // 记录父节点
        this.selectedItem = item;       // 也可以同步选中
        item.expanded = true;           // 保证展开
        try {
          // 架构变更视图：直接显示组件
          const response = await axios.post('http://localhost:5000/get_markdown_architecture_version_summary_report',{
            label: item.label,
          });
          this.mdContent = response.data.content;
          this.renderedContent = this.markdownIt.render(this.mdContent);
        } catch (e) {
          this.mdContent = '';
          this.renderedContent = '<p>加载失败</p>';
        }
      }else {
        // 子节点点击，只切换 selectedItem，不动 selectedTreeParent
        this.selectedItem = item;
        this.mdContent = '';
        // ...加载右侧内容...
      } 
    },
    toggleExpand(item) {
      // 切换展开状态
      item.expanded = !item.expanded
    },
    startDrag(e) {
      this.isDragging = true;
      this.startX = e.clientX;
      this.startWidth = this.sidebarWidth;

      document.addEventListener('mousemove', this.onDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },
    onDrag(e) {
      if (!this.isDragging) return;
      const deltaX = e.clientX - this.startX;
      let newWidth = this.startWidth + deltaX;
      // 限制最小宽度
      if (newWidth < 150) newWidth = 150;
      // 限制最大宽度（你可以按需调整）
      if (newWidth > 800) newWidth = 800;
      this.sidebarWidth = newWidth;
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener('mousemove', this.onDrag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
  }
}
</script>

<style scoped>
.md-children-links {
  margin-bottom: 12px;
  font-size: 15px;
}
.md-child-link {
  color: #1976d2;
  text-decoration: underline;
  margin-right: 16px;
  cursor: pointer;
}
.md-child-link:hover {
  color: #125199;
  text-decoration: underline;
}

.code-diff-container {
  background: #fff;
  border-radius: 8px;
  overflow: auto;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 8px 0 0 0;
  transition: height 0.1s;
  overflow: auto;
  transition: height 0.1s;
  flex-direction: column;
  min-height: 100px;
}
.diff-header {
  display: flex;
  justify-content: space-between;
  padding: 0 32px 4px 32px;
  font-weight: bold;
  color: #333;
  overflow-y: auto;
}
.diff-label {
  font-size: 15px;
}
.resize-bar {
  height: 8px;
  background: #e0e0e0;
  cursor: row-resize;
  width: 100%;
  margin: 0;
  z-index: 10;
}
.split-area {
  position: relative;
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.vscode-layout {
  display: flex;
  height: 100vh;
  background-color: #1e1e1e;
  color: #d4d4d4;
}

.tree-header {
  text-align: left;
  padding: 10px 15px;
  border-bottom: 1px solid grey;
}

.header-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.tree-header h3 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 600;
  color: #bbbbbb;
  display: inline-block;
}
.tree-header .icon {
  width: 1.2em;
  height: 1.2em;
  vertical-align: middle;
}


.sidebar {
  width: 250px;
  background-color: grey;
  border-right: 1px solid #333;
  /* overflow-y: auto; */
  overflow-y: auto; /* 添加垂直滚动条 */
  height: 100%; /* 确保高度为100% */
  position: relative;
}

.tree-container {
  padding: 10px 0;
  /* max-height: calc(100vh - 20px); */
   /* 限制最大高度，避免内容溢出 */
  /* overflow-y: auto;  */
  /* 添加滚动条 */
}

.tree-header {
  padding: 10px 15px;
  border-bottom: 1px solid grey;
}

.tree-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #bbbbbb;
}

.tree-content {
  padding: 10px 0;
}

.tree-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tree-item {
  display: flex;
  align-items: center;
  padding: 6px 15px;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.tree-item:hover {
  background-color: #2a2d2e;
}

.tree-item.active {
  background-color: #37373d;
}

.icon {
  margin-right: 8px;
  font-size: 16px;
}

.icon-folder {
  color: #e8c77e;
}

.icon-file {
  color: #6a9955;
}

.arrow {
  margin-left: auto;
  font-size: 12px;
  transition: transform 0.2s;
}

.arrow.expanded {
  transform: rotate(180deg);
}

.subtree {
  list-style: none;
  padding-left: 20px;
  margin: 0;
}

.horizontal-children {
  display: flex;
  gap: 1px;
  padding: 2px;
  flex-direction: row;
  flex-wrap: nowrap;       /* ✅ 不换行 */
  overflow-x: auto; 
  padding-left: 20px;
}

.child-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 12px;
  width: 240px;
}

.child-card.active {
  border: 2px solid #1890ff;
}

.meta-info {
  font-size: 14px;
  margin-top: 10px;
  margin-bottom: 10px;
  color: white;
  line-height: 1.6;
}

.divider-line {
  border-top: 1px solid #ccc;
  margin-top: 6px;
  margin-bottom: 6px;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
  /* background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); */
  background : #fff !important;
}

.content-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
  padding: 0;
}

.content-header {
  padding: 15px 20px;
  border-bottom: 1px solid #333;
}

.content-header h2 {
  margin: 0;
  font-size: 18px;
  color: black;
}

.content-body {
  flex: 1;
  height: 100%;
  position: relative;
  overflow: hidden;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.markdown-content {
  color: black;
  padding-left: 2%;
  background-color: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Arial', sans-serif; /* 设置字体 */
  margin: 0 auto;
  text-align: left; /* 设置左对齐 */
  line-height: 1.6; /* 增加行高，提升可读性 */
  overflow: auto;
  transition: height 0.1s;
  flex: 1 1 auto;
  min-height: 100px;
  word-wrap: break-word; /* 自动换行 */
  overflow-y: auto; /* 添加垂直滚动条 */
}
.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  color: #2c3e50; /* 设置标题颜色 */
  margin-top: 20px;
  margin-bottom: 10px;
  border-bottom: 1px solid #ddd; /* 添加下划线 */
  padding-bottom: 5px;
}
.markdown-content p {
  margin: 10px 0;
}
.markdown-content ul,
.markdown-content ol {
  padding-left: 20px;
  margin: 10px 0;
}
.empty-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 10%;
  color: #666;
}

.default-content {
  padding: 20px;
  text-align: center;
  color: #666;
}
.sidebar {
  position: relative;
  height: 100vh;
  border-right: 1px solid #ccc;
  /* overflow: hidden; */
}

.drag-bar {
  width: 5px;
  background-color: #ddd;
  cursor: ew-resize; /* 鼠标左右拉伸图标 */
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
}

.collapsible-content {
  display: none;
  margin-left: 20px; /* 缩进折叠内容 */
}

h1, h2, h3 {
  cursor: pointer;
  position: relative;
}

h1::after, h2::after{
  content: '▼'; /* 折叠箭头 */
  position: absolute;
  right: 10px;
  font-size: 12px;
  transition: transform 0.2s;
}

h1.expanded::after, h2.expanded::after, h3.expanded::after {
  transform: rotate(180deg); /* 展开箭头 */
}
.avatar-emoji {
  font-size: 1.5rem;
  margin-right: 8px;
}
.sidebar-back-btn {
  /* position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 24px; */
  width: 80%;
  padding: 10px 0;
  background: #595c5c;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  z-index: 200;
  transition: background 0.2s;
}
.sidebar-back-btn:hover {
  background-color: #2a2d2e
}

.custom-tree-node {
  display: inline-flex;
  align-items: center;
}

.change-indicator {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-size: 12px;
  margin-left: 6px;
  font-weight: bold;
  border: 2px solid;
}

/* 每种颜色的圆圈样式 */
.circle-green {
  color: green;
  border-color: green;
}
.circle-red {
  color: red;
  border-color: red;
}
.circle-blue {
  color: blue;
  border-color: blue;
}
.circle-yellow {
  color: yellow;
  border-color: yellow;
}

</style>