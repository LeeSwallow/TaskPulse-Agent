export function createMainWindowConfig() {
  return {
    width: 1440,
    height: 960,
    minWidth: 1200,
    minHeight: 760,
    title: 'TaskPulse Agent',
    backgroundColor: '#efe6d8',
    preload: '../preload/preload.js',
  }
}
