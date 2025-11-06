<template>
  <ul>
    <li v-for="(node, index) in nodes" :key="index">
      <div @click="toggle(node)" class="node">
        <span v-if="node.children.length">
          <span v-if="node.expanded">📂</span>
          <span v-else>📁</span>
        </span>
        <span v-else>📄</span>

        <span class="title" @click.stop="jumpTo(node)">
          {{ node.title }}
        </span>
      </div>

      <ul v-if="node.expanded">
        <markdown-tree :nodes="node.children" @jumpTo="jumpTo"></markdown-tree>
      </ul>
    </li>
  </ul>
</template>

<script>
export default {
  name: "MarkdownTree",
  props: {
    nodes: Array
  },
  methods: {
    toggle(node) {
      if (node.children.length) {
        this.$set(node, "expanded", !node.expanded);
      }
    },
    jumpTo(node) {
      this.$emit("jumpTo", node.id);
    }
  }
};
</script>

<style scoped>
.node {
  cursor: pointer;
  padding: 5px 0;
}
.title {
  margin-left: 5px;
  color: blue;
  text-decoration: underline;
  cursor: pointer;
}
</style>
