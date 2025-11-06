import { reactive } from 'vue';

export const EventBus = reactive({
  sharedFile: null,
});
if (import.meta.hot) {
    import.meta.hot.accept();
  }
  
export default EventBus;