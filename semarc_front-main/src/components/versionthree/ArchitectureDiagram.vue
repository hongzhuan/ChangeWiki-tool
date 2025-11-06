<template>
  <div class="architecture-diagram">
    <svg :width="width" :height="height" class="diagram">
      <g v-for="(component, index) in structure" :key="index" :transform="`translate(0, ${index * (componentHeight + spacing)})`">
        <!-- Component rectangle -->
        <rect
          :x="0"
          :y="0"
          :width="width"
          :height="componentHeight"
          class="component"
          rx="5"
          ry="5"
        />
        <text
          :x="width/2"
          :y="componentHeight/2"
          text-anchor="middle"
          dominant-baseline="middle"
          class="component-text"
        >
          {{ component.name }}
        </text>
        
        <!-- Nested clusters -->
        <g v-for="(cluster, clusterIndex) in component.nested" :key="clusterIndex"
           :transform="`translate(${clusterSpacing}, ${clusterSpacing + clusterIndex * (clusterHeight + clusterSpacing)})`">
          <rect
            :width="width - 2 * clusterSpacing"
            :height="clusterHeight"
            class="cluster"
            rx="3"
            ry="3"
          />
          <text
            :x="(width - 2 * clusterSpacing)/2"
            :y="clusterHeight/2"
            text-anchor="middle"
            dominant-baseline="middle"
            class="cluster-text"
          >
            {{ cluster.name }}
          </text>
        </g>
      </g>
    </svg>
  </div>
</template>

<script>
export default {
  name: 'ArchitectureDiagram',
  props: {
    structure: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      width: 800,
      componentHeight: 200,
      clusterHeight: 60,
      spacing: 50,
      clusterSpacing: 20
    }
  },
  computed: {
    height() {
      return this.structure.length * (this.componentHeight + this.spacing)
    }
  }
}
</script>

<style scoped>
.architecture-diagram {
  padding: 20px;
  overflow: auto;
}

.diagram {
  background-color: #f8f9fa;
}

.component {
  fill: #e9ecef;
  stroke: #6c757d;
  stroke-width: 2;
}

.cluster {
  fill: #dee2e6;
  stroke: #495057;
  stroke-width: 1;
}

.component-text {
  font-size: 16px;
  font-weight: bold;
  fill: #212529;
}

.cluster-text {
  font-size: 14px;
  fill: #343a40;
}
</style> 