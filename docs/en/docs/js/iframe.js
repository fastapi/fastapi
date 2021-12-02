function inIframe() {
    try {
      return window.self !== window.top;
    } catch (err) {
      console.log("Iframe error: ", err)
      return true;
    }
  }
  
  if (inIframe()) {
    document.getElementsByTagName('html')[0].classList.add('loaded-in-iframe');
  }
