<template>
  <div class="dialog-overlay">
    <div >
      <h2>PlantUML 视图</h2>
      <!-- 这里是你的 PlantUML 相关内容 -->
      <div @mousedown="startDrag" @mouseup="stopDrag" @mousemove="drag">
        <img  class="scaled-image"
        :style="imageStyle"
        :src="plantUMLUrl" alt="PlantUML Diagram" 
        @wheel="zoom"
        />
      </div>
      <button class="close-btn" @click="$emit('close')">×</button>
    </div>
  </div>
</template>

<script>
import plantumlEncoder from 'plantuml-encoder';
export default {
  name: "PlantUMLRight",
  data() {
    return {
      pumlCode: `
        @startuml
        

        node "Event Loop" {
            [libuv-platforms] as 4
            [Libuv Core Functionality and Performance Testing] as 5
        }

        

        node "Signal-Handler" {
          [libuv Network and Resource Management Test Suite] as 1
          [System Resource Management and Asynchronous I/O] as 2
          [libuv Error Handling and Event Loop Behavior Tests] as 3
        }

        node "Thread Pool"{
          [libuv Functionality and Behavior Testing] as 6
        }
        1 --> 4: 1619
        2 --> 4: 761
        5 --> 4: 694
        6 --> 4: 672
        4 --> 5: 468
        3 --> 4: 286
        1 --> 5: 238
        4 --> 2: 188
        6 --> 5: 120
        4 --> 1: 80
        
              
        @enduml
      `,
      scale: 0.65,
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      positionX: 0,
      positionY: 0,
    };
  },
  computed: {
    plantUMLUrl() {
      const encoded = plantumlEncoder.encode(this.pumlCode);
      return `https://www.plantuml.com/plantuml/svg/${encoded}`;
    },
    imageStyle() {
      return {
        transform: `scale(${this.scale}) translate(${this.positionX}px, ${this.positionY}px)`,
        transition: this.isDragging ? "none" : "transform 0.3s ease",
      };
    },
  },
  methods: {
    zoom(event) {
      event.preventDefault();
      event.stopPropagation();
      
      // const img = event.target;
      let newScale = this.scale + event.deltaY * -0.001;
      this.scale = Math.max(0.1, newScale);
      console.log("this.scale:"+this.scale);
      // this.scale = ${Math.max(0.1, img.scale + delta)};
    },
    startDrag(event) {
      this.isDragging = true;
      this.dragStartX = event.clientX - this.positionX;
      this.dragStartY = event.clientY - this.positionY;
      document.addEventListener("mousemove", this.drag);
      document.addEventListener("mouseup", this.stopDrag);
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.drag);
      document.removeEventListener("mouseup", this.stopDrag);
    },
    drag(event) {
      if (this.isDragging) {
        this.positionX = event.clientX - this.dragStartX;
        this.positionY = event.clientY - this.dragStartY;
      }
    },
  },
};
</script>

<style scoped>
.scaled-image {
    transition: transform 0.3s ease;
    transform-origin: center; /* 缩放中心 */
}
/* 遮罩层 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 50%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  color: white;
}

/* 对话框内容 */
.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: red;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
</style>
