<template>
  <div class="mainContainer">
    <button @click="fetchMarkdown">加载文档</button>

    <div v-if="loading">加载中...</div>
    <div>
      <v-md-editor
      v-if="!loading && content"
      v-model="content"
      mode="preview"
      />
    </div>
    
    <!-- 右侧侧边栏：带折叠内容 -->
    <div v-if="activeSidebarItem" class="sidebar">
      <div class="sidebar-header">
        <span >🔍 {{ activeSidebarItem.key }}</span>
        <span @click="closeSidebar" class="sidebar-close-btn" >  ×</span>
      </div>
      <div class="sidebar-content">
        <v-md-editor
          v-model="activeSidebarItem.content"
          mode="preview"
          class="sidebar-editor"
          
        />
      </div>
      <div class="sidebar-resize-handle " @mousedown="startResize"></div>
    </div>
    <!-- 控制侧边栏显示/隐藏按钮 -->
    <!-- <button @click="toggleSidebar" class="sidebar-toggle-btn">
      {{ sidebarVisible ? '隐藏侧边栏' : '显示侧边栏' }}
    </button> -->
  </div>
</template>

<script>
import axios from 'axios'
import VMdEditor from '@kangc/v-md-editor'
import githubTheme from '@kangc/v-md-editor/lib/theme/github'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import VMdPreview from "@kangc/v-md-editor/lib/preview"

VMdEditor.use(githubTheme)
VMdPreview.use(githubTheme)

export default {

  components: {
    VMdEditor,
    VMdPreview,
  },
  data() {
    return {
      content: '',
      loading: true,
      sidebarContent: "",
      sidebarItems: [], // 每个折叠项包含：key, content, expanded
      sidebarVisible: true, // 控制侧边栏的显示和隐藏
      activeSidebarItem: null, // 当前活动的侧边栏内容
      sidebarWidth: 0, // 默认侧边栏宽度
      isResizing: false, // 是否正在拖动侧边栏
      startX: 0, // 拖动起始位置
    }
  },
  
  methods: {
  async fetchMarkdown() {
    try {
      const response = await axios.get("http://localhost:5000/get_markdown");
      this.content = response.data.content;
      this.loading = false;

      // 渲染后添加折叠效果（需延迟执行）
      this.$nextTick(() => {
        this.addCollapsibleBehavior();
      });
    } catch (error) {
      console.error("获取 Markdown 失败:", error);
      this.loading = false;
    }
  },

  addCollapsibleBehavior() {
    const preview = document.querySelector('.v-md-editor-preview');
    if (!preview) return;

    let html = preview.innerHTML;

      // 识别函数名如：processData()
    html = html.replace(/\b(\w+)\(\)/g, (match, p1) => {
        return `<a href="#" class="md-key" data-key="${p1}">${match}</a>`;
    });

      // 识别 commitID 如 abc1234
    html = html.replace(/\b[a-f0-9]{7,}\b/gi, (match) => {
      return `<a href="#" class="md-key" data-key="${match}">${match}</a>`;
    });

    preview.innerHTML = html;

    this.bindLinkClicks();


    const headers = preview.querySelectorAll("h1, h2, h3"); // 你也可以只选 h1 或 h2

    headers.forEach(header => {
      header.style.cursor = 'pointer';
      header.style.userSelect = 'none';

      let next = header.nextElementSibling;
      const children = [];

      while (next && !/^H[1-3]$/.test(next.tagName)) {
        children.push(next);
        next = next.nextElementSibling;
      }

      const wrapper = document.createElement('div');
      wrapper.classList.add('collapsible-content');
      children.forEach(child => wrapper.appendChild(child));

      header.after(wrapper);

      // 初始折叠状态
      wrapper.style.display = 'none';

      header.addEventListener('click', () => {
        wrapper.style.display = wrapper.style.display === 'none' ? 'block' : 'none';
      });
    });
  },
  bindLinkClicks() {
      const links = document.querySelectorAll(".md-key");
      links.forEach((link) => {
        link.addEventListener("click", async (e) => {
          e.preventDefault();
          const key = link.dataset.key;
          await this.loadSidebarMarkdown(key);
        });
      });
    },

  async loadSidebarMarkdown(key) {
    try {
      const res = await axios.get(`http://localhost:5000/get_markdown_by_key?key=${key}`);
      this.sidebarContent = res.data.content;
      console.log(`⚠️ 已找到与 "${key}" 对应的内容。`)
      console.log(this.sidebarContent )
      this.activeSidebarItem = {
          key,
          content: res.data.content,
        };
      // const existing = this.sidebarItems.find((item) => item.key === key);
      //   if (!existing) {
      //     this.sidebarItems.push({
      //       key,
      //       content: res.data.content,
      //       expanded: true,
      //     });
      //   } else {
      //     existing.expanded = !existing.expanded;
      //   }
    } catch (error) {
      this.sidebarContent = `⚠️ 未找到与 "${key}" 对应的内容。`;
      this.sidebarItems.push({
          key,
          content: `⚠️ 未找到与 "${key}" 对应的内容。`,
          expanded: true,
        });
      this.activeSidebarItem = {
        key,
          content: `⚠️ 未找到与 "${key}" 对应的内容。`,
      };
    }
  },
  toggleSection(index) {
      this.sidebarItems[index].expanded = !this.sidebarItems[index].expanded;
  },
  closeSidebar() {
      this.activeSidebarItem = null; // 关闭侧边栏
    },
  // toggleSidebar() {
  //     this.sidebarVisible = !this.sidebarVisible;
  //   },
  // 鼠标按下事件，开始拖动
  // 鼠标按下事件，开始拖动调整宽度
  startResize(e) {
      this.isResizing = true;
      this.startX = e.clientX;

      // 添加鼠标移动和鼠标松开事件
      document.addEventListener("mousemove", this.resizeSidebar);
      document.addEventListener("mouseup", this.stopResize);
    },

    // 鼠标移动事件，调整侧边栏宽度
    resizeSidebar(e) {
      if (this.isResizing) {
        const diff = this.startX - e.clientX;
        this.sidebarWidth = Math.max(200, this.sidebarWidth - diff); // 限制最小宽度为 200px
        this.startX = e.clientX;
      }
    },

    // 鼠标松开事件，停止调整宽度
    stopResize() {
      this.isResizing = false;
      document.removeEventListener("mousemove", this.resizeSidebar);
      document.removeEventListener("mouseup", this.stopResize);
    },
  },
  //   mounted() {
  //     this.fetchMarkdown();
  // },
}
</script>

<style scoped>
.mainContainer {
    width: 100%;
    height: 100%;
    display: flex;
    border: 1px solid #ddd;
    background: #0070f3;
}
/* 修改字体颜色和背景色 */
.v-md-editor-preview {
  color: black !important;
  background-color: #182f46 !important;
  padding: 16px;
  border-radius: 8px;
}

/* 可选：调整整体容器样式 */
.v-md-editor {
  background-color: #718caa !important;
  border: 1px solid #2c3e50;
}
.tree-container {
  width: 30%;
  border-right: 1px solid #271e1e;
  padding-right: 10px;
}

.markdown-content {
  padding-top: 20px;
}
button {
  margin-bottom: 10px;
}
.header {
  cursor: pointer;
  color: #0070f3; /* 标题文本颜色设为黑色 */
  font-weight: bold;
}

a.md-key {
  color: #0070f3;
  text-decoration: underline;
  cursor: pointer;
}
a.md-key:hover {
  color: #0056b3;
}



.sidebar-content {
  padding: 10px;
  background-color: #718caa;
}

.main-editor {
  height: calc(100vh - 40px);
}

.sidebar-editor {
  max-height: 1085px;
  overflow-y: auto;
  overflow-x: auto;
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #0070f3;
}

.sidebar {
  position: auto;
  top: 0;
  right: 0;
  width: 300px;
  height: 100%;
  transition: transform 0.3s ease;
  transform: translateX(0);
}

.sidebar-toggle-btn {
  position: fixed;
  top: 10px;
  right: 320px;
  padding: 10px;
  background-color: #0070f3;
  color: #0070f3;
  border: none;
  cursor: pointer;
  z-index: 1000;
}

.sidebar-toggle-btn:hover {
  background-color: #718caa;
}

.sidebar[style*="transform: translateX(0)"] {
  transform: translateX(0);
}

.sidebar[style*="transform: translateX(100%)"] {
  transform: translateX(100%);
}

.sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 300px;
  height: 100%;
  background-color: #718caa;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  z-index: 999;
}

.sidebar-close-btn {
  cursor: pointer;
  font-size: 18px;
  color: #a41d82;
}

.sidebar-close-btn:hover {
  color: #f00;
}

.sidebar-resize-handle {
  position: absolute;
  top: 0;
  left: -5px;
  width: 10px;
  height: 100%;
  cursor: ew-resize;
  background-color: white;
}
</style>