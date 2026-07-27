# WebSockets की Testing { #testing-websockets }

आप WebSockets को test करने के लिए उसी `TestClient` का उपयोग कर सकते हैं।

इसके लिए, आप `TestClient` को एक `with` statement में उपयोग करते हैं, WebSocket से connect करते हुए:

{* ../../docs_src/app_testing/tutorial002_py310.py hl[27:31] *}

/// note | नोट

अधिक जानकारी के लिए, Starlette की documentation में [WebSockets की testing](https://www.starlette.dev/testclient/#testing-websocket-sessions) देखें।

///
