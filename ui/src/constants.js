export default {
  zimfarm_webapi: window.environ.ZIMFARM_WEBAPI || "https://api.farm.youzim.it/v1",
  zimitui_api: window.environ.ZIMIT_API_URL || "/api/v1",
  zimit_limit: window.environ.ZIMIT_LIMIT,
  zim_download_url: window.environ.ZIM_DOWNLOAD_URL || "https://s3.us-west-1.wasabisys.com/org-kiwix-zimit/zim",
  ALERT_DEFAULT_DURATION: 5,
  ALERT_LONG_DURATION: 10,
  ALERT_PERMANENT_DURATION: true,
  zimit_refresh_after: parseInt(window.environ.ZIM_DOWNLOAD_URL || "60"),
  zimit_fields: ["lang", "title", "description", "favicon", "zim_file", "limit",
                 "tags", "creator", "source", "include_domains", "exclude",
                 "wait_until", "scope", "scroll", "page", "use_sitemap", "mobile_device"],
  hidden_flags: ["adminEmail", "name", "output", "statsFilename", "url", "zim-file"],
  yes_no(value, value_yes, value_no) {
    if (!value_yes)
      value_yes = "yes";
    if (!value_no)
      value_no = "no";
    return value ? value_yes : value_no;
  },
  standardHTTPError(response) {
    let statuses = {
      // 1××: Informational
      100: "Continue",
      101: "Switching Protocols",
      102: "Processing",

      // 2××: Success
      200: "OK",
      201: "Created",
      202: "Accepted",
      203: "Non-authoritative Information",
      204: "No Content",
      205: "Reset Content",
      206: "Partial Content",
      207: "Multi-Status",
      208: "Already Reported",
      226: "IM Used",

      // 3××: Redirection
      300: "Multiple Choices",
      301: "Moved Permanently",
      302: "Found",
      303: "See Other",
      304: "Not Modified",
      305: "Use Proxy",
      307: "Temporary Redirect",
      308: "Permanent Redirect",

      // 4××: Client Error
      400: "Bad Request",
      401: "Unauthorized",
      402: "Payment Required",
      403: "Forbidden",
      404: "Not Found",
      405: "Method Not Allowed",
      406: "Not Acceptable",
      407: "Proxy Authentication Required",
      408: "Request Timeout",
      409: "Conflict",
      410: "Gone",
      411: "Length Required",
      412: "Precondition Failed",
      413: "Payload Too Large",
      414: "Request-URI Too Long",
      415: "Unsupported Media Type",
      416: "Requested Range Not Satisfiable",
      417: "Expectation Failed",
      418: "I'm a teapot",
      421: "Misdirected Request",
      422: "Unprocessable Entity",
      423: "Locked",
      424: "Failed Dependency",
      426: "Upgrade Required",
      428: "Precondition Required",
      429: "Too Many Requests",
      431: "Request Header Fields Too Large",
      444: "Connection Closed Without Response",
      451: "Unavailable For Legal Reasons",
      499: "Client Closed Request",

      //5××: Server Error
      500: "Internal Server Error",
      501: "Not Implemented",
      502: "Bad Gateway",
      503: "Service Unavailable",
      504: "Gateway Timeout",
      505: "HTTP Version Not Supported",
      506: "Variant Also Negotiates",
      507: "Insufficient Storage",
      508: "Loop Detected",
      510: "Not Extended",
      511: "Network Authentication Required",
      599: "Network Connect Timeout Error",
    };

    if (response === undefined) { // no response
                                  //usually due to browser blocking failed OPTION preflight request
      return "Cross-Origin Request Blocked: preflight request failed."
    }
    let status_text = response.statusText ? response.statusText : statuses[response.status];
    if (response.status == 400) {
      if (response.data && response.data.error)
        status_text += "<br />" + JSON.stringify(response.data.error);
      if (response.data && response.data.error_description)
        status_text += "<br />" + JSON.stringify(response.data.error_description);
      if (response.data && response.data.message)
        status_text += "<br />" + JSON.stringify(response.data.message);
    }
    return response.status + ": " + status_text + ".";
  },
};
