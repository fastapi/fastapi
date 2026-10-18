# पुराने 403 Authentication Error Status Codes का उपयोग करें { #use-old-403-authentication-error-status-codes }

FastAPI version `0.122.0` से पहले, जब integrated security utilities failed authentication के बाद client को error लौटाती थीं, तो वे HTTP status code `403 Forbidden` का उपयोग करती थीं।

FastAPI version `0.122.0` से शुरू होकर, वे अधिक उपयुक्त HTTP status code `401 Unauthorized` का उपयोग करती हैं, और HTTP specifications, [RFC 7235](https://datatracker.ietf.org/doc/html/rfc7235#section-3.1), [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized) का पालन करते हुए response में एक उचित `WWW-Authenticate` header लौटाती हैं।

लेकिन अगर किसी कारण से आपके clients पुराने behavior पर निर्भर हैं, तो आप अपनी security classes में method `make_not_authenticated_error` को override करके उस पर वापस जा सकते हैं।

उदाहरण के लिए, आप `HTTPBearer` का एक subclass बना सकते हैं जो default `401 Unauthorized` error के बजाय `403 Forbidden` error लौटाता है:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | टिप

ध्यान दें कि function exception instance लौटाता है, उसे raise नहीं करता। raising बाकी internal code में किया जाता है।

///
