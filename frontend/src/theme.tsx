import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
  colors: {
    ui: {
      main: '#009688',
      secondary: '#EDF2F7',
      success: '#48BB78',
      danger: '#E53E3E',
    },
  },
  components: {
    Tabs: {
      variants: {
        enclosed: {
          tab: {
            _selected: {
              color: 'ui.main',
            },
          },
        },
      },
    },
  },
})

export default theme
