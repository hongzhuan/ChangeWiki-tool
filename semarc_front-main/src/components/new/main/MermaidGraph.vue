<template>
  <div>
    <!-- 图例区域 -->
    <div class="legend-container">
      <div class="legend-item">
        <svg width="32" height="32">
          <rect x="3" y="3" width="40" height="26" stroke="#333" stroke-width="3" fill="#9f6" fill-opacity="0.7"/>
        </svg>
        <span>新增</span>
      </div>
      <div class="legend-item">
        <svg width="32" height="32">
          <rect x="3" y="3" width="40" height="26" stroke="#333" stroke-width="3" fill="#f96" fill-opacity="0.7"/>
        </svg>
        <span>移动</span>
      </div>
      <div class="legend-item">
        <svg width="32" height="32">
          <rect x="3" y="3" width="40" height="26" stroke="#333" stroke-width="3" fill="#add8e6" fill-opacity="0.7"/>
        </svg>
        <span>不变</span>
      </div>
      <div class="legend-item">
        <svg width="32" height="32">
          <rect x="3" y="3" width="40" height="26" stroke="#333" stroke-width="3" fill="#FF0000" fill-opacity="0.7"/>
        </svg>
        <span>删除</span>
      </div>
    </div>
    <div ref="mermaidRenderArea" class="mermaid-container" id="mermaid-container"></div>
    <button @click="downloadImage">下载图片</button>
  </div>
</template>

<script>
import axios from "axios";
import mermaid from "mermaid";
import html2canvas from "html2canvas";

export default {
  name: "MermaidGraph",
  data() {
    return {
      mermaidData: "",
    };
  },
  mounted() {
      mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose", // 允许内嵌 HTML 和样式
      theme: "default",
      useShadowDOM: false, // ✅ 关键：关闭 Shadow DOM，样式才能作用到 SVG 内容
      themeVariables: {
        fontSize: "16px",
        textColor: "#000000",
        fontFamily: "Arial"
      }
    });
    this.loadMermaidData();
  },
  methods: {
    async loadMermaidData() {
      try {
        const res = await axios.post("http://localhost:5000/api/plantuml",{
          name2 : "MermaidGraph",
        }); // 改为你实际后端接口
        this.mermaidData = res.data.mermaid_data;
        console.log("Mermaid 数据加载成功：", this.mermaidData);
        if (!this.mermaidData || typeof this.mermaidData !== "string") {
          throw new Error("无效的 Mermaid 数据");
        }

        this.$nextTick(() => {
          this.renderMermaid();
        });
      } catch (err) {
        console.error("加载或渲染失败：", err);
      }
    },
    renderMermaid() {
      const graphId = "mermaid-graph";
      const el = this.$refs.mermaidRenderArea;
      // 清空旧图
      el.innerHTML = "";
      // 创建新的容器并设置 HTML
      const container = document.createElement("div");
      container.className = "mermaid";
      container.innerHTML = this.mermaidData;
      el.appendChild(container);
      // Mermaid 对该节点重新初始化
      mermaid.init(undefined, container);
    },
    async downloadImage() {
      try {
        const container = this.$refs.mermaidRenderArea;
        const canvas = await html2canvas(container);
        const link = document.createElement("a");
        link.download = "mermaid-diagram.png";
        link.href = canvas.toDataURL("image/png");
        link.click();
      } catch (err) {
        console.error("下载失败：", err);
      }
    },
  },
};
</script>

<style scoped>
.legend-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 24px;         /* 图例之间的间距 */
  justify-content: center; /* 水平居中 */
  margin-bottom: 16px;
  flex-wrap: nowrap; /* 不换行 */
}
.legend-item {
  gap: 16px; 
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #333;
  margin-left: 20px;
}
.mermaid-container {
  color: #333;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  padding: 20px;
}
button {
  margin-top: 20px;
}
.legend-container{
  color: #333;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.mermaid-container svg text {
  fill: #000 !important;
}
</style>
