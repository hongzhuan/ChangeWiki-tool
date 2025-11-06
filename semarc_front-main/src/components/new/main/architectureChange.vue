<template>
    <div class="mainContainer">
        <div>
        <button @click="fetchPlantUML" class="btn">获取架构数据</button>
        <div v-if="plantUMLCode">
          <!-- <img :src="plantUMLUrl" alt="架构图" /> -->
          <img 
            :src="plantUMLUrl" 
            alt="架构图" 
            class="plantuml-image" 
            :style="{ 
              transform: `scale(${scale}) translate(${position.x}px, ${position.y}px)`
            }"
            @wheel.prevent="zoomImage"
            @mousedown="startDrag"
          />
        </div>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import plantumlEncoder from 'plantuml-encoder';
export default {
    name: 'ArchitectureChange',
    data() {
      return {
        plantUMLCode: "", // 存储 PlantUML 代码
        scale: 1, // 图片缩放比例
        position: { x: 0, y: 0 }, // 记录图片的偏移量
        isDragging: false, // 是否正在拖拽
        startX: 0, 
        startY: 0
      };
    },
    computed: {
    // **动态计算 PlantUML 服务器 URL**
    plantUMLUrl() {
      if (!this.plantUMLCode) return "";
      console.log("plantUMLCode:")
      console.log(this.plantUMLCode)
      console.log("hahahahha_plantUMLUrl")
      return `https://www.plantuml.com/plantuml/svg/${plantumlEncoder.encode(this.plantUMLCode)}`;
    },
  },
  methods: {
    async fetchPlantUML() {
      try {
        const response = await axios.get("http://localhost:5000/api/plantuml");
        console.log("后端返回的数据:", response.data.architecture_data);
        this.generatePlantUML(response.data.architecture_data);
      } catch (error) {
        console.error("获取数据失败:", error);
      }
    },
    generatePlantUML(data) {
      let plantUML = "@startuml\n";
      plantUML += "top to bottom direction\n";
      plantUML += "skinparam componentStyle rectangle\n\n";

      // 组件分组
      data.components.forEach((group) => {
        plantUML += `rectangle ${group.name} {\n`;
        group.elements.forEach((component) => {
          plantUML += `  component ${component.name} #${component.color}\n`;
        });
        plantUML += "}\n\n";
      });

      // 连接关系
      data.connections.forEach((conn) => {
        if (conn.hidden) {
          plantUML += `${conn.from} -[hidden]-> ${conn.to}\n`;
        } else {
          plantUML += `${conn.from} --> ${conn.to}\n`;
        }
      });

      plantUML += "@enduml";
      this.plantUMLCode = plantUML;
    },
    // **正确的 PlantUML 编码**
    encodePlantUML(umlString) {
      return encodeURIComponent(umlString)
        .replace(/\(/g, "%28")
        .replace(/\)/g, "%29")
        .replace(/%20/g, " ");
    },
    zoomImage(event) {
      const zoomStep = 0.1; // 每次缩放的增量
      if (event.deltaY < 0) {
        this.scale = Math.min(this.scale + zoomStep, 3); // 放大，最大 3 倍
      } else {
        this.scale = Math.max(this.scale - zoomStep, 0.5); // 缩小，最小 0.5 倍
      }
    },
    // **开始拖动**
    startDrag(event) {
      this.isDragging = true;
      this.startX = event.clientX - this.position.x;
      this.startY = event.clientY - this.position.y;

      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },

    // **拖动过程中**
    onDrag(event) {
      if (!this.isDragging) return;
      this.position.x = event.clientX - this.startX;
      this.position.y = event.clientY - this.startY;
    },

    // **停止拖动**
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
    },

  },
};
</script>

<style scoped>
.mainContainer {
    width: 100%;
    height: 100%;
    display: flex;
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
  height: 40px;
  width: 125px;
  margin-top: 10px;
  margin-left: 10px;
}
.btn:hover {
  background-color: #9ACBD0;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}
.plantuml-image {
  max-width: 100%;
  height: auto;
  cursor: zoom-in;
  transition: transform 0.2s ease-in-out;
}
</style>