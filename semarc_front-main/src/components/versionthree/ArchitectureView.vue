<template>
  <div class="architecture-view">
    <h1>Project Architecture</h1>
    <ArchitectureDiagram :structure="architectureData" />
  </div>
</template>

<script>
import ArchitectureDiagram from '@/components/versionthree/ArchitectureDiagram.vue'

export default {
  name: 'ArchitectureView',
  components: {
    ArchitectureDiagram
  },
  data() {
    return {
      architectureData:[
        {
            "@type": "component",
            "name": "Scalability and Concurrent Execution",
            "nested": [
                {
                    "@type": "cluster",
                    "name": "libuv_Testing_and_Benchmarking_Suite"
                }
            ]
        },
        {
            "@type": "component",
            "name": "Plugin Management and Extensibility",
            "nested": [
                {
                    "@type": "cluster",
                    "name": "libuv_Functionality_and_Performance_Tests"
                }
            ]
        },
        {
            "@type": "component",
            "name": "Asynchronous Task Distribution (Slaves)",
            "nested": [
                {
                    "@type": "cluster",
                    "name": "libuv_Core_and_Platform-Specific_Functionalities"
                },
                {
                    "@type": "cluster",
                    "name": "libuv_Asynchronous_I/O_and_Multi-threading_Test_Suite"
                }
            ]
        },
        {
            "@type": "component",
            "name": "Benchmarking and Testing",
            "nested": [
                {
                    "@type": "cluster",
                    "name": "libuv_Functionality_Testing_Suite"
                }
            ]
        },
        {
            "@type": "component",
            "name": "Fault Tolerance and Error Handling",
            "nested": [
                {
                    "@type": "cluster",
                    "name": "libuv_Functionality_and_Behavior_Tests"
                }
            ]
        },
        {
            "@type": "component",
            "name": "Centralized Event Loop (Master)",
            "nested": [
                {
                    "@type": "cluster",
                    "name": "libuv_Functional_and_Performance_Testing_Suite"
                },
                {
                    "@type": "cluster",
                    "name": "Platform-Specific_I/O_and_System_Resource_Management_for_libuv"
                }
            ]
        },
        {
            "@type": "component",
            "name": "Platform-Specific Implementations (Distributed Execution)",
            "nested": [
                {
                    "@type": "cluster",
                    "name": "libuv_Functionality_and_Performance_Testing"
                }
            ]
        }
    ]
    }
  }
}
</script>

<style scoped>
.architecture-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}
</style> 