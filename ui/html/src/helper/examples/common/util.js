export const getComponents = (context) => {
  // const components = {}
  const components = []
  context.keys().forEach((item) => {
    const component = context(item).default || context(item)
    if (component.name) {
      // components[component.name] = component
      components.push({ tabId: component.name, tabName: component.title, show: true, component })
    }
  })
  return { components }
}
