import { reactive } from 'vue';
import Architecture_change_graph from './changeanalysis/architecture_change_graph.vue';
import { version } from 'cytoscape';

export const EventBus = reactive({
  sharedFile1: null,
  sharedFile2: null,
  a2a_value: '',
  module_weight: '',
  architecture1_change_json: '',
  architecture2_change_json: '',
  reverse1_change_json: '',
  reverse2_change_json: '',
  a2a_tableInfo: '',
  a2a_tableInfo_json_add_fileInfo: '',
  git_branches: '',
  git_tags: '',
  repo_url: '',
  version1:'',
  version2:'',
  time: '',
});
if (import.meta.hot) {
  import.meta.hot.accept();
}

export default EventBus;