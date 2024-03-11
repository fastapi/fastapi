import { extendTheme } from '@chakra-ui/react'

const disabledStyles = {
  _disabled: {
    backgroundColor: 'ui.main',
  },
}

const theme = extendTheme({
  colors: {
    ui: {
      main: '#009688',
      secondary: '#EDF2F7',
      success: '#48BB78',
      danger: '#E53E3E',
      white: '#FFFFFF',
      dark: '#1A202C',
      darkSlate: '#252D3D',
    },
  },
  components: {
    Button: {
      variants: {
        primary: {
          backgroundColor: 'ui.main',
          color: 'ui.white',
          _hover: {
            backgroundColor: '#00766C',
          },
          _disabled: {
            ...disabledStyles,
            _hover: {
              ...disabledStyles,
            },
          },
        },
        danger: {
          backgroundColor: 'ui.danger',
          color: 'ui.white',
          _hover: {
            backgroundColor: '#E32727',
          },
        },
      },
    },
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
